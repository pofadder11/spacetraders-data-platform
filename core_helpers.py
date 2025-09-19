# =================================================================================================
# core_helpers.py
# -------------------------------------------------------------------------------------------------
# In-memory state containers + initialization that builds domain objects up-front
# using adapters (no DTOs in runner). Also provides nav/ready helpers that UPDATE the state.
# =================================================================================================
from __future__ import annotations
import sqlite3
import asyncio
import os
import sys
import math
import pandas as pd
from typing import Any, Dict, Iterable, List, Optional, Tuple
from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt

from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.agents_api import AgentsApi
from openapi_client.api.systems_api import SystemsApi

from db.auto_repo_sqlite import snapshot_many, TableSpec, upsert_many
from domain.market_rows import MarketGoodRow, MarketTransactionRow
from domain.waypoint_ref import WaypointRef
from domain.waypoint_trait import WaypointTraitRow
from domain.fleet_state import FleetState
from domain.ships_activity import ShipsActivity

from market_runtime import capture_market_for_waypoint, market_to_db, capture_shipyard_for_waypoint, shipyard_to_db

from adapters.ships_specs_adapter import adapt_ships_specs_from_ship
from adapters.ships_activity_adapter import adapt_ships_activity_from_ship, merge_activity_with_nav
from adapters.waypoint_adapter import adapt_waypoints              # returns List[WaypointRef]
from adapters.waypoint_trait_adapter import adapt_traits_from_waypoint_dtos  # returns List[WaypointTraitRow]

from sdk_runtime_helper import call_sdk, unwrap_data

from runtime_support import (
    fmt_dt,
    now_utc,
    is_in_transit,
    status_value,
    api_get_my_ships,
    api_get_my_agent,
    api_get_ship_nav,
    api_refuel_ship,
    api_orbit_ship,
    api_dock_ship,
    api_navigate_ship,
    api_get_system_waypoints,
)

from refuel_routing import Node

from openapi_client import Configuration, ApiClient

def _load_env_token() -> Optional[str]:
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass
    return os.getenv("BEARER_TOKEN")

def setup_client_from_env() -> ApiClient:
    token = _load_env_token()
    if not token:
        print("[FATAL] Missing BEARER_TOKEN in environment or .env")
        sys.exit(1)
    cfg = Configuration()
    cfg.host = "https://api.spacetraders.io/v2"
    cfg.api_key = {"Authorization": token}
    cfg.api_key_prefix = {"Authorization": "Bearer"}
    cfg.access_token = token
    return ApiClient(cfg)

with setup_client_from_env() as client:
    fleet_api = FleetApi(client)
    agents_api = AgentsApi(client)
    systems_api = SystemsApi(client)

conn = sqlite3.connect("spacetraders.db")


class FleetActivityState:
    """In-memory map of ShipsActivity by symbol; patched via adapters on every API response."""
    def __init__(self, items: Iterable[ShipsActivity]):
        self.by_symbol: Dict[str, ShipsActivity] = {s.symbol: s for s in items if getattr(s, "symbol", None)}

    def get(self, symbol: str) -> Optional[ShipsActivity]:
        return self.by_symbol.get(symbol)

    def upsert(self, item: ShipsActivity) -> None:
        self.by_symbol[item.symbol] = item

    def merge_nav(self, symbol: str, nav_dto: Any) -> ShipsActivity:
        cur = self.get(symbol) or ShipsActivity(symbol=symbol)
        upd = merge_activity_with_nav(cur, nav_dto)
        self.upsert(upd)
        return upd

    def merge_refuel(self, symbol: str, refuel_dto: Any) -> ShipsActivity:
        cur = self.get(symbol) or ShipsActivity(symbol=symbol)
        fuel = getattr(refuel_dto, "fuel", None)
        f_cur = getattr(fuel, "current", None) if fuel else None
        f_cap = getattr(fuel, "capacity", None) if fuel else None
        upd = cur.model_copy(update={
            "fuel_current": f_cur if f_cur is not None else cur.fuel_current,
            "fuel_capacity": f_cap if f_cap is not None else cur.fuel_capacity,
        })
        self.upsert(upd)
        return upd


