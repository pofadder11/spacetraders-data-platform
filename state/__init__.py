"""Simple in-memory state helpers for runner.

This module provides tiny helpers for the runner script so that the
runner's decision logic can track the latest view of ship state without
concerning itself with persistence.  It uses the :class:`ShipState`
model from :mod:`runner_state` and stores instances in a module level
cache.

Additionally, helpers are provided to sync state directly from
write-through API results (e.g., nav updates), so you can keep the
runner's working set fresh without querying the DB.
"""

from __future__ import annotations

from typing import Dict, Iterable, Any
from datetime import datetime

from runner_state import ShipState

# Internal cache of ship state keyed by ship symbol
_SHIPS: Dict[str, ShipState] = {}


def update_from_api(ship: object) -> ShipState:
    """Create :class:`ShipState` from an API ship object and cache it.

    Parameters
    ----------
    ship:
        Object returned from the OpenAPI client representing a ship.

    Returns
    -------
    ShipState
        The normalised state for the ship.
    """

    state = ShipState.from_api(ship)
    _SHIPS[state.symbol] = state
    return state


def update_from_ships(ships: Iterable[object]) -> Dict[str, ShipState]:
    """Bulk-update cache from an iterable of API ship objects.

    Returns a shallow copy of the updated cache entries for convenience.
    """
    updated: Dict[str, ShipState] = {}
    for ship in ships:
        st = update_from_api(ship)
        updated[st.symbol] = st
    return updated


def update_from_nav(ship_symbol: str, nav: Any | None, fuel: Any | None = None) -> ShipState:
    """Update cached state from a ShipNav payload.

    Parameters
    ----------
    ship_symbol: str
        Symbol identifying the ship.
    nav: Any | None
        OpenAPI ShipNav model (may be None, in which case only timestamp is refreshed).
    fuel: Any | None
        Optional fuel payload; currently ignored by ShipState but accepted for future use.
    """
    cur = _SHIPS.get(ship_symbol)
    if cur is None:
        # create a minimal placeholder, then fill from nav if available
        cur = ShipState(symbol=ship_symbol, updated_at=datetime.utcnow())

    system_symbol = getattr(nav, "system_symbol", None) if nav is not None else cur.system_symbol
    waypoint_symbol = getattr(nav, "waypoint_symbol", None) if nav is not None else cur.waypoint_symbol
    # Prefer explicit fields; fall back to route.origin/destination for context
    if nav is not None and (system_symbol is None or waypoint_symbol is None):
        route = getattr(nav, "route", None)
        if route is not None:
            dest = getattr(route, "destination", None)
            if dest is not None:
                system_symbol = system_symbol or getattr(dest, "system_symbol", None)
                waypoint_symbol = waypoint_symbol or getattr(dest, "symbol", None)

    st = ShipState(
        symbol=ship_symbol,
        nav_status=getattr(nav, "status", None) if nav is not None else cur.nav_status,
        system_symbol=system_symbol,
        waypoint_symbol=waypoint_symbol,
        cargo_units=cur.cargo_units,
        updated_at=datetime.utcnow(),
    )
    _SHIPS[ship_symbol] = st
    return st


def get_ship(symbol: str) -> ShipState | None:
    """Return cached state for ``symbol`` if available."""

    return _SHIPS.get(symbol)


def all_ships() -> Dict[str, ShipState]:
    """Return a shallow copy of the entire ship state cache."""

    return dict(_SHIPS)
