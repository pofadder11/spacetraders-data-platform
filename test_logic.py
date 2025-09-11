#!/usr/bin/env python3
# test_logic.py  — drop-in replacement
# Navigate a FRIGATE to every SHIPYARD waypoint using local Pydantic state + DB writes.
from __future__ import annotations

import asyncio
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

# Reuse helpers from your testrunner
from testrunner import maybe_await, unwrap_data, setup_client_from_env  # type: ignore

# Generated APIs
from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.systems_api import SystemsApi

# Domain + adapters already in your repo
from domain.ships_activity import ShipsActivity
from domain.ships_specs import ShipsSpecs
from adapters.ships_activity_adapter import (
    adapt_ships_activity_from_ship,
    merge_activity_with_nav,
)
from adapters.ships_specs_adapter import adapt_ships_specs_from_ship

# Shipyard domain/adapter
from domain.ship_market import ShipMarketRow
from adapters.shipyard_adapter import adapt_ship_market_rows

# SQLite auto-repo (DRY persistence)
from db.auto_repo_sqlite import TableSpec, upsert_many


# ----------------------------- util -------------------------------------------
def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _fmt_dt(dt: Optional[datetime]) -> str:
    if not dt:
        return "None"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")

def _build_nav_request(waypoint_symbol: str) -> Any:
    """Create a navigate request compatible with the generated client."""
    try:
        from openapi_client.models.navigate_ship_request import NavigateShipRequest  # type: ignore
        return NavigateShipRequest(waypoint_symbol=waypoint_symbol)
    except Exception:
        # Some clients accept dict/kw-body
        return {"waypoint_symbol": waypoint_symbol, "waypointSymbol": waypoint_symbol}

async def _sleep_until(arrival: datetime) -> None:
    if arrival.tzinfo is None:
        arrival = arrival.replace(tzinfo=timezone.utc)
    now = _now_utc()
    secs = (arrival - now).total_seconds()
    if secs > 0:
        await asyncio.sleep(secs)


# --- status normalization ------------------------------------------------------
def _status_value(status_obj: Any) -> str:
    """Return plain 'IN_TRANSIT' / 'IN_ORBIT' / ... from enum or str."""
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
        s = s.split(".")[-1]  # e.g., "ShipNavStatus.IN_TRANSIT" -> "IN_TRANSIT"
    return s

def _is_in_transit(nav_dto: Any) -> bool:
    return _status_value(getattr(nav_dto, "status", None)) == "IN_TRANSIT"


# -------------------------- local state ---------------------------------------
@dataclass
class FleetState:
    """Local, easily-referenced state for your session."""
    # Activity & Specs keyed by ship symbol
    activities: Dict[str, ShipsActivity] = field(default_factory=dict)
    specs: Dict[str, ShipsSpecs] = field(default_factory=dict)

    # Shipyard listings cached by waypoint
    ship_market: Dict[str, List[ShipMarketRow]] = field(default_factory=dict)

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


# ----------------------- DB convenience ---------------------------------------
def get_shipyard_waypoints(conn: sqlite3.Connection) -> list[str]:
    """Use already-flattened waypoint_traits to find SHIPYARD locations."""
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT waypoint_symbol FROM waypoint_traits WHERE trait_symbol = 'SHIPYARD' ORDER BY waypoint_symbol"
    )
    return [row["waypoint_symbol"] for row in cur.fetchall()]


# ----------------------------- bootstrap --------------------------------------
async def load_initial_fleet_state(conn: sqlite3.Connection, fleet: FleetApi) -> FleetState:
    """Load ships once, build local state (activity + specs) and persist to DB."""
    resp = await maybe_await(fleet, "get_my_ships")
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


# ------------------------- waiters / guards -----------------------------------
async def wait_while_in_transit(fleet: FleetApi, ship_symbol: str) -> None:
    """
    Poll nav until ship is no longer IN_TRANSIT.
    Prefer sleeping until route.arrival; fallback to short polling.
    """
    while True:
        nav_resp = await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol)
        nav = unwrap_data(nav_resp)
        if not _is_in_transit(nav):
            return

        arrival = getattr(getattr(nav, "route", None), "arrival", None)
        if arrival:
            now = datetime.now(timezone.utc)
            if arrival.tzinfo is None:
                arrival = arrival.replace(tzinfo=timezone.utc)
            secs = (arrival - now).total_seconds()
            await asyncio.sleep(max(secs, 0) + 1.0)  # cushion
        else:
            await asyncio.sleep(2.0)

