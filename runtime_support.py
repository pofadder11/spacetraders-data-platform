# =================================================================================================
# runtime_support.py
# -------------------------------------------------------------------------------------------------
# Infra/shared helpers: client factory, async bridge, unwrap, enum normalization, safe API calls.
# Keeps I/O and SDK quirks out of your business logic & adapters.
# =================================================================================================
from __future__ import annotations

import asyncio
import inspect
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional, Dict, Iterable

# Domain + adapters
from domain.ships_activity import ShipsActivity
from domain.market_rows import MarketGoodRow
from adapters.ships_activity_adapter import (
    adapt_ships_activity_from_ship,
    merge_activity_with_nav,
)

from openapi_client import Configuration, ApiClient

# Generated APIs
from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.agents_api import AgentsApi
from openapi_client.api.systems_api import SystemsApi

from services.journeys_writer import append_journey_from_nav
from datetime import datetime, timezone

import sqlite3

conn = sqlite3.connect("spacetraders.db")


# ---------- env + client ------------------------------------------------------
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

# ---------- async bridge + unwrap ---------------------------------------------
async def call_sdk(api_obj: Any, method_name: str, *args, **kwargs) -> Any:
    fn = getattr(api_obj, method_name)
    if inspect.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))

def unwrap_data(resp: Any) -> Any:
    return getattr(resp, "data", resp)

# ---------- small utils -------------------------------------------------------
def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def fmt_dt(dt: Optional[datetime]) -> str:
    if not dt:
        return "None"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")

def status_value(enum_like: Any) -> str:
    """Normalize enums/strings to raw value name, e.g. 'IN_TRANSIT'."""
    if enum_like is None:
        return ""
    val = getattr(enum_like, "value", None)
    if isinstance(val, str):
        return val
    name = getattr(enum_like, "name", None)
    if isinstance(name, str):
        return name
    s = str(enum_like)
    if "." in s:
        s = s.split(".")[-1]
    return s

def is_in_transit(nav_like: Any) -> bool:
    return status_value(getattr(nav_like, "status", None)) == "IN_TRANSIT"

# -------------------- request builds ------------------------------

def build_purchase_cargo_request(cargo_symbol: str, units: int) -> Any:
    try:
        from openapi_client.models.purchase_cargo_request import PurchaseCargoRequest  # type: ignore
        return PurchaseCargoRequest(cargo_symbol=cargo_symbol, units=units)
    except Exception:
        return {"symbol": cargo_symbol, "units": units}
    
def build_sell_cargo_request(cargo_symbol: str, units: int) -> Any:
    try:
        from openapi_client.models.sell_cargo_request import SellCargoRequest  # type: ignore
        return SellCargoRequest(cargo_symbol=cargo_symbol, units=units)
    except Exception:
        return {"symbol": cargo_symbol, "units": units}
    
def build_nav_request(waypoint_symbol: str) -> Any:
    try:
        from openapi_client.models.navigate_ship_request import NavigateShipRequest  # type: ignore
        return NavigateShipRequest(waypoint_symbol=waypoint_symbol)
    except Exception:
        return {"waypoint_symbol": waypoint_symbol, "waypointSymbol": waypoint_symbol}

# ---------- safe API call wrappers (hide SDK differences) ---------------------
async def api_get_my_ships(fleet_api) -> list[Any]:
    resp = await call_sdk(fleet_api, "get_my_ships")
    data = unwrap_data(resp)
    return list(data) if isinstance(data, (list, tuple)) else list(data or [])

async def api_get_ship_nav(fleet_api, ship_symbol: str) -> Any:
    resp = await call_sdk(fleet_api, "get_ship_nav", ship_symbol=ship_symbol)
    return unwrap_data(resp)

async def api_get_my_agent(agents_api) -> Any:
    resp = await call_sdk(agents_api, "get_my_agent")
    return unwrap_data(resp)