class WaypointsRefState:
    """In-memory reference of waypoints by symbol."""
    def __init__(self, waypoints: Iterable[Any]):
        self.by_symbol: Dict[str, Any] = {getattr(w, "symbol", None): w for w in waypoints if getattr(w, "symbol", None)}

    def has_trait(self, waypoint_symbol: str, trait_symbol: str) -> bool:
        wp = self.by_symbol.get(waypoint_symbol)
        if not wp:
            return False
        # WaypointRef no longer stores traits; traits live in separate table/state.
        return False


class WaypointTraitsState:
    """Flattened traits per waypoint."""
    def __init__(self, rows: Iterable[Any]):
        self.by_wp: Dict[str, List[Any]] = {}
        for r in rows:
            wp = getattr(r, "waypoint_symbol", None)
            if not wp:
                continue
            self.by_wp.setdefault(wp, []).append(r)

    def has_trait(self, waypoint_symbol: str, trait_symbol: str) -> bool:
        for row in self.by_wp.get(waypoint_symbol, []):
            if getattr(row, "trait_symbol", None) == trait_symbol:
                return True
        return False


class WorldState:
    """Top-level state the runner will use instead of DTOs."""
    def __init__(self, fleet: FleetActivityState, waypoints: WaypointsRefState, traits: WaypointTraitsState, agent_hq: str, agent: str):
        self.fleet = fleet
        self.waypoints = waypoints
        self.traits = traits
        self.agent_hq = agent_hq
        self.agent = agent

    def ensure_activity(self, symbol: str) -> ShipsActivity:
        a = self.activities.get(symbol)
        if a is None:
            a = ShipsActivity(symbol=symbol)
            self.activities[symbol] = a
        return a

    def update_activity_from_nav(self, symbol: str, nav_dto: Any) -> ShipsActivity:
        current = self.ensure_activity(symbol)
        updated = merge_activity_with_nav(current, nav_dto)
        self.activities[symbol] = updated
        return updated

    def update_activity_from_refuel(self, symbol: str, resp_dto: Any) -> ShipsActivity:
        """Use refuel response to update fuel state in local activity."""
        current = self.ensure_activity(symbol)
        fuel_cur = getattr(getattr(resp_dto, "fuel", None), "current", None)
        fuel_cap = getattr(getattr(resp_dto, "fuel", None), "capacity", None)
        patched = current.model_copy(update={
            "fuel_current": fuel_cur if fuel_cur is not None else current.fuel_current,
            "fuel_capacity": fuel_cap if fuel_cap is not None else current.fuel_capacity,
        })
        self.activities[symbol] = patched
        return patched

# -------- initialization (one-time at runner start) ---------------------------
async def init_world_state(fleet_api: FleetApi, agents_api: AgentsApi, systems_api: SystemsApi) -> WorldState:
    # Fleet (activity slice)
    ship_dtos = await api_get_my_ships(fleet_api)
    fleet_acts = [adapt_ships_activity_from_ship(d) for d in ship_dtos]
    fleet_state = FleetActivityState(fleet_acts)

    # Agent HQ + derive system for waypoints
    agent = await api_get_my_agent(agents_api)
    hq_wp = getattr(agent, "headquarters", None)
    if not hq_wp or "-" not in str(hq_wp):
        raise RuntimeError("Agent headquarters missing or malformed.")
    parts = str(hq_wp).split("-")
    system_symbol = "-".join(parts[:2])

    # Waypoints + traits (reference)
    wps_dtos = await api_get_system_waypoints(systems_api, system_symbol)
    waypoints = adapt_waypoints(wps_dtos)
    traits = adapt_traits_from_waypoint_dtos(wps_dtos)
    wp_state = WaypointsRefState(waypoints)
    trait_state = WaypointTraitsState(traits)

    return WorldState(fleet=fleet_state, waypoints=wp_state, traits=trait_state, agent_hq=hq_wp, agent = agent)

#---- check if load_initial_fleet_state is duplicating what world state already does

async def load_initial_fleet_state(fleet: FleetApi) -> FleetState:
    """Load ships once, build local state (activity + specs) and persist to DB."""
    conn = sqlite3.connect("spacetraders.db")
    resp = await call_sdk(fleet, "get_my_ships")
    ships: Iterable[Any] = unwrap_data(resp)
    ships = list(ships)
    if not ships:
        raise SystemExit("[FATAL] No ships returned; check token/agent.")

    activities = [adapt_ships_activity_from_ship(d) for d in ships]
    specs = [adapt_ships_specs_from_ship(d) for d in ships]

    # Persist to DB (idempotent upserts)
    upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), activities)
    upsert_many(conn, TableSpec(table="ships_specs", pk="symbol"), specs)

    # Build local state dicts
    state = FleetState(
        activities={a.symbol: a for a in activities if a.symbol},
        specs={s.symbol: s for s in specs if s.symbol},
    )
    return state


