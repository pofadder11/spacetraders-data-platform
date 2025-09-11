#!/usr/bin/env python3
# tester_fleet_object_nav.py
# Rewrite: use the *adapted* fleet_object (ShipsActivity) for all logic checks.
# - Build fleet_object from get_my_ships() via adapters
# - Use ShipsActivity fields (fuel_level/status/current_waypoint) for decisions
# - When API calls mutate state (nav/refuel/orbit), merge the results back into fleet_object

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

# Infra helpers (no DTOs leak into logic)
from runtime_support import setup_client_from_env, maybe_await, unwrap_data  # type: ignore

# Generated APIs
from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.agents_api import AgentsApi

# Domain + adapters
from domain.ships_activity import ShipsActivity
from adapters.ships_activity_adapter import (
    adapt_ships_activity_from_ship,
    merge_activity_with_nav,
)

# ----------------------------- util -------------------------------------------
def _fmt_dt(dt: Optional[datetime]) -> str:
    if not dt:
        return "None"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")

def _status_value(status_obj: Any) -> str:
    if status_obj is None:
        return ""
    val = getattr(status_obj, "value", None)
    if isinstance(val, str):
        return val
    name = getattr(status_obj, "name", None)
    if isinstance(name, str):
        return name
    s = str(status_obj)
    if "." in s:
        s = s.split(".")[-1]
    return s

def _is_in_transit_status(status_obj: Any) -> bool:
    return _status_value(status_obj) == "IN_TRANSIT"

def _build_nav_request(waypoint_symbol: str) -> Any:
    try:
        from openapi_client.models.navigate_ship_request import NavigateShipRequest  # type: ignore
        return NavigateShipRequest(waypoint_symbol=waypoint_symbol)
    except Exception:
        return {"waypoint_symbol": waypoint_symbol, "waypointSymbol": waypoint_symbol}

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
async def build_fleet_object(fleet_api: FleetApi) -> FleetObject:
    """Call get_my_ships() once and adapt to domain for logic checks."""
    resp = await maybe_await(fleet_api, "get_my_ships")
    dtos: Iterable[Any] = unwrap_data(resp)
    adapted = [adapt_ships_activity_from_ship(d) for d in dtos]
    print(f"[BOOT] Adapted {len(adapted)} ships into fleet_object")
    return FleetObject(adapted)

async def get_agent_hq_waypoint(agents: AgentsApi) -> str:
    resp = await maybe_await(agents, "get_my_agent")
    agent = unwrap_data(resp)
    hq_wp = getattr(agent, "headquarters", None)
    if not hq_wp or not isinstance(hq_wp, str):
        raise RuntimeError("Agent headquarters not found")
    print(f"[INFO] Agent HQ waypoint: {hq_wp}")
    return hq_wp

# ------------------------------ waiters ---------------------------------------
async def wait_while_in_transit(fleet_api: FleetApi, fleet_obj: FleetObject, ship_symbol: str) -> None:
    """Poll nav until not IN_TRANSIT; keep fleet_obj synced from nav."""
    while True:
        nav_resp = await maybe_await(fleet_api, "get_ship_nav", ship_symbol=ship_symbol)
        nav = unwrap_data(nav_resp)
        updated = fleet_obj.update_from_nav(ship_symbol, nav)
        if not _is_in_transit_status(updated.status):
            return
        arrival = getattr(getattr(nav, "route", None), "arrival", None)
        print(f"[WAIT] {ship_symbol} in transit; arrival {_fmt_dt(arrival)}")
        now = datetime.now(timezone.utc)
        if arrival and arrival.tzinfo is None:
            arrival = arrival.replace(tzinfo=timezone.utc)
        if arrival:
            secs = (arrival - now).total_seconds()
            await asyncio.sleep(max(secs, 0) + 1.0)
        else:
            await asyncio.sleep(2.0)

