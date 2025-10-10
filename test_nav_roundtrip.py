#!/usr/bin/env python3
# test_nav_roundtrip.py
# Verbose mini-runner:
# - Preps ship TROOTS-1 (fuel/orbit) for navigation to Agent HQ waypoint
# - Navigates there, waits 15s, then navigates back to the original waypoint

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Iterable, Optional

# Reuse infra from your repo (created earlier). Falls back gracefully if missing.
from runtime_support import setup_client_from_env, maybe_await, unwrap_data 

# Generated APIs
from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.agents_api import AgentsApi

# You have these in your repo
from adapters.ships_activity_adapter import adapt_ships_activity_from_ship


# ----------------------------- utils ------------------------------------------
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

def _is_in_transit(nav_dto: Any) -> bool:
    return _status_value(getattr(nav_dto, "status", None)) == "IN_TRANSIT"

def _build_nav_request(waypoint_symbol: str) -> Any:
    try:
        from openapi_client.models.navigate_ship_request import NavigateShipRequest  # type: ignore
        return NavigateShipRequest(waypoint_symbol=waypoint_symbol)
    except Exception:
        return {"waypoint_symbol": waypoint_symbol, "waypointSymbol": waypoint_symbol}


# -------------------------- core helpers --------------------------------------
async def get_agent_hq_waypoint(agents: AgentsApi) -> str:
    resp = await maybe_await(agents, "get_my_agent")
    agent = unwrap_data(resp)
    hq_wp = getattr(agent, "headquarters", None)
    if not hq_wp or not isinstance(hq_wp, str):
        raise RuntimeError("Agent headquarters not found")
    print(f"[INFO] Agent HQ waypoint: {hq_wp}")
    return hq_wp

async def get_ship_activity_snapshot(fleet: FleetApi, ship_symbol: str):
    # You can also call get_ship_nav directly; we also adapt the full ship for fuel_level
    try:
        ship_resp = await maybe_await(fleet, "get_my_ship", ship_symbol=ship_symbol)
    except Exception:
        ship_resp = await maybe_await(fleet, "get_ship", ship_symbol=ship_symbol)
    ship_dto = unwrap_data(ship_resp)
    activity = adapt_ships_activity_from_ship(ship_dto)  # gives fuel_level, status, current_waypoint, etc.

    nav_resp = await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol)
    nav_dto = unwrap_data(nav_resp)

    return activity, nav_dto

async def wait_while_in_transit(fleet: FleetApi, ship_symbol: str) -> None:
    while True:
        nav_resp = await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol)
        nav = unwrap_data(nav_resp)
        if not _is_in_transit(nav):
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

async def ensure_ready_to_navigate(fleet: FleetApi, ship_symbol: str, target_waypoint: str) -> None:
    """Verbose prep: not in transit, enough fuel (refuel if < 1.0), in orbit, not already at target."""
    # Check current snapshot
    act, nav = await get_ship_activity_snapshot(fleet, ship_symbol)
    print(f"[DEBUG] {ship_symbol} status={act.status}, wp={act.current_waypoint}, fuel_level={act.fuel_level}")

    # 1) Already at target? (and not in transit)
    if (act.current_waypoint == target_waypoint) and not _is_in_transit(nav):
        print(f"[INFO] {ship_symbol} already at {target_waypoint} — no navigation needed.")
        return

    # 2) If in transit, wait
    if _is_in_transit(nav):
        print(f"[INFO] {ship_symbol} is in transit. Waiting until arrival...")
        await wait_while_in_transit(fleet, ship_symbol)
        # refresh after wait
        act, nav = await get_ship_activity_snapshot(fleet, ship_symbol)

    # 3) Fuel check
    needs_fuel = (act.fuel_level is None) or (act.fuel_level < 1.0)
    print(f"[CHECK] Fuel level = {act.fuel_level} → needs_refuel={needs_fuel}")
    if needs_fuel:
        # Dock
        print(f"[ACTION] Dock {ship_symbol} for refuel")
        try:
            await maybe_await(fleet, "dock_ship", ship_symbol=ship_symbol)
        except Exception as e:
            print(f"[WARN] dock_ship failed: {e}")

        # Refuel (always send empty JSON)
        print(f"[ACTION] Refuel {ship_symbol}")
        try:
            await maybe_await(fleet, "refuel_ship", ship_symbol=ship_symbol, refuel_ship_request={})
        except TypeError:
            try:
                await maybe_await(fleet, "refuel_ship", ship_symbol=ship_symbol, body={})
            except Exception as e:
                print(f"[WARN] refuel_ship failed: {e}")
        except Exception as e:
            print(f"[WARN] refuel_ship failed: {e}")

        # Refresh and report
        act, nav = await get_ship_activity_snapshot(fleet, ship_symbol)
        print(f"[DEBUG] Post-refuel: fuel_level={act.fuel_level}")

        # Orbit again if not in transit
        if not _is_in_transit(nav):
            print(f"[ACTION] Orbit {ship_symbol}")
            try:
                await maybe_await(fleet, "orbit_ship", ship_symbol=ship_symbol)
            except Exception as e:
                print(f"[WARN] orbit_ship failed: {e}")
        else:
            print(f"[INFO] Skipping orbit — ship entered transit unexpectedly.")

    # 4) Ensure IN_ORBIT before navigating
    nav = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    status = _status_value(getattr(nav, "status", None))
    if status != "IN_ORBIT":
        print(f"[ACTION] Ensure orbit: current status={status}")
        try:
            await maybe_await(fleet, "orbit_ship", ship_symbol=ship_symbol)
        except Exception as e:
            print(f"[WARN] orbit_ship failed: {e}")

    # Final check log
    act, nav = await get_ship_activity_snapshot(fleet, ship_symbol)
    print(f"[READY] {ship_symbol} → status={act.status}, wp={act.current_waypoint}, fuel_level={act.fuel_level}")


async def navigate_and_wait(fleet: FleetApi, ship_symbol: str, target_wp: str) -> None:
    # final sanity: if already there and not in transit, skip
    nav0 = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    here = getattr(nav0, "waypoint_symbol", None)
    if here == target_wp and not _is_in_transit(nav0):
        print(f"[SKIP] {ship_symbol} already at {target_wp}")
        return

    print(f"[NAV] Request: {ship_symbol} → {target_wp}")
    req = _build_nav_request(target_wp)
    try:
        nav_resp = await maybe_await(fleet, "navigate_ship", ship_symbol=ship_symbol, navigate_ship_request=req)
    except TypeError:
        nav_resp = await maybe_await(fleet, "navigate_ship", ship_symbol=ship_symbol, body=req)

    nav_dto = unwrap_data(nav_resp)
    route = getattr(nav_dto, "route", None)
    arrival = getattr(route, "arrival", None)
    dest = getattr(getattr(route, "destination", None), "symbol", target_wp)
    print(f"[NAV] Accepted: {ship_symbol} → {dest}, arrival {_fmt_dt(arrival)}")

    await wait_while_in_transit(fleet, ship_symbol)
    print(f"[NAV] Arrived at {dest}")


# ------------------------------ main ------------------------------------------
async def async_main() -> None:
    ship_symbol = "TROOTS-1"

    with setup_client_from_env() as client:
        fleet = FleetApi(client)
        agents = AgentsApi(client)

        # Get agent HQ waypoint
        hq_wp = await get_agent_hq_waypoint(agents)

        # Snapshot starting waypoint for the ship
        nav0 = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
        start_wp = getattr(nav0, "waypoint_symbol", None)
        print(f"[START] {ship_symbol} currently at {start_wp}, heading to HQ {hq_wp}")

        # Prep checks: fuel/status/current_waypoint != target
        await ensure_ready_to_navigate(fleet, ship_symbol, hq_wp)

        # Navigate to HQ and wait to arrive
        await navigate_and_wait(fleet, ship_symbol, hq_wp)

        # Hold 15 seconds
        print("[PAUSE] Sleeping 15 seconds at HQ...")
        await asyncio.sleep(15)

        # Navigate back to original waypoint (if it exists and is different)
        if start_wp and start_wp != hq_wp:
            print(f"[RETURN] Preparing to return to {start_wp}")
            await ensure_ready_to_navigate(fleet, ship_symbol, start_wp)
            await navigate_and_wait(fleet, ship_symbol, start_wp)
        else:
            print("[RETURN] No distinct original waypoint to return to (or same as HQ).")

        print("[DONE] Round-trip complete.")


if __name__ == "__main__":
    asyncio.run(async_main())
