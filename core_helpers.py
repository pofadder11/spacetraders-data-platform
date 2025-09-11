# =================================================================================================
# core_helpers.py
# -------------------------------------------------------------------------------------------------
# In-memory state containers + initialization that builds domain objects up-front
# using adapters (no DTOs in runner). Also provides nav/ready helpers that UPDATE the state.
# =================================================================================================
from __future__ import annotations
import asyncio
from typing import Any, Dict, Iterable, List, Optional
from datetime import datetime, timezone

from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.agents_api import AgentsApi
from openapi_client.api.systems_api import SystemsApi

from runtime_support import (
    maybe_await,
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

# domain + adapters you already have
from domain.ships_activity import ShipsActivity
from adapters.ships_activity_adapter import adapt_ships_activity_from_ship, merge_activity_with_nav

from adapters.waypoint_adapter import adapt_waypoints              # returns List[WaypointRef]
from adapters.waypoint_trait_adapter import adapt_traits_from_waypoint_dtos  # returns List[WaypointTraitRow]


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
    def __init__(self, fleet: FleetActivityState, waypoints: WaypointsRefState, traits: WaypointTraitsState, agent_hq: str):
        self.fleet = fleet
        self.waypoints = waypoints
        self.traits = traits
        self.agent_hq = agent_hq


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

    return WorldState(fleet=fleet_state, waypoints=wp_state, traits=trait_state, agent_hq=hq_wp)


# -------- navigation helpers USING STATE (and patching it) --------------------
async def wait_while_in_transit(fleet_api: FleetApi, state: WorldState, ship_symbol: str) -> None:
    while True:
        nav = await api_get_ship_nav(fleet_api, ship_symbol)
        act = state.fleet.merge_nav(ship_symbol, nav)
        if not is_in_transit(nav):
            return
        arrival = getattr(getattr(nav, "route", None), "arrival", None)
        print(f"[WAIT] {ship_symbol} in transit; arrival {fmt_dt(arrival)}")
        now = now_utc()
        if arrival and getattr(arrival, "tzinfo", None) is None:
            arrival = arrival.replace(tzinfo=timezone.utc)
        if arrival:
            secs = (arrival - now).total_seconds()
            await asyncio.sleep(max(secs, 0) + 1.0)
        else:
            await asyncio.sleep(2.0)

async def ensure_ready_to_navigate(fleet_api: FleetApi, state: WorldState, ship_symbol: str, target_waypoint: str) -> None:
    # Refresh nav → state
    nav = await api_get_ship_nav(fleet_api, ship_symbol)
    act = state.fleet.merge_nav(ship_symbol, nav)
    print(f"[SNAP] {ship_symbol}: status={act.status}, wp={act.current_waypoint}, fuel_level={act.fuel_level}")

    # Already at target & not in transit
    if act.current_waypoint == target_waypoint and status_value(act.status) != "IN_TRANSIT":
        print(f"[INFO] {ship_symbol} already at {target_waypoint}")
        return

    # Wait if in transit
    if status_value(act.status) == "IN_TRANSIT":
        print(f"[INFO] {ship_symbol} IN_TRANSIT → waiting...")
        await wait_while_in_transit(fleet_api, state, ship_symbol)
        act = state.fleet.get(ship_symbol)  # refreshed

    # Fuel check via domain property
    needs_fuel = (act.fuel_level is None) or (act.fuel_level < 1.0)
    print(f"[CHECK] fuel_level={act.fuel_level} → needs_refuel={needs_fuel}")
    if needs_fuel:
        # Dock, refuel, orbit — with state patches
        try:
            await api_dock_ship(fleet_api, ship_symbol)
        except Exception as e:
            print(f"[WARN] dock_ship: {e}")

        ref = await api_refuel_ship(fleet_api, ship_symbol)
        if ref:
            state.fleet.merge_refuel(ship_symbol, ref)
            print(f"[SNAP] post-refuel fuel_level={state.fleet.get(ship_symbol).fuel_level}")

        # Update nav and orbit if not in transit
        nav1 = await api_get_ship_nav(fleet_api, ship_symbol)
        act1 = state.fleet.merge_nav(ship_symbol, nav1)
        if status_value(act1.status) != "IN_TRANSIT":
            try:
                await api_orbit_ship(fleet_api, ship_symbol)
            except Exception as e:
                print(f"[WARN] orbit_ship: {e}")
            nav2 = await api_get_ship_nav(fleet_api, ship_symbol)
            state.fleet.merge_nav(ship_symbol, nav2)

    # Ensure in orbit finally
    nav_final = await api_get_ship_nav(fleet_api, ship_symbol)
    act_final = state.fleet.merge_nav(ship_symbol, nav_final)
    if status_value(act_final.status) != "IN_ORBIT":
        try:
            await api_orbit_ship(fleet_api, ship_symbol)
        except Exception as e:
            print(f"[WARN] orbit_ship(final): {e}")
        nav_after = await api_get_ship_nav(fleet_api, ship_symbol)
        state.fleet.merge_nav(ship_symbol, nav_after)

async def navigate_and_wait(fleet_api: FleetApi, state: WorldState, ship_symbol: str, target_waypoint: str) -> None:
    act = state.fleet.get(ship_symbol)
    if act and act.current_waypoint == target_waypoint and status_value(act.status) != "IN_TRANSIT":
        print(f"[SKIP] {ship_symbol} already at {target_waypoint}")
        return

    nav_dto = await api_navigate_ship(fleet_api, ship_symbol, target_waypoint)
    act2 = state.fleet.merge_nav(ship_symbol, nav_dto)
    print(f"[NAV] {ship_symbol} → {act2.destination_waypoint or target_waypoint}, arrival {fmt_dt(act2.arr_time)}")
    await wait_while_in_transit(fleet_api, state, ship_symbol)
    act3 = state.fleet.get(ship_symbol)
    print(f"[ARRIVED] {ship_symbol} at {act3.current_waypoint}")