async def load_initial_waypoint_state(
    agents: AgentsApi,
    systems: SystemsApi,
) -> Tuple[List[WaypointRef], List[WaypointTraitRow]]:
    """
    Resolve the agent HQ's system, pull all waypoints in that system,
    adapt to domain rows, and persist to DB (idempotent upserts).
    Returns (waypoint_refs, waypoint_traits).
    """
    conn = sqlite3.connect("spacetraders.db")
    
    # 1) Figure out which system to index from agent HQ
    agent_resp = await call_sdk(agents, "get_my_agent")
    agent = unwrap_data(agent_resp)
    hq_wp = getattr(agent, "headquarters", None)
    if not hq_wp or "-" not in str(hq_wp):
        raise RuntimeError("Agent headquarters missing or malformed, cannot derive system.")
    sys_symbol = "-".join(str(hq_wp).split("-")[:2])  # e.g. "X1-HA25"

    # 2) Pull the system waypoints (DTO list)
    #    NOTE: If your client uses a different method name (e.g. list_system_waypoints),
    #          swap it here. The signature usually takes system_symbol, plus page/limit.
    
    wps_resp = await api_get_system_waypoints(systems, system_symbol=sys_symbol)
    wps_dtos: Iterable[Any] = unwrap_data(wps_resp)

    # 3) Adapt → domain types
    waypoint_refs: List[WaypointRef] = adapt_waypoints(wps_dtos)
    waypoint_traits: List[WaypointTraitRow] = adapt_traits_from_waypoint_dtos(wps_dtos)

    # 4) Persist to DB (idempotent upserts)
    upsert_many(conn, TableSpec(table="waypoint_refs", pk="symbol"), waypoint_refs)

    # If your TableSpec supports composite PKs, use the tuple form below.
    # If not, create a UNIQUE index on (waypoint_symbol, trait_symbol) in schema, and keep pk="id" if you have one.
    upsert_many(conn, TableSpec(table="waypoint_traits", pk=("waypoint_symbol", "trait_symbol")), waypoint_traits)

    conn.commit()
    return waypoint_refs, waypoint_traits

# ---------------------------------- basics ---------------------------------- #
def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _has_marketplace(traits_by_wp: Optional[Dict[str, Iterable[Any]]], waypoint: str) -> bool:
    """Return True if traits_by_wp says this waypoint has a MARKETPLACE trait (if provided)."""
    if not traits_by_wp:
        return True  # don't block capture if you didn't supply traits
    rows = traits_by_wp.get(waypoint) or []
    return any(getattr(r, "trait_symbol", None) == "MARKETPLACE" for r in rows)

async def get_wps_by_trait(traits_list: str, trait: str):

    data = []
    for wp_symbol, rows_list in traits_list.items():
        for row in rows_list:
            if row.trait_symbol == trait:
                x = row.x or 0
                y = row.y or 0
                data.append({"waypoint": wp_symbol, "x": x, "y": y, "distance": math.hypot(x, y)})
    data = pd.DataFrame(data).sort_values("distance", ascending=True).reset_index(drop=True)
    #print (data.to_string(index=False))
    return data

