#!/usr/bin/env python3
"""
demo_refuel_routing_viz.py
Generate a fictional map + ship, plan a fuel-safe route inside a corridor,
and render the corridor, candidate stops, and chosen path.
Also prints the BUY/FLY steps to the console and saves a PNG.

Requirements:
    pip install networkx matplotlib

Usage:
    python demo_refuel_routing_viz.py
"""
import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# If refuel_routing.py is in the same folder, this import will work.
# Otherwise, adjust sys.path or paste the module contents here.
from refuel_routing import (
    Node,
    build_candidates,
    build_reachability_graph,
    astar_by_time,
    compute_refuel_plan,
    corridor_polygon,
    plan_route_and_refuel,
)


# ----------------------
# Fictional world
# ----------------------

def make_demo_world(seed=13):
    random.seed(seed)
    S = Node("S", 0.0, 0.0, has_fuel=True, price=8.0)
    T = Node("T", 42.0, 8.0, has_fuel=True, price=10.0)
    waypoints = [S, T]

    # Points roughly along S->T with jitter; ~20 extra waypoints
    for i in range(1, 22):
        t = i / 22.0
        x = (1 - t) * S.x + t * T.x
        y = (1 - t) * S.y + t * T.y
        x += random.uniform(-3.0, 3.0)
        y += random.uniform(-2.0, 2.0)
        has_fuel = random.random() < 0.65
        price = round(random.uniform(5.5, 11.5), 2) if has_fuel else None
        symbol = f"W{i:02d}"
        waypoints.append(Node(symbol, x, y, has_fuel, price))

    return waypoints, S, T


# ----------------------
# Main
# ----------------------

def main():
    # Ship & planner config (tweak freely)
    fuel_capacity = 24        # units
    burn_per_au = 1.8         # units per AU
    speed_au_per_hr = 3.0     # AU/hour
    current_fuel = 5          # starting fuel units
    corridor_width = 3.2      # AU (half-width of band around S->T)
    landing_overhead_hr = 0.05
    non_market_penalty = 0.03
    keep_k_nearest_extra = 3  # add a few out-of-corridor wildcards

    nodes, S, T = make_demo_world(seed=13)

    # Full plan (graph + path + actions)
    plan = plan_route_and_refuel(
        all_nodes=nodes,
        start_symbol=S.symbol,
        goal_symbol=T.symbol,
        fuel_capacity=fuel_capacity,
        burn_per_au=burn_per_au,
        speed_au_per_hr=speed_au_per_hr,
        current_fuel=current_fuel,
        corridor_width=corridor_width,
        landing_overhead_hr=landing_overhead_hr,
        non_market_penalty=non_market_penalty,
        keep_k_nearest_extra=keep_k_nearest_extra,
    )

    G = plan["graph"]
    path = plan["path"]
    actions = plan["actions"]

    # ----- Print a readable action log -----
    print("\n=== Route ===")
    print(" -> ".join(path))
    print("\n=== Actions (BUY/FLY) ===")
    step = 1
    for act in actions:
        if act[0] == "BUY":
            _, at, units, price = act
            print(f"{step:02d}. BUY at {at:<4}  +{units} fuel @ {price}/u")
        else:
            _, a, b, dist, need = act
            print(f"{step:02d}. FLY {a:>4} -> {b:<4}  {float(dist):5.2f} AU  (use {need} fuel)")
        step += 1

    # ----- Visualization -----
    fig, ax = plt.subplots(figsize=(9, 6))

    # Corridor band
    poly_pts = corridor_polygon(S.x, S.y, T.x, T.y, half_width=corridor_width)
    ax.add_patch(Polygon(poly_pts, alpha=0.15))

    # Candidate nodes
    for n in G.nodes:
        nd = G.nodes[n]["data"]
        marker = "o" if nd.has_fuel else "x"  # circle = market, x = non-market
        ax.scatter([nd.x], [nd.y], marker=marker)
        ax.annotate(nd.symbol, (nd.x, nd.y), xytext=(4, 4), textcoords="offset points", fontsize=8)

    # Path polyline with step indices
    xs = [G.nodes[s]["data"].x for s in path]
    ys = [G.nodes[s]["data"].y for s in path]
    ax.plot(xs, ys, linewidth=2)
    for i, sym in enumerate(path):
        nd = G.nodes[sym]["data"]
        ax.annotate(f"{i}", (nd.x, nd.y), xytext=(0, -12), textcoords="offset points", fontsize=8)

    # Labels
    ax.annotate("START", (S.x, S.y), xytext=(10, -10), textcoords="offset points", fontsize=9)
    ax.annotate("TARGET", (T.x, T.y), xytext=(10, -10), textcoords="offset points", fontsize=9)

    ax.set_title("Refueling-Constrained Route with Corridor Filter (Demo)")
    ax.set_xlabel("X (AU)")
    ax.set_ylabel("Y (AU)")
    ax.set_aspect("equal")
    ax.grid(True)
    plt.tight_layout()

    # Save PNG and show
    out_path = "refuel_routing_demo.png"
    plt.savefig(out_path, dpi=150)
    print(f"\nSaved plot -> {out_path}")
    plt.show()


if __name__ == "__main__":
    main()
