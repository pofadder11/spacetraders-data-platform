"""
refuel_routing.py
Route planning with market/fuel constraints + corridor filtering + refuel optimization.

Requirements:
    pip install networkx matplotlib

Provides:
    - Node dataclass
    - inside_corridor, corridor_polygon
    - build_candidates, build_reachability_graph
    - astar_by_time (A* with admissible straight-line-time heuristic)
    - compute_refuel_plan (cheapest-next-within-range greedy policy)
    - plan_route_and_refuel (high-level one-call)

This module is UI-agnostic; pair it with a demo script to visualize.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Iterable
import math
import networkx as nx


# ----------------------
# Data structures
# ----------------------

@dataclass(frozen=True)
class Node:
    symbol: str
    x: float
    y: float
    has_fuel: bool = False
    price: Optional[float] = None  # price per fuel unit if known


# ----------------------
# Geometry helpers
# ----------------------

def euclid(a: Node, b: Node) -> float:
    dx, dy = (a.x - b.x), (a.y - b.y)
    return math.hypot(dx, dy)

def _point_segment_distance(px, py, ax, ay, bx, by) -> float:
    """Distance from point P(px,py) to segment AB(ax,ay)-(bx,by)."""
    apx, apy = px - ax, py - ay
    abx, aby = bx - ax, by - ay
    ab2 = abx * abx + aby * aby
    if ab2 == 0:
        return math.hypot(apx, apy)
    t = max(0.0, min(1.0, (apx * abx + apy * aby) / ab2))
    cx, cy = ax + t * abx, ay + t * aby
    return math.hypot(px - cx, py - cy)

def inside_corridor(p: Node, s: Node, t: Node, width: float) -> bool:
    """Return True if node p lies within 'width' of the S->T line segment."""
    return _point_segment_distance(p.x, p.y, s.x, s.y, t.x, t.y) <= width

def corridor_polygon(sx, sy, tx, ty, half_width):
    """Return polygon points for a band of half_width around segment S->T."""
    dx, dy = tx - sx, ty - sy
    L = math.hypot(dx, dy)
    if L == 0:
        return [(sx - half_width, sy - half_width),
                (sx + half_width, sy - half_width),
                (sx + half_width, sy + half_width),
                (sx - half_width, sy + half_width)]
    # unit perpendicular to the segment
    ux, uy = -dy / L, dx / L
    p1 = (sx + ux * half_width, sy + uy * half_width)
    p2 = (tx + ux * half_width, ty + uy * half_width)
    p3 = (tx - ux * half_width, ty - uy * half_width)
    p4 = (sx - ux * half_width, sy - uy * half_width)
    return [p1, p2, p3, p4]


# ----------------------
# Graph construction
# ----------------------

def build_candidates(
    all_nodes: Iterable[Node],
    start: Node,
    goal: Node,
    corridor_width: float,
    keep_k_nearest_extra: int = 0,
) -> List[Node]:
    """
    Filter to a corridor around S->T. Optionally keep a few nearest out-of-corridor nodes.
    """
    candidates: List[Node] = []
    out_of_corridor: List[Tuple[float, Node]] = []
    for n in all_nodes:
        if n.symbol in (start.symbol, goal.symbol):
            continue
        if inside_corridor(n, start, goal, corridor_width):
            candidates.append(n)
        else:
            out_of_corridor.append((euclid(n, start) + euclid(n, goal), n))
    out_of_corridor.sort(key=lambda x: x[0])
    extras = [n for _, n in out_of_corridor[:keep_k_nearest_extra]]
    return [start, goal] + candidates + extras


def build_reachability_graph(
    nodes: List[Node],
    max_range: float,
    speed_au_per_hr: float,
    landing_overhead_hr: float = 0.0,
    non_market_penalty: float = 0.0,
) -> nx.DiGraph:
    """
    Create edges only when the hop is ≤ max_range (single-tank reach).
    Edge 'weight' = travel time + arrival overhead + optional penalty when arriving at a non-market.

    non_market_penalty: extra cost added to arriving at a node that doesn't sell fuel
                        (biases paths to land on markets).
    """
    G = nx.DiGraph()
    for n in nodes:
        G.add_node(n.symbol, data=n)

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                continue
            a, b = nodes[i], nodes[j]
            d = euclid(a, b)
            if d <= max_range:
                travel_time = d / speed_au_per_hr
                arrival_overhead = landing_overhead_hr
                arrival_penalty = (non_market_penalty if not b.has_fuel else 0.0)
                w = travel_time + arrival_overhead + arrival_penalty
                G.add_edge(a.symbol, b.symbol, distance=d, time=travel_time, weight=w)
    return G


# ----------------------
# Shortest path (A* with admissible heuristic)
# ----------------------

def astar_by_time(G: nx.DiGraph, start: str, goal: str, speed_au_per_hr: float) -> List[str]:
    """
    A* shortest path with straight-line travel time heuristic.
    Compatible with networkx.astar_path which calls heuristic(u, v).
    """
    if start == goal:
        return [start]
    pos: Dict[str, Tuple[float, float]] = {
        n: (G.nodes[n]["data"].x, G.nodes[n]["data"].y) for n in G.nodes
    }
    gx, gy = pos[goal]

    def h(u: str, v: Optional[str] = None) -> float:
        ux, uy = pos[u]
        return math.hypot(ux - gx, uy - gy) / speed_au_per_hr

    try:
        return nx.astar_path(G, start, goal, heuristic=h, weight="weight")
    except nx.NetworkXNoPath:
        return nx.dijkstra_path(G, start, goal, weight="weight")


# ----------------------
# Refuel planning
# ----------------------

def fuel_for_leg(distance_au: float, burn_per_au: float) -> int:
    return math.ceil(distance_au * burn_per_au)

def _price_of(node: Node, default_price: float = 1.0) -> float:
    return node.price if (node.price is not None) else default_price

def compute_refuel_plan(
    path: List[str],
    G: nx.DiGraph,
    fuel_capacity: int,
    burn_per_au: float,
    current_fuel: int,
    default_price: float = 1.0,
) -> List[Tuple[str, ...]]:
    """
    Greedy “cheapest-next-within-range” policy along a fixed sequence of stops.
    Returns actions like:
        ("BUY", node_symbol, units_to_buy, price_per_unit)
        ("FLY", a, b, distance_au, fuel_used)
    """
    actions: List[Tuple[str, ...]] = []
    tank = current_fuel
    nodes: Dict[str, Node] = {n: G.nodes[n]["data"] for n in path}

    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        dist = G[a][b]["distance"]
        need = fuel_for_leg(dist, burn_per_au)
        price_a = _price_of(nodes[a], default_price)

        # Look ahead: any cheaper station within single-tank range from 'a'?
        cheaper_ahead = False
        for j in range(i + 1, len(path)):
            u = path[j]
            if G.has_edge(a, u):
                if G[a][u]["distance"] <= (fuel_capacity / burn_per_au):
                    if _price_of(nodes[u], default_price) < price_a:
                        cheaper_ahead = True
                        break

        # Decide how much to buy at 'a'
        if tank < need:
            if cheaper_ahead:
                buy = min(fuel_capacity - tank, need - tank)  # just enough
            else:
                buy = fuel_capacity - tank  # fill up
            if buy > 0:
                actions.append(("BUY", a, str(buy), f"{price_a}"))
                tank += buy

        # Fly a -> b
        actions.append(("FLY", a, b, f"{dist:.3f}", str(need)))
        tank -= need
        tank = max(0, tank)

    return actions


# ----------------------
# High-level one-call
# ----------------------

def plan_route_and_refuel(
    all_nodes: Iterable[Node],
    start_symbol: str,
    goal_symbol: str,
    fuel_capacity: int,
    burn_per_au: float,
    speed_au_per_hr: float,
    current_fuel: int,
    corridor_width: float,
    landing_overhead_hr: float = 0.0,
    non_market_penalty: float = 0.0,
    keep_k_nearest_extra: int = 0,
) -> Dict:
    """
    1) Corridor filter
    2) Build reachability graph using max_range = fuel_capacity / burn_per_au
    3) A* by time (with penalties/overheads in edge weights)
    4) Greedy price-aware refuel plan along the path
    """
    node_map = {n.symbol: n for n in all_nodes}
    if start_symbol not in node_map or goal_symbol not in node_map:
        raise ValueError("start or goal symbol not present in nodes")

    start, goal = node_map[start_symbol], node_map[goal_symbol]
    candidates = build_candidates(
        all_nodes, start, goal, corridor_width, keep_k_nearest_extra=keep_k_nearest_extra
    )

    max_range = fuel_capacity / burn_per_au
    G = build_reachability_graph(
        candidates,
        max_range=max_range,
        speed_au_per_hr=speed_au_per_hr,
        landing_overhead_hr=landing_overhead_hr,
        non_market_penalty=non_market_penalty,
    )

    if start_symbol not in G.nodes or goal_symbol not in G.nodes:
        raise RuntimeError("Start/goal filtered out; widen corridor_width or include explicitly.")

    path = astar_by_time(G, start_symbol, goal_symbol, speed_au_per_hr)
    actions = compute_refuel_plan(
        path=path,
        G=G,
        fuel_capacity=fuel_capacity,
        burn_per_au=burn_per_au,
        current_fuel=current_fuel,
        default_price=1.0,
    )

    total_travel_time = sum(G[a][b]["time"] for a, b in zip(path[:-1], path[1:]))
    total_edges_weight = sum(G[a][b]["weight"] for a, b in zip(path[:-1], path[1:]))

    return {
        "graph": G,
        "path": path,
        "actions": actions,
        "stats": {
            "legs": len(path) - 1,
            "total_travel_time_hr": total_travel_time,
            "objective_weight_sum": total_edges_weight,
            "max_range_au": max_range,
        },
    }

# ----------------------
# Reserve-aware refuel planning (tank + cargo)
# ----------------------

class PlanInfeasibleError(RuntimeError):
    pass

def _sum_fuel_required_between(path: List[str], G: nx.DiGraph, i_start: int, i_end_exclusive: int, burn_per_au: float) -> int:
    """Sum integer fuel for legs path[i] -> path[i+1] for i in [i_start, i_end_exclusive)."""
    total = 0
    for i in range(i_start, i_end_exclusive):
        a, b = path[i], path[i+1]
        dist = G[a][b]["distance"]
        total += fuel_for_leg(dist, burn_per_au)
    return total

def _find_next_market_index(path: List[str], G: nx.DiGraph, start_idx: int) -> int:
    """Return index j (>= start_idx) of the next node on path that has fuel.
    If none, return len(path)-1 (the goal)."""
    for j in range(start_idx, len(path)):
        node = G.nodes[path[j]]["data"]
        if node.has_fuel:
            return j
    return len(path) - 1

def compute_refuel_plan_with_reserve(
    path: List[str],
    G: nx.DiGraph,
    tank_capacity: int,
    cargo_fuel_capacity: int,
    burn_per_au: float,
    current_tank: int,
    current_cargo_fuel: int,
    default_price: float = 1.0,
) -> List[Tuple[str, ...]]:
    """
    Safe plan that guarantees you won't get stranded between markets, provided:
      * each hop distance <= tank_capacity / burn_per_au (already enforced by graph),
      * and the cumulative fuel needed between markets fits in (tank_capacity + cargo_fuel_capacity).

    Emits actions:
      - ("BUY", node, units_to_tank, units_to_cargo, price_per_unit)
      - ("TRANSFER", node, units_from_cargo_to_tank)
      - ("FLY", a, b, distance_au, fuel_used)
    """
    actions: List[Tuple[str, ...]] = []

    tank = int(current_tank)
    cargo = int(current_cargo_fuel)

    # Pre-check per-leg feasibility vs tank_capacity (should already pass)
    for a, b in zip(path[:-1], path[1:]):
        need = fuel_for_leg(G[a][b]["distance"], burn_per_au)
        if need > tank_capacity:
            raise PlanInfeasibleError(
                f"Leg {a}->{b} requires {need} which exceeds tank capacity {tank_capacity}."
            )

    # Walk the path
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        node_a = G.nodes[a]["data"]
        dist_ab = G[a][b]["distance"]
        need_ab = fuel_for_leg(dist_ab, burn_per_au)

        # 1) If we're at a market, ensure coverage until the next market
        if node_a.has_fuel:
            next_market_idx = _find_next_market_index(path, G, i + 1)  # market at/after next node
            # Total fuel needed for legs [i .. next_market_idx-1]
            required_until_next_market = _sum_fuel_required_between(path, G, i, next_market_idx, burn_per_au)

            # hard bound: cannot carry more than tank + cargo capacity
            max_onboard = tank_capacity + cargo_fuel_capacity
            if required_until_next_market > max_onboard:
                raise PlanInfeasibleError(
                    f"From {a}, required fuel until next market is {required_until_next_market}, "
                    f"but max onboard capacity is {max_onboard}. Widen corridor, alter route, or increase capacities."
                )

            total_onboard = tank + cargo
            deficit = max(0, required_until_next_market - total_onboard)
            if deficit > 0:
                # Buy into tank first (up to tank_capacity), then cargo
                price = _price_of(node_a, default_price)
                add_to_tank = min(deficit, tank_capacity - tank)
                tank += add_to_tank
                remaining = deficit - add_to_tank
                add_to_cargo = min(remaining, cargo_fuel_capacity - cargo)
                cargo += add_to_cargo
                if add_to_tank > 0 or add_to_cargo > 0:
                    actions.append(("BUY", a, str(add_to_tank), str(add_to_cargo), f"{price}"))

        # 2) Before flying, top up tank from cargo if needed for the next leg
        if tank < need_ab:
            transfer = min(need_ab - tank, cargo)
            if transfer < (need_ab - tank):
                # Not enough cargo to cover the leg => infeasible
                raise PlanInfeasibleError(
                    f"Insufficient cargo fuel at {a}: need {need_ab}, tank {tank}, cargo {cargo}."
                )
            tank += transfer
            cargo -= transfer
            if transfer > 0:
                actions.append(("TRANSFER", a, str(transfer)))

        # 3) Fly a -> b
        actions.append(("FLY", a, b, f"{dist_ab:.3f}", str(need_ab)))
        tank -= need_ab
        # Safety clamp
        tank = max(0, tank)

    return actions

def plan_route_and_refuel_with_reserve(
    all_nodes: Iterable[Node],
    start_symbol: str,
    goal_symbol: str,
    tank_capacity: int,
    cargo_fuel_capacity: int,
    burn_per_au: float,
    speed_au_per_hr: float,
    current_tank: int,
    current_cargo_fuel: int,
    corridor_width: float,
    landing_overhead_hr: float = 0.0,
    non_market_penalty: float = 0.0,
    keep_k_nearest_extra: int = 0,
    default_price: float = 1.0,
) -> Dict:
    """
    Same as plan_route_and_refuel(), but uses the reserve-aware policy.
    """
    node_map = {n.symbol: n for n in all_nodes}
    if start_symbol not in node_map or goal_symbol not in node_map:
        raise ValueError("start or goal symbol not present in nodes")

    start, goal = node_map[start_symbol], node_map[goal_symbol]
    candidates = build_candidates(
        all_nodes, start, goal, corridor_width, keep_k_nearest_extra=keep_k_nearest_extra
    )

    node_map = {n.symbol: n for n in all_nodes}
    if start_symbol not in node_map or goal_symbol not in node_map:
        raise ValueError("start or goal symbol not present in nodes")

    start, goal = node_map[start_symbol], node_map[goal_symbol]
    candidates = build_candidates(
        all_nodes, start, goal, corridor_width, keep_k_nearest_extra=keep_k_nearest_extra
    )

    max_range = tank_capacity / burn_per_au
    G = build_reachability_graph(
        candidates,
        max_range=max_range,
        speed_au_per_hr=speed_au_per_hr,
        landing_overhead_hr=landing_overhead_hr,
        non_market_penalty=non_market_penalty,
    )

    if start_symbol not in G.nodes or goal_symbol not in G.nodes:
        raise RuntimeError("Start/goal filtered out; widen corridor_width or include explicitly.")

    path = astar_by_time(G, start_symbol, goal_symbol, speed_au_per_hr)
    actions = compute_refuel_plan_with_reserve(
        path=path,
        G=G,
        tank_capacity=tank_capacity,
        cargo_fuel_capacity=cargo_fuel_capacity,
        burn_per_au=burn_per_au,
        current_tank=current_tank,
        current_cargo_fuel=current_cargo_fuel,
        default_price=default_price,
    )

    total_travel_time = sum(G[a][b]["time"] for a, b in zip(path[:-1], path[1:]))
    total_edges_weight = sum(G[a][b]["weight"] for a, b in zip(path[:-1], path[1:]))

    return {
        "graph": G,
        "path": path,
        "actions": actions,
        "stats": {
            "legs": len(path) - 1,
            "total_travel_time_hr": total_travel_time,
            "objective_weight_sum": total_edges_weight,
            "max_range_au": max_range,
            "tank_capacity": tank_capacity,
            "cargo_fuel_capacity": cargo_fuel_capacity,
        },
    }

