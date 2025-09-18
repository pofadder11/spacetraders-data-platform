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
from typing import Any, Dict, Iterable, List, Optional, Tuple
from datetime import datetime, timezone

from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.agents_api import AgentsApi
from openapi_client.api.systems_api import SystemsApi

from db.auto_repo_sqlite import snapshot_many, TableSpec, upsert_many
from domain.market_rows import MarketGoodRow, MarketTransactionRow
from domain.waypoint_ref import WaypointRef
from domain.waypoint_trait import WaypointTraitRow
from domain.fleet_state import FleetState
from domain.ships_activity import ShipsActivity

from market_runtime import capture_market_for_waypoint

from adapters.ships_specs_adapter import adapt_ships_specs_from_ship
from adapters.ships_activity_adapter import adapt_ships_activity_from_ship, merge_activity_with_nav
from adapters.waypoint_adapter import adapt_waypoints              # returns List[WaypointRef]
from adapters.waypoint_trait_adapter import adapt_traits_from_waypoint_dtos  # returns List[WaypointTraitRow]

from runtime_support import (
    call_sdk,
    unwrap_data,
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


async def market_to_db(waypoint: str) -> None:
    # Fetch first (network I/O), then write to DB (short-lived connection)
    rows = await capture_market_for_waypoint(systems_api, waypoint)
    with sqlite3.connect("spacetraders.db") as conn:
        snapshot_many(conn, "market_goods", MarketGoodRow, rows["goods"])  # append-only history
        if rows["transactions"]:
            upsert_many(conn, TableSpec(table="market_transactions", pk="id"), rows["transactions"])


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
