"""Reusable action helper functions."""

from __future__ import annotations

from typing import Any, Optional
import asyncio

from . import api_groups
from openapi_client.models.navigate_ship_request import NavigateShipRequest
from openapi_client.models.sell_cargo_request import SellCargoRequest
from openapi_client.models.refuel_ship_request import RefuelShipRequest


def navigate_ship(
    ship_symbol: str,
    waypoint_symbol: str,
    api: Any = api_groups.etl,
):
    """Navigate a ship to the given waypoint."""
    req = NavigateShipRequest(waypointSymbol=waypoint_symbol)
    return api.fleet.navigate_ship(ship_symbol, req)

def sell_cargo(
    ship_symbol: str,
    good_symbol: str,
    units: int,
    api: Any = api_groups.etl,
):
    """Sell cargo from a ship."""
    req = SellCargoRequest(symbol=good_symbol, units=units)
    return api.fleet.sell_cargo(ship_symbol, req)


def refuel_ship(
    ship_symbol: str,
    units: Optional[int] = None,
    from_cargo: Optional[bool] = None,
    api: Any = api_groups.etl,
):
    """Refuel a ship, optionally specifying units or drawing from cargo."""
    request = None
    if units is not None or from_cargo is not None:
        request = RefuelShipRequest(units=units, fromCargo=from_cargo)
        return api.fleet.refuel_ship(ship_symbol, request)
    return api.fleet.refuel_ship(ship_symbol)


def list_ships(api: Any = api_groups.etl):
    """Return the player's ships and persist via write-through handlers."""
    return api.fleet.get_my_ships()


def orbit(ship_symbol: str, api: Any = api_groups.etl):
    """Put a ship into orbit and persist nav via write-through handlers."""
    return api.fleet.orbit_ship(ship_symbol)


__all__ = [
    "navigate_ship",
    "sell_cargo",
    "refuel_ship",
    "list_ships",
    "orbit",
]

# -------------------------
# Async helpers for orchestration
# These use the plain data-proxy (no write-through) so callers can decide
# when/if to persist via external mechanisms.
# -------------------------
async def _to_thread(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)
async def get_ship_nav_async(ship_symbol: str, api: Any = api_groups.api):
    return await _to_thread(api.fleet.get_ship_nav, ship_symbol)
async def get_my_ship_async(ship_symbol: str, api: Any = api_groups.api):
    return await _to_thread(api.fleet.get_my_ship, ship_symbol)
async def dock_ship_async(ship_symbol: str, api: Any = api_groups.api):
    return await _to_thread(api.fleet.dock_ship, ship_symbol)
async def orbit_ship_async(ship_symbol: str, api: Any = api_groups.api):
    return await _to_thread(api.fleet.orbit_ship, ship_symbol)
async def refuel_ship_async(
    ship_symbol: str,
    units: Optional[int] = None,
    from_cargo: Optional[bool] = None,
    api: Any = api_groups.api,
):
    req = None
    if units is not None or from_cargo is not None:
        req = RefuelShipRequest(units=units, fromCargo=from_cargo)
        return await _to_thread(api.fleet.refuel_ship, ship_symbol, req)
    return await _to_thread(api.fleet.refuel_ship, ship_symbol)
async def navigate_ship_async(
    ship_symbol: str,
    waypoint_symbol: str,
    api: Any = api_groups.api,
):
    req = NavigateShipRequest(waypointSymbol=waypoint_symbol)
    return await _to_thread(api.fleet.navigate_ship, ship_symbol, req)
async def prepare_ship_for_navigation_async(
    ship_symbol: str,
    api: Any = api_groups.api,
) -> None:
    """Ensure a ship is ready to navigate: wait out transit, refuel, and orbit.
    - If IN_TRANSIT, wait until nav.route.arrival.
    - If fuel < capacity, dock (if needed) and refuel.
    - Ensure final status is IN_ORBIT.
    """
    nav = await get_ship_nav_async(ship_symbol, api=api)
    status = getattr(nav, "status", None)
    # Wait out transit
    if status == "IN_TRANSIT":
        route = getattr(nav, "route", None)
        arrival = getattr(route, "arrival", None) if route else None
        if arrival is not None:
            # arrival is datetime with tz; compute seconds to wait
            import datetime as _dt
            now = _dt.datetime.now(_dt.timezone.utc)
            if arrival.tzinfo is None:
                arrival = arrival.replace(tzinfo=_dt.timezone.utc)
            wait_sec = max(0.0, (arrival - now).total_seconds())
            await asyncio.sleep(wait_sec + 1)
    # Refuel if below capacity
    ship = await get_my_ship_async(ship_symbol, api=api)
    fuel = getattr(ship, "fuel", None)
    fuel_current = getattr(fuel, "current", None) if fuel else None
    fuel_capacity = getattr(fuel, "capacity", None) if fuel else None
    if (
        fuel_current is not None
        and fuel_capacity is not None
        and fuel_current < fuel_capacity
    ):
        if status != "DOCKED":
            await dock_ship_async(ship_symbol, api=api)
            # tiny pause to let server-side state settle
            await asyncio.sleep(0.5)
        await refuel_ship_async(ship_symbol, api=api)
        await asyncio.sleep(0.2)
        # Refresh nav after refuel/dock
        nav = await get_ship_nav_async(ship_symbol, api=api)
        status = getattr(nav, "status", None)
    # Ensure ship is in orbit
    if status != "IN_ORBIT":
        await orbit_ship_async(ship_symbol, api=api)
        await asyncio.sleep(0.2)
async def navigate_with_prep_async(
    ship_symbol: str,
    waypoint_symbol: str,
    api: Any = api_groups.api,
):
    """Prepare the ship then navigate; wait until arrival.
    Skips navigation if already at waypoint.
    """
    nav = await get_ship_nav_async(ship_symbol, api=api)
    cur_wp = getattr(nav, "waypoint_symbol", None)
    if cur_wp == waypoint_symbol:
        return nav  # already there
    await prepare_ship_for_navigation_async(ship_symbol, api=api)
    resp = await navigate_ship_async(ship_symbol, waypoint_symbol, api=api)
    nav_after = getattr(resp, "nav", None)
    # Wait for arrival if provided in response
    route = getattr(nav_after, "route", None) if nav_after is not None else None
    arrival = getattr(route, "arrival", None) if route else None
    if arrival is not None:
        import datetime as _dt
        now = _dt.datetime.now(_dt.timezone.utc)
        if arrival.tzinfo is None:
            arrival = arrival.replace(tzinfo=_dt.timezone.utc)
        wait_sec = max(0.0, (arrival - now).total_seconds())
        await asyncio.sleep(wait_sec + 1)
    return resp

__all__ += [
    "get_ship_nav_async",
    "get_my_ship_async",
    "dock_ship_async",
    "orbit_ship_async",
    "refuel_ship_async",
    "navigate_ship_async",
    "prepare_ship_for_navigation_async",
    "navigate_with_prep_async",
]