# --------------------------- prep & navigate ----------------------------------
async def ensure_ready_to_navigate(
    fleet_api: FleetApi,
    fleet_obj: FleetObject,
    ship_symbol: str,
    target_waypoint: str,
) -> None:
    """Use fleet_obj only for decisions; sync from nav/refuel responses."""
    # 1) Get latest nav and merge to fleet_obj
    nav_resp = await maybe_await(fleet_api, "get_ship_nav", ship_symbol=ship_symbol)
    nav_dto = unwrap_data(nav_resp)
    act = fleet_obj.update_from_nav(ship_symbol, nav_dto)
    print(f"[SNAP] {ship_symbol}: status={act.status}, wp={act.current_waypoint}, fuel_level={act.fuel_level}")

    # Already there and not in transit?
    if act.current_waypoint == target_waypoint and not _is_in_transit_status(act.status):
        print(f"[INFO] {ship_symbol} already at {target_waypoint} — no nav needed.")
        return

    # If in transit, wait
    if _is_in_transit_status(act.status):
        print(f"[INFO] {ship_symbol} IN_TRANSIT → waiting for arrival...")
        await wait_while_in_transit(fleet_api, fleet_obj, ship_symbol)
        act = fleet_obj.get(ship_symbol)  # refreshed by waiter

    # Fuel check via domain property
    needs_fuel = (act.fuel_level is None) or (act.fuel_level < 1.0)
    print(f"[CHECK] fuel_level={act.fuel_level} → needs_refuel={needs_fuel}")
    if needs_fuel:
        # Dock
        print(f"[ACTION] dock_ship({ship_symbol})")
        try:
            await maybe_await(fleet_api, "dock_ship", ship_symbol=ship_symbol)
        except Exception as e:
            print(f"[WARN] dock_ship failed: {e}")

        # Refuel (empty JSON body to avoid 422)
        print(f"[ACTION] refuel_ship({ship_symbol})")
        refuel_resp = None
        try:
            refuel_resp = await maybe_await(
                fleet_api, "refuel_ship", ship_symbol=ship_symbol, refuel_ship_request={}
            )
        except TypeError:
            try:
                refuel_resp = await maybe_await(
                    fleet_api, "refuel_ship", ship_symbol=ship_symbol, body={}
                )
            except Exception as e:
                print(f"[WARN] refuel_ship failed: {e}")
        except Exception as e:
            print(f"[WARN] refuel_ship failed: {e}")

        if refuel_resp is not None:
            fleet_obj.update_from_refuel(ship_symbol, unwrap_data(refuel_resp))
            print(f"[SNAP] post-refuel fuel_level={fleet_obj.get(ship_symbol).fuel_level}")

        # Orbit back (if not in transit)
        nav_chk = unwrap_data(await maybe_await(fleet_api, "get_ship_nav", ship_symbol=ship_symbol))
        act = fleet_obj.update_from_nav(ship_symbol, nav_chk)
        if not _is_in_transit_status(act.status):
            print(f"[ACTION] orbit_ship({ship_symbol})")
            try:
                await maybe_await(fleet_api, "orbit_ship", ship_symbol=ship_symbol)
                # refresh activity after orbit
                nav_chk2 = unwrap_data(await maybe_await(fleet_api, "get_ship_nav", ship_symbol=ship_symbol))
                fleet_obj.update_from_nav(ship_symbol, nav_chk2)
            except Exception as e:
                print(f"[WARN] orbit_ship failed: {e}")

    # Ensure IN_ORBIT before navigating
    nav_final = unwrap_data(await maybe_await(fleet_api, "get_ship_nav", ship_symbol=ship_symbol))
    act = fleet_obj.update_from_nav(ship_symbol, nav_final)
    if _status_value(act.status) != "IN_ORBIT":
        print(f"[ACTION] ensure orbit (status={act.status})")
        try:
            await maybe_await(fleet_api, "orbit_ship", ship_symbol=ship_symbol)
            nav_final2 = unwrap_data(await maybe_await(fleet_api, "get_ship_nav", ship_symbol=ship_symbol))
            fleet_obj.update_from_nav(ship_symbol, nav_final2)
        except Exception as e:
            print(f"[WARN] orbit_ship failed: {e}")

    act = fleet_obj.get(ship_symbol)
    print(f"[READY] {ship_symbol}: status={act.status}, wp={act.current_waypoint}, fuel_level={act.fuel_level}")

async def navigate_and_wait(fleet_api: FleetApi, fleet_obj: FleetObject, ship_symbol: str, target_wp: str) -> None:
    # Skip if already there & not in transit
    act = fleet_obj.get(ship_symbol)
    if act and act.current_waypoint == target_wp and not _is_in_transit_status(act.status):
        print(f"[SKIP] {ship_symbol} already at {target_wp}")
        return

    print(f"[NAV] request: {ship_symbol} → {target_wp}")
    req = _build_nav_request(target_wp)
    try:
        nav_resp = await maybe_await(fleet_api, "navigate_ship", ship_symbol=ship_symbol, navigate_ship_request=req)
    except TypeError:
        nav_resp = await maybe_await(fleet_api, "navigate_ship", ship_symbol=ship_symbol, body=req)

    nav_dto = unwrap_data(nav_resp)
    act = fleet_obj.update_from_nav(ship_symbol, nav_dto)
    arrival = act.arr_time
    dest = act.destination_waypoint or target_wp
    print(f"[NAV] accepted: {ship_symbol} → {dest}, arrival {_fmt_dt(arrival)}")

    await wait_while_in_transit(fleet_api, fleet_obj, ship_symbol)
    act = fleet_obj.get(ship_symbol)
    print(f"[NAV] arrived: {ship_symbol} at {act.current_waypoint}")

# -------------------------------- main ----------------------------------------
async def async_main() -> None:
    ship_symbol = "TROOTS-1"

    with setup_client_from_env() as client:
        fleet_api = FleetApi(client)
        agents_api = AgentsApi(client)

        # Build adapted fleet_object (no DTOs in business logic)
        fleet_obj = await build_fleet_object(fleet_api)

        # Select ship or fall back
        act = fleet_obj.get(ship_symbol)
        if act is None:
            # pick first ship present
            ship_symbol = next(iter(fleet_obj.by_symbol.keys()), None)
            act = fleet_obj.get(ship_symbol) if ship_symbol else None
        if not act:
            raise SystemExit("[FATAL] No ships available in fleet_object.")

        # Determine HQ and current location
        hq_wp = await get_agent_hq_waypoint(agents_api)
        # Ensure local nav is fresh
        nav0 = unwrap_data(await maybe_await(fleet_api, "get_ship_nav", ship_symbol=ship_symbol))
        act = fleet_obj.update_from_nav(ship_symbol, nav0)
        start_wp = act.current_waypoint
        print(f"[START] {ship_symbol} at {start_wp}, HQ is {hq_wp}")

        # Prep & go to HQ
        await ensure_ready_to_navigate(fleet_api, fleet_obj, ship_symbol, hq_wp)
        await navigate_and_wait(fleet_api, fleet_obj, ship_symbol, hq_wp)

        # Pause 15s at HQ
        print("[PAUSE] Sleeping 15 seconds at HQ...")
        await asyncio.sleep(15)

        # Return to start if different
        if start_wp and start_wp != hq_wp:
            print(f"[RETURN] to {start_wp}")
            await ensure_ready_to_navigate(fleet_api, fleet_obj, ship_symbol, start_wp)
            await navigate_and_wait(fleet_api, fleet_obj, ship_symbol, start_wp)
        else:
            print("[RETURN] no-op (start == HQ)")

        # Final snapshot
        final = fleet_obj.get(ship_symbol)
        print(f"[DONE] {ship_symbol}: status={final.status}, wp={final.current_waypoint}, fuel_level={final.fuel_level}")

if __name__ == "__main__":
    asyncio.run(async_main())