async def ensure_not_in_transit(fleet: FleetApi, ship_symbol: str) -> None:
    nav = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    if _is_in_transit(nav):
        arrival = getattr(getattr(nav, "route", None), "arrival", None)
        print(f"[NAV] {ship_symbol} is IN_TRANSIT; waiting until { _fmt_dt(arrival) }")
        await wait_while_in_transit(fleet, ship_symbol)


# ------------------------- ship ops (with state) ------------------------------
async def ensure_fuel_full(fleet: FleetApi, state: FleetState, conn: sqlite3.Connection, ship_symbol: str) -> None:
    # If in transit, skip fuel handling entirely
    nav_now = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    if _is_in_transit(nav_now):
        print(f"[FUEL] {ship_symbol}: skip (in transit)")
        return

    # Fetch ship → check fuel
    try:
        resp = await maybe_await(fleet, "get_my_ship", ship_symbol=ship_symbol)
    except Exception:
        resp = await maybe_await(fleet, "get_ship", ship_symbol=ship_symbol)
    ship = unwrap_data(resp)
    fuel = getattr(ship, "fuel", None)
    cur = getattr(fuel, "current", None) if fuel else None
    cap = getattr(fuel, "capacity", None) if fuel else None
    if cur is None or cap is None or cur >= cap:
        return

    print(f"[FUEL] {ship_symbol}: {cur}/{cap} — docking & refueling...")
    # Guard again: API may reject if we somehow got in-transit
    nav_chk = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    if _is_in_transit(nav_chk):
        print(f"[FUEL] {ship_symbol}: abort dock (became in transit)")
        return
    try:
        await maybe_await(fleet, "dock_ship", ship_symbol=ship_symbol)
    except Exception as e:
        print(f"[FUEL][dock] warn: {e}")

    # Refuel — always send an empty JSON body to avoid 422
    refuel_resp = None
    try:
        refuel_resp = await maybe_await(
            fleet, "refuel_ship", ship_symbol=ship_symbol, refuel_ship_request={}
        )
    except TypeError:
        try:
            refuel_resp = await maybe_await(
                fleet, "refuel_ship", ship_symbol=ship_symbol, body={}
            )
        except Exception as e:
            print(f"[FUEL][refuel] warn: {e}")
    except Exception as e:
        print(f"[FUEL][refuel] warn: {e}")

    if refuel_resp is not None:
        refuel_dto = unwrap_data(refuel_resp)
        updated = state.update_activity_from_refuel(ship_symbol, refuel_dto)
        upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), [updated])

    # Orbit (only if not in transit)
    nav_chk2 = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    if _is_in_transit(nav_chk2):
        print(f"[FUEL] {ship_symbol}: skip orbit (in transit)")
        return
    try:
        await maybe_await(fleet, "orbit_ship", ship_symbol=ship_symbol)
    except Exception as e:
        print(f"[FUEL][orbit] warn: {e}")

async def ensure_in_orbit(fleet: FleetApi, state: FleetState, conn: sqlite3.Connection, ship_symbol: str) -> None:
    nav = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    if _is_in_transit(nav):
        print(f"[ORBIT] {ship_symbol}: skip (in transit)")
        return
    status = _status_value(getattr(nav, "status", None))
    if status != "IN_ORBIT":
        print(f"[ORBIT] {ship_symbol}: status={status} → orbit")
        try:
            await maybe_await(fleet, "orbit_ship", ship_symbol=ship_symbol)
        except Exception as e:
            print(f"[ORBIT] warn: {e}")
        nav2 = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
        updated = state.update_activity_from_nav(ship_symbol, nav2)
        upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), [updated])