def create_market_indexes(conn: sqlite3.Connection) -> None:
    """Fast once-off helper — safe to call repeatedly."""
    cur = conn.cursor()
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_goods_snap_wp_trade_ts
        ON market_goods_snapshots(waypoint_symbol, trade_symbol, observed_at)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_goods_snap_trade_ts
        ON market_goods_snapshots(trade_symbol, observed_at)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_tx_wp_trade_ts
        ON market_transactions(waypoint_symbol, trade_symbol, timestamp)
    """)
    conn.commit()

# ---------------------- core: capture + persist for waypoint ----------------- #
async def snapshot_market_for_waypoint(
    conn: sqlite3.Connection,
    systems_api: Any,
    waypoint_symbol: str,
    *,
    include_transactions: bool = True,
    observed_at: Optional[datetime] = None,
) -> Dict[str, int]:
    """
    Fetch market for `waypoint_symbol`, snapshot goods (append-only time-series),
    optionally upsert transactions (already have timestamped IDs).
    Returns counts: {"goods_snap": n, "transactions": m}
    """
    rows = await capture_market_for_waypoint(systems_api, waypoint_symbol)

    # Append-only goods snapshots (writes to market_goods_snapshots with composite PK)
    snapshot_many(conn, "market_goods", MarketGoodRow, rows["goods"], observed_at=observed_at)

    # Transactions accumulate naturally (adapter builds unique id with timestamp)
    tx_count = 0
    if include_transactions and rows["transactions"]:
        upsert_many(conn, TableSpec(table="market_transactions", pk="id"), rows["transactions"])
        tx_count = len(rows["transactions"])

    # (Optional) backfill explicit waypoint_symbol on tx table for older rows
    conn.execute("""
        UPDATE market_transactions
           SET waypoint_symbol = substr(id, 1, instr(id, '#') - 1)
         WHERE (waypoint_symbol IS NULL OR waypoint_symbol = '')
           AND instr(id, '#') > 1
    """)
    conn.commit()

    return {"goods_snap": len(rows["goods"]), "transactions": tx_count}

# --------------- convenience: snapshot market for a given ship --------------- #
async def snapshot_market_for_ship_if_market(
    
    conn: sqlite3.Connection,
    systems_api: Any,
    fleet_api: Any,
    ship_symbol: str,
    *,
    traits_by_wp: Optional[Dict[str, Iterable[Any]]] = None,
    include_transactions: bool = True,
    observed_at: Optional[datetime] = None,
    strict_check: bool = False,
) -> Tuple[bool, Optional[str], Dict[str, int]]:
    """
    Look up the ship's *current* waypoint via get_ship_nav, optionally verify it has a MARKETPLACE
    (using traits_by_wp), and snapshot that market. Returns (did_capture, waypoint, counts).

    - If `strict_check=True` and no MARKETPLACE trait is found, it won't call the API.
    - If `strict_check=False` (default), it will attempt capture regardless (useful if traits cache lags).
    """
    nav = await api_get_ship_nav(fleet_api, ship_symbol)
    # Try common locations of the waypoint symbol
    wp = (
        getattr(nav, "waypoint_symbol", None)
        or getattr(getattr(nav, "route", None), "destination", None) and getattr(nav.route.destination, "symbol", None)
        or getattr(getattr(nav, "route", None), "origin", None) and getattr(nav.route.origin, "symbol", None)
    )

    if not isinstance(wp, str) or not wp:
        return (False, None, {"goods_snap": 0, "transactions": 0})

    if strict_check and not _has_marketplace(traits_by_wp, wp):
        # bail out early if you require an explicit MARKETPLACE trait
        return (False, wp, {"goods_snap": 0, "transactions": 0})

    counts = await snapshot_market_for_waypoint(
        conn,
        systems_api,
        wp,
        include_transactions=include_transactions,
        observed_at=observed_at,
    )
    return (True, wp, counts)


# ---------- sort market waypoints in a logical travel order ----------

"""
market_route_svg.py
- Build a visit-all-markets route starting at a chosen waypoint
- Save an SVG showing:
    • all waypoints (green)
    • start waypoint (blue)
    • lines drawn in the visiting order

Requirements:
    pip install numpy pandas matplotlib
