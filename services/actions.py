"""Reusable action helper functions."""

from __future__ import annotations

from typing import Any, Optional
import asyncio

from services import api_groups
from openapi_client.models.navigate_ship_request import NavigateShipRequest
from openapi_client.models.sell_cargo_request import SellCargoRequest
from openapi_client.models.refuel_ship_request import RefuelShipRequest
from openapi_client.models.ship_nav_status import ShipNavStatus
from openapi_client.exceptions import ApiException


def navigate_ship(
    ship_symbol: str,
    waypoint_symbol: str,
    api: Any = api_groups.etl,
):
    """Navigate a ship to the given waypoint."""
    req = NavigateShipRequest(waypointSymbol=waypoint_symbol)
    # Write-through etl requires selecting the API group explicitly
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
    # API expects '{}' as body when no params are specified
    return api.fleet.refuel_ship(ship_symbol, RefuelShipRequest())


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
    return await _to_thread(api.get_ship_nav, ship_symbol)

async def get_my_ship_async(ship_symbol: str, api: Any = api_groups.api):
    return await _to_thread(api.get_my_ship, ship_symbol)

async def dock_ship_async(ship_symbol: str, api: Any = api_groups.api):
    return await _to_thread(api.dock_ship, ship_symbol)

async def orbit_ship_async(ship_symbol: str, api: Any = api_groups.api):
    return await _to_thread(api.orbit_ship, ship_symbol)

async def refuel_ship_async(
    ship_symbol: str,
    units: Optional[int] = None,
    from_cargo: Optional[bool] = None,
    api: Any = api_groups.api,
):
    # Skip refuel for ships that don't use fuel (capacity == 0)
    try:
        ship = await get_my_ship_async(ship_symbol, api=api)
        cap = getattr(getattr(ship, "fuel", None), "capacity", None)
        if cap is not None and cap <= 0:
            return None
    except Exception:
        pass
    req = None
    if units is not None or from_cargo is not None:
        req = RefuelShipRequest(units=units, fromCargo=from_cargo)
        return await _to_thread(api.refuel_ship, ship_symbol, req)
    # API expects an empty JSON object when no params are given
    return await _to_thread(api.refuel_ship, ship_symbol, RefuelShipRequest())


async def navigate_ship_async(
    ship_symbol: str,
    waypoint_symbol: str,
    api: Any = api_groups.api,
):
    req = NavigateShipRequest(waypointSymbol=waypoint_symbol)
    return await _to_thread(api.navigate_ship, ship_symbol, req)


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
    # Wait out transit
    if nav.status == "IN_TRANSIT":
        if getattr(nav, "route", None) is not None and getattr(nav.route, "arrival", None) is not None:
            # arrival is datetime with tz; compute seconds to wait
            import datetime as _dt
            now = _dt.datetime.now(_dt.timezone.utc)
            arrival = nav.route.arrival
            if arrival.tzinfo is None:
                arrival = arrival.replace(tzinfo=_dt.timezone.utc)
            wait_sec = max(0.0, (arrival - now).total_seconds())
            await asyncio.sleep(wait_sec + 1)
    # Refuel if below capacity
    ship = await get_my_ship_async(ship_symbol, api=api)

    cur = getattr(getattr(ship, "fuel", None), "current", None)
    cap = getattr(getattr(ship, "fuel", None), "capacity", None)
    # Only attempt refuel when capacity > 0 and not already full
    if (cap is not None and cap > 0 and cur is not None and cur < cap):
        # Ensure docked, with retry/backoff if rate limited
        await _ensure_docked_with_backoff(ship_symbol, api=api)
        # Try refuel with lightweight retry/backoff and recheck docking if needed
        await _refuel_with_backoff(ship_symbol, api=api)
        # Refresh nav after refuel/dock
        nav = await get_ship_nav_async(ship_symbol, api=api)
    # Ensure ship is in orbit
    if nav.status != ShipNavStatus.IN_ORBIT:
        await _orbit_with_backoff(ship_symbol, api=api)
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
    # Robust wait: poll nav until not IN_TRANSIT (respects rate limits)
    await _wait_until_not_in_transit(ship_symbol, api=api, hint_resp=resp)
    return resp