async def api_refuel_ship(fleet_api, ship_symbol: str) -> Optional[Any]:
    try:
        resp = await call_sdk(fleet_api, "refuel_ship", ship_symbol=ship_symbol, refuel_ship_request={})
        return unwrap_data(resp)
    except TypeError:
        try:
            resp = await call_sdk(fleet_api, "refuel_ship", ship_symbol=ship_symbol, body={})
            return unwrap_data(resp)
        except Exception:
            return None
    except Exception:
        return None

async def api_orbit_ship(fleet_api, ship_symbol: str) -> None:
    await call_sdk(fleet_api, "orbit_ship", ship_symbol=ship_symbol)

async def api_dock_ship(fleet_api, ship_symbol: str) -> None:
    await call_sdk(fleet_api, "dock_ship", ship_symbol=ship_symbol)

async def api_navigate_ship(fleet_api, ship_symbol: str, waypoint_symbol: str) -> Any:
    print("starting navigation...")
    ready = await nav_prep(fleet_api, ship_symbol=ship_symbol, waypoint_symbol=waypoint_symbol)
    print("Prep complete")
    if not ready:
        print("[SKIP] Navigation aborted, already at destination")
        return None  # stop here
    req = build_nav_request(waypoint_symbol)
    resp = await call_sdk(fleet_api, "navigate_ship", ship_symbol=ship_symbol, navigate_ship_request=req)
    
    resp2 = unwrap_data(resp)
    # extract a nav DTO from the response (supporting both shapes)
    nav_dto = getattr(resp2, "nav", resp2)
    # 1) append a journey row (append-only)
    append_journey_from_nav(
        ship_symbol,
        nav_dto,
        ship_dto_for_counters=getattr(resp2, "nav", None) and resp2 or None,
        observed_at=datetime.now(timezone.utc),
    )
    print(ship_symbol, " has taken off and is in transit")

    # wait for arrival before performing next action
    ships_activity_obj = await build_fleet_object(fleet_api)
    act = ships_activity_obj.get(ship_symbol)
    now = datetime.now(timezone.utc)
    secs_to_arrival = (act.arr_time - now).total_seconds()
    print("Seconds until arrival:", secs_to_arrival)
    await asyncio.sleep(secs_to_arrival + 2)
    print("Arrived and ready")
    # wait complete

    return unwrap_data(resp)

async def api_purchase_cargo(fleet_api, ship_symbol:str, waypoint_symbol: str, cargo_symbol:str, units: int):
    req = build_purchase_cargo_request(cargo_symbol=cargo_symbol, units=units)
    resp = await call_sdk(fleet_api, "purchase_cargo", ship_symbol=ship_symbol , purchase_cargo_request = req)
    await market_to_db(waypoint = waypoint_symbol)

    return unwrap_data(resp)

async def api_sell_cargo(fleet_api, ship_symbol:str, waypoint_symbol: str, cargo_symbol:str, units: int):
    req = build_sell_cargo_request(cargo_symbol=cargo_symbol, units=units)
    resp = await call_sdk(fleet_api, "sell_cargo", ship_symbol=ship_symbol , sell_cargo_request = req)
    await market_to_db(waypoint = waypoint_symbol)

    return unwrap_data(resp)

async def api_get_system_waypoints(systems_api, system_symbol: str) -> list[Any]:
    """Handle clients with/without page/limit."""
    all_dtos: list[Any] = []
    page, limit = 1, 20
    while True:
        try:
            resp = await call_sdk(systems_api, "get_system_waypoints", system_symbol=system_symbol, page=page, limit=limit)
            data = unwrap_data(resp)
        except TypeError:
            resp = await call_sdk(systems_api, "get_system_waypoints", system_symbol=system_symbol)
            data = unwrap_data(resp)

        if data is None:
            break
        if isinstance(data, (list, tuple)):
            batch = list(data)
        else:
            batch = list(getattr(data, "data", None) or getattr(data, "waypoints", []) or [])
        all_dtos.extend(batch)
        if not batch or len(batch) < limit:
            break
        page += 1
    return all_dtos