"""
# ----------------------------
# Core TSP-lite helpers
# ----------------------------

def _euclid(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    dx, dy = a[0] - b[0], a[1] - b[1]
    return math.hypot(dx, dy)

def _pairwise_dist_matrix(coords: np.ndarray) -> np.ndarray:
    # coords: (N,2) -> (N,N) distances
    diff = coords[:, None, :] - coords[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=2))

def _nearest_neighbor_tour(D: np.ndarray, start_idx: int) -> List[int]:
    n = D.shape[0]
    unvisited = set(range(n))
    tour = [start_idx]
    unvisited.remove(start_idx)
    cur = start_idx
    while unvisited:
        nxt = min(unvisited, key=lambda j: D[cur, j])
        tour.append(nxt)
        unvisited.remove(nxt)
        cur = nxt
    return tour

def _two_opt_once(tour: List[int], D: np.ndarray) -> Tuple[List[int], bool]:
    """Single 2-opt improvement pass on a *path* (not necessarily a closed tour)."""
    n = len(tour)
    best = tour[:]
    improved = False
    # Evaluate path length segments (no wrap-around)
    def seg_len(i1, i2):
        a, b = best[i1], best[i1 + 1]
        c, d = best[i2], best[i2 + 1]
        return D[a, b] + D[c, d]
    for i in range(0, n - 3):
        for k in range(i + 2, n - 1):
            before = seg_len(i, k)
            after = D[best[i], best[k]] + D[best[i + 1], best[k + 1]]
            if after + 1e-12 < before:
                best = best[: i + 1] + list(reversed(best[i + 1 : k + 1])) + best[k + 1 :]
                improved = True
    return best, improved

def _two_opt(tour: List[int], D: np.ndarray, max_iters: int = 50) -> List[int]:
    cur = tour[:]
    for _ in range(max_iters):
        cur, improved = _two_opt_once(cur, D)
        if not improved:
            break
    return cur

def _rotate_to_start(tour: List[int], want_first: int) -> List[int]:
    """Rotate the order so that want_first appears at index 0 (preserves relative order)."""
    i = tour.index(want_first)
    return tour[i:] + tour[:i]

def all_wp_visitor(
    df: pd.DataFrame,
    start_waypoint: Optional[str] = None,
    return_to_start: bool = False,
    improve_2opt: bool = True,
    fix_start_anchor: bool = True,
) -> pd.DataFrame:
    """
    Build a route that visits all markets.

    df: DataFrame with columns ['waypoint', 'x', 'y']
    start_waypoint: waypoint symbol to start at (required for your use case).
    return_to_start: if True, append the start at the end (closed loop).
    improve_2opt: apply 2-opt local improvement to reduce total path length.
    fix_start_anchor: re-anchor start waypoint at index 0 after 2-opt (keeps your chosen start in front).

    Returns a DataFrame ordered by visit, with leg and cumulative distances.
    """
    if df.empty:
        return pd.DataFrame(columns=["visit_idx", "waypoint", "x", "y", "leg_distance", "cumulative_distance"])

    for col in ["waypoint", "x", "y"]:
        if col not in df.columns:
            raise ValueError(f"markets_df must contain column '{col}'")

    df = df[["waypoint", "x", "y"]].copy().reset_index(drop=True)
    coords = df[["x", "y"]].to_numpy(dtype=float)
    D = _pairwise_dist_matrix(coords)

    if start_waypoint is None:
        raise ValueError("Please provide start_waypoint for anchored plotting.")

    if start_waypoint not in set(df["waypoint"]):
        raise ValueError(f"start_waypoint '{start_waypoint}' not found in markets_df['waypoint']")

    start_idx = int(df.index[df["waypoint"] == start_waypoint][0])

    # Initial heuristic tour
    tour = _nearest_neighbor_tour(D, start_idx)

    # Optional improvement
    if improve_2opt and len(tour) >= 4:
        tour = _two_opt(tour, D)

    # Ensure the chosen start stays first (2-opt can rotate endpoints)
    if fix_start_anchor:
        tour = _rotate_to_start(tour, start_idx)

    # Optionally close the loop
    sequence = tour + ([tour[0]] if return_to_start else [])

    # Distances
    legs = [0.0]
    cum = [0.0]
    for i in range(1, len(sequence)):
        a, b = sequence[i - 1], sequence[i]
        dist = D[a, b]
        legs.append(dist)
        cum.append(cum[-1] + dist)

    out = df.iloc[sequence].reset_index(drop=True)
    out.insert(0, "visit_idx", range(len(sequence)))
    out["leg_distance"] = np.round(legs, 3)
    out["cumulative_distance"] = np.round(cum, 3)
    return out

def plot_route_svg(
    markets_df: pd.DataFrame,
    route_df: pd.DataFrame,
    start_waypoint: str,
    svg_path: str = "markets_route.svg",
    point_size: float = 40.0,
    line_width: float = 1.5,
    annotate_labels: bool = True,
):
    
    # ----------------------------
    # SVG plotting for visual route assessment
    # ----------------------------
    """
    Save an SVG that shows:
      - all waypoints (green)
      - start waypoint (blue)
      - lines between waypoints in visiting order
    """
    # Prepare data
    xy_all = markets_df[["x", "y"]].to_numpy(float)
    wp_all = markets_df["waypoint"].astype(str).tolist()

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Lines for visiting order
    xs = route_df["x"].to_numpy(float)
    ys = route_df["y"].to_numpy(float)
    ax.plot(xs, ys, linewidth=line_width, alpha=0.9)

    # Scatter all markets (green)
    ax.scatter(xy_all[:, 0], xy_all[:, 1], s=point_size, c="green")

    # Highlight start (blue) on top
    if start_waypoint not in wp_all:
        raise ValueError(f"start_waypoint '{start_waypoint}' not found in markets_df['waypoint']")
    start_row = markets_df.loc[markets_df["waypoint"] == start_waypoint].iloc[0]
    ax.scatter([float(start_row["x"])], [float(start_row["y"])], s=point_size * 1.4, c="blue")

    if annotate_labels:
        # Label every market
        for wp, (x, y) in zip(wp_all, xy_all):
            ax.annotate(str(wp), (x, y), xytext=(5, 5), textcoords="offset points", fontsize=8)
        # Add visit indices along the route
        for i, row in route_df.iterrows():
            ax.annotate(f"{int(row['visit_idx'])}", (row["x"], row["y"]), xytext=(0, -12),
                        textcoords="offset points", fontsize=8)

    ax.set_aspect("equal")
    ax.set_title("All-Market Visitor — Anchored Start, Route Lines")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(svg_path, format="svg")
    print(f"Saved SVG -> {svg_path}")

async def patrol_markets(ship_symbol: str, markets_df) -> None:
    # dedupe and coerce to plain list of strings
    waypoints: List[str] = list(dict.fromkeys(markets_df["waypoint"].astype(str).tolist()))
    print(waypoints)
    if not waypoints:
        print("[WARN] No waypoints to patrol.")
        return

    print(f"[PATROL] {ship_symbol} looping through {len(waypoints)} markets.")
    idx = 0
    while True:
        wp = waypoints[idx]
        try:
            print(f"[PATROL] -> Navigating to {wp} (#{idx+1}/{len(waypoints)})")
            nav_resp = await api_navigate_ship(fleet_api, ship_symbol, wp)
            print(f"[MARKET] Capturing {wp} …")
            await market_to_db(wp)
            await asyncio.sleep(1.0)  # small dwell

        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[ERR] Patrol step at {wp} failed: {e!r}")
            await asyncio.sleep(3.0)  # brief backoff

        # round-robin
        idx = (idx + 1) % len(waypoints)

async def patrol_shipyards(ship_symbol: str, shipyards_df) -> None:
    # dedupe and coerce to plain list of strings
    waypoints: List[str] = list(dict.fromkeys(shipyards_df["waypoint"].astype(str).tolist()))
    print(waypoints)
    if not waypoints:
        print("[WARN] No waypoints to patrol.")
        return

    print(f"[PATROL] {ship_symbol} looping through {len(waypoints)} shipyards.")
    idx = 0
    while True:
        wp = waypoints[idx]
        try:
            print(f"[PATROL] -> Navigating to {wp} (#{idx+1}/{len(waypoints)})")
            nav_resp = await api_navigate_ship(fleet_api, ship_symbol, wp)
            print(f"[Shipyard] Capturing {wp} …")
            await shipyard_to_db(wp)
            await asyncio.sleep(1.0)  # small dwell

        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[ERR] Patrol step at {wp} failed: {e!r}")
            await asyncio.sleep(3.0)  # brief backoff

        # round-robin
        idx = (idx + 1) % len(waypoints)

def build_nodes_from_traits_dict(
    traits_dict: Dict[str, List[WaypointTraitRow]],
    fuel_price_lookup: Dict[str, float] = None,
) -> List[Node]:
    """
    Convert a dict of {waypoint_symbol: [WaypointTraitRow, ...]} into Node objects.

    Args:
        traits_dict: mapping from waypoint_symbol -> list of WaypointTraitRow.
        fuel_price_lookup: optional {waypoint_symbol: price} for refining
                           Node.price (default None).

    Returns:
        List[Node]
    """
    nodes: List[Node] = []

    for symbol, trait_rows in traits_dict.items():
        if not trait_rows:
            continue  # skip empty

        # all rows for this waypoint share x,y,type
        first = trait_rows[0]
        x, y = float(first.x), float(first.y)

        # check if any trait is a MARKETPLACE
        has_marketplace = any(tr.trait_symbol == "MARKETPLACE" for tr in trait_rows)

        # build Node
        node = Node(
            symbol=symbol,
            x=x,
            y=y,
            has_fuel=has_marketplace,
            price=(fuel_price_lookup.get(symbol) if fuel_price_lookup else None),
        )
        nodes.append(node)

    return nodes