async def navigate_and_wait(
    fleet: FleetApi,
    state: FleetState,
    conn: sqlite3.Connection,
    ship_symbol: str,
    target_wp: str,
) -> None:
    # Already there + not in transit?
    nav0 = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    here = getattr(nav0, "waypoint_symbol", None)
    if here == target_wp and not _is_in_transit(nav0):
        print(f"[SKIP] {ship_symbol} already at {target_wp}")
        return

    # Ensure we’re not mid-flight (block until arrival)
    await ensure_not_in_transit(fleet, ship_symbol)

    # Fuel & Orbit (now guaranteed not in transit)
    await ensure_fuel_full(fleet, state, conn, ship_symbol)
    await ensure_in_orbit(fleet, state, conn, ship_symbol)

    # Send navigate
    req = _build_nav_request(target_wp)
    try:
        nav_resp = await maybe_await(fleet, "navigate_ship", ship_symbol=ship_symbol, navigate_ship_request=req)
    except TypeError:
        nav_resp = await maybe_await(fleet, "navigate_ship", ship_symbol=ship_symbol, body=req)

    nav_dto = unwrap_data(nav_resp)
    updated = state.update_activity_from_nav(ship_symbol, nav_dto)
    upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), [updated])

    route = getattr(nav_dto, "route", None)
    arrival = getattr(route, "arrival", None)
    dest = getattr(getattr(route, "destination", None), "symbol", target_wp)
    print(f"[NAV] {ship_symbol} → {dest}, arrival { _fmt_dt(arrival) }")

    # Block until not in transit
    await wait_while_in_transit(fleet, ship_symbol)

    # Final sync
    nav_after = unwrap_data(await maybe_await(fleet, "get_ship_nav", ship_symbol=ship_symbol))
    updated2 = state.update_activity_from_nav(ship_symbol, nav_after)
    upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), [updated2])


# ----------------------- shipyard caching (state + DB) ------------------------
async def cache_shipyard_listings(
    systems: SystemsApi,
    state: FleetState,
    conn: sqlite3.Connection,
    system_symbol: str,
    waypoint_symbol: str,
) -> None:
    """Fetch shipyard listings at a waypoint and store both locally and in DB."""
    try:
        resp = await maybe_await(systems, "get_shipyard", system_symbol=system_symbol, waypoint_symbol=waypoint_symbol)
        dto = unwrap_data(resp)
        rows = adapt_ship_market_rows(dto, waypoint_symbol)
        if rows:
            state.ship_market[waypoint_symbol] = rows
            upsert_many(conn, TableSpec(table="ship_market", pk="id"), rows)
            print(f"[SHIPYARD] {waypoint_symbol}: cached {len(rows)} listings")
        else:
            print(f"[SHIPYARD] {waypoint_symbol}: no listings returned")
    except Exception as e:
        print(f"[SHIPYARD] {waypoint_symbol}: error {e}")


# ------------------------------ orchestration ---------------------------------
async def async_main() -> None:
    # open DB
    conn = sqlite3.connect("spacetraders.db")
    try:
        with setup_client_from_env() as client:
            fleet_api = FleetApi(client)
            systems_api = SystemsApi(client)

            # 0) Load local state from API once (also persists to DB)
            state = await load_initial_fleet_state(conn, fleet_api)
            print(f"[BOOT] Loaded {len(state.activities)} activities, {len(state.specs)} specs into local state")

            # 1) Choose a FRIGATE from local state specs (fallback to any ship if none)
            ship_symbol = None
            for sym, spec in state.specs.items():
                if (spec.frame_name or "").lower().find("frigate") >= 0:
                    ship_symbol = sym
                    break
            if not ship_symbol:
                ship_symbol = next(iter(state.activities.keys()), None)
            if not ship_symbol:
                raise SystemExit("[FATAL] No ships in state.")
            print(f"[SELECT] Using ship {ship_symbol}")

            # 2) Gather SHIPYARD targets (from DB trait table)
            targets = get_shipyard_waypoints(conn)
            if not targets:
                print("[INFO] No SHIPYARD waypoints found in DB. Load waypoints+traits first.")
                return

            def _system_of(wp: str) -> str:
                parts = (wp or "").split("-")
                return "-".join(parts[:2]) if len(parts) >= 2 else ""

            print(f"[PLAN] Visit {len(targets)} shipyards")

            # 3) Visit each shipyard: navigate + cache ship listings
            for wp in targets:
                try:
                    print(f"\n[TARGET] {wp}")
                    await navigate_and_wait(fleet_api, state, conn, ship_symbol, wp)
                    sys_sym = _system_of(wp)
                    if sys_sym:
                        await cache_shipyard_listings(systems_api, state, conn, sys_sym, wp)
                except Exception as e:
                    print(f"[ERROR] {wp}: {e}")

            print("\n[DONE] Navigation + shipyard caching complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    asyncio.run(async_main())
