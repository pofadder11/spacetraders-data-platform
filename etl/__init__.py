"""Simple in-memory state helpers for runner.

This module provides tiny helpers for the runner script so that the
runner's decision logic can track the latest view of ship state without
concerning itself with persistence.  It uses the :class:`ShipState`
model from :mod:`runner_state` and stores instances in a module level
cache.

The functions are intentionally lightweight; a more complete
implementation would likely sync state to a database.  For the purpose
of the unit tests and the runner example they provide just enough
functionality.
"""

from __future__ import annotations

from typing import Dict

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


def get_ship(symbol: str) -> ShipState | None:
    """Return cached state for ``symbol`` if available."""

    return _SHIPS.get(symbol)


def all_ships() -> Dict[str, ShipState]:
    """Return a shallow copy of the entire ship state cache."""

    return dict(_SHIPS)