__all__ += [
    "get_ship_nav_async",
    "get_my_ship_async",
    "dock_ship_async",
    "orbit_ship_async",
    "refuel_ship_async",
    "navigate_ship_async",
    "navigate_with_prep_async",
]


# Public helper: ensure docked with internal backoff/wait
async def ensure_docked_async(ship_symbol: str, api: Any = api_groups.api) -> None:
    await _ensure_docked_with_backoff(ship_symbol, api=api)

__all__ += ["ensure_docked_async"]


# -------------------------
# Internal reliability helpers (backoff / state-assert)
# -------------------------
async def _sleep_from_exception(e: Exception) -> None:
    """Sleep based on Retry-After header when present; otherwise small default."""
    delay = 0.5
    try:
        headers = getattr(e, "headers", None) or {}
        ra = headers.get("Retry-After") if isinstance(headers, dict) else None
        if ra is not None:
            try:
                delay = max(delay, float(ra))
            except Exception:
                pass
    except Exception:
        pass
    await asyncio.sleep(delay)


async def _ensure_docked_with_backoff(ship_symbol: str, api: Any) -> None:
    # Ensure we're not in transit first
    await _wait_until_not_in_transit(ship_symbol, api=api)
    # quick exit
    nav = await get_ship_nav_async(ship_symbol, api=api)
    if getattr(nav, "status", None) == ShipNavStatus.DOCKED:
        return
    # try a few times
    for _ in range(5):
        try:
            await dock_ship_async(ship_symbol, api=api)
        except ApiException as e:
            await _sleep_from_exception(e)
        await asyncio.sleep(0.3)
        nav = await get_ship_nav_async(ship_symbol, api=api)
        if getattr(nav, "status", None) == ShipNavStatus.DOCKED:
            return
    # last attempt without raising if still not docked
    return


async def _refuel_with_backoff(ship_symbol: str, api: Any) -> None:
    for _ in range(5):
        try:
            await refuel_ship_async(ship_symbol, api=api)
            return
        except ApiException as e:
            body = getattr(e, "body", "") or ""
            if "not currently docked" in str(body).lower():
                await _ensure_docked_with_backoff(ship_symbol, api=api)
            await _sleep_from_exception(e)
    return


async def _orbit_with_backoff(ship_symbol: str, api: Any) -> None:
    for _ in range(5):
        try:
            await orbit_ship_async(ship_symbol, api=api)
            return
        except ApiException as e:
            await _sleep_from_exception(e)
    return


async def _wait_until_not_in_transit(ship_symbol: str, api: Any, hint_resp: Any | None = None) -> None:
    """Wait until ship is no longer IN_TRANSIT. Uses response arrival as hint then polls nav.

    - If hint_resp.nav.route.arrival is provided, sleep until that time.
    - Then poll get_ship_nav until status != IN_TRANSIT, with short backoff.
    """
    # First wait based on response arrival if available
    try:
        nav_after = getattr(hint_resp, "nav", None) if hint_resp is not None else None
        route = getattr(nav_after, "route", None) if nav_after is not None else None
        arrival = getattr(route, "arrival", None) if route is not None else None
        if arrival is not None:
            import datetime as _dt
            now = _dt.datetime.now(_dt.timezone.utc)
            if getattr(arrival, "tzinfo", None) is None:
                arrival = arrival.replace(tzinfo=_dt.timezone.utc)
            wait_sec = max(0.0, (arrival - now).total_seconds())
            if wait_sec > 0:
                await asyncio.sleep(wait_sec + 1)
    except Exception:
        pass
    # Then poll nav up to a few times to confirm state change server-side
    for _ in range(10):
        try:
            nav = await get_ship_nav_async(ship_symbol, api=api)
            if getattr(nav, "status", None) != ShipNavStatus.IN_TRANSIT:
                return
        except ApiException as e:
            await _sleep_from_exception(e)
        await asyncio.sleep(0.5)
    return


