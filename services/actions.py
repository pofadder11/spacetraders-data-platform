"""Reusable action helper functions."""

from __future__ import annotations

from typing import Any, Optional

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