async def nav_prep(fleet_api, ship_symbol: str, waypoint_symbol: str) -> bool:
    ships_activity_obj = await build_fleet_object(fleet_api)
    act = ships_activity_obj.get(ship_symbol)

    # already at destination → stop
    if act.destination_waypoint == waypoint_symbol:
        print("Ship is already at the destination")
        return False
    else:
        print("Not at destination, continuing")

    if act.transit_check:
        now = datetime.now(timezone.utc)
        secs_to_arrival = (act.arr_time - now).total_seconds()
        print("Seconds until arrival:", secs_to_arrival)
        await asyncio.sleep(secs_to_arrival + 2)
        print("Arrived and ready")
        update = await build_fleet_object(fleet_api)
        new_status = update.get(act.symbol).status
        act.status = new_status
        print("After arriving, the status of", act.symbol, "is", act.status)

    if act.refuel_check:
        print("Refuelling now...")
        await api_dock_ship(fleet_api, act.symbol)
        act.status = "DOCKED"
        await asyncio.sleep(2)
        await api_refuel_ship(fleet_api, act.symbol)

    if not act.in_orbit_check:
        print("Not in orbit, going into orbit now...")
        await api_orbit_ship(fleet_api, act.symbol)
        await asyncio.sleep(2)

    return True   # ready to navigate

async def build_fleet_object(fleet_api: FleetApi) -> FleetObject:
    """Call get_my_ships() once and adapt to domain for logic checks."""
    resp = await call_sdk(fleet_api, "get_my_ships")
    dtos: Iterable[Any] = unwrap_data(resp)
    adapted = [adapt_ships_activity_from_ship(d) for d in dtos]
    print(f"[BOOT] Adapted {len(adapted)} ships into fleet_object")
    return FleetObject(adapted)

# -------------------------- local state (in-memory) ---------------------------
class FleetObject:
    """Lightweight in-memory store for adapted ShipsActivity objects."""
    def __init__(self, ships: Iterable[ShipsActivity]):
        self.by_symbol: Dict[str, ShipsActivity] = {s.symbol: s for s in ships if s.symbol}

    def get(self, symbol: str) -> ShipsActivity | None:
        return self.by_symbol.get(symbol)

    def upsert(self, obj: ShipsActivity) -> None:
        self.by_symbol[obj.symbol] = obj

    def update_from_nav(self, symbol: str, nav_dto: Any) -> ShipsActivity:
        current = self.get(symbol) or ShipsActivity(symbol=symbol)
        updated = merge_activity_with_nav(current, nav_dto)
        self.upsert(updated)
        return updated

    def update_from_refuel(self, symbol: str, refuel_dto: Any) -> ShipsActivity:
        """Patch fuel from a refuel response DTO (fuel.current/capacity)."""
        cur = self.get(symbol) or ShipsActivity(symbol=symbol)
        fuel = getattr(refuel_dto, "fuel", None)
        f_cur = getattr(fuel, "current", None) if fuel else None
        f_cap = getattr(fuel, "capacity", None) if fuel else None
        patched = cur.model_copy(update={
            "fuel_current": f_cur if f_cur is not None else cur.fuel_current,
            "fuel_capacity": f_cap if f_cap is not None else cur.fuel_capacity,
        })
        self.upsert(patched)
        return patched

# ---------------------------- bootstrap ---------------------------------------
async def get_agent_hq_waypoint(agents: AgentsApi) -> str:
    resp = await call_sdk(agents, "get_my_agent")
    agent = unwrap_data(resp)
    hq_wp = getattr(agent, "headquarters", None)
    if not hq_wp or not isinstance(hq_wp, str):
        raise RuntimeError("Agent headquarters not found")
    print(f"[INFO] Agent HQ waypoint: {hq_wp}")
    return hq_wp