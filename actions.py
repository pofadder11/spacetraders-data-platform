from __future__ import annotations

from typing import Any, Optional

from openapi_client.models.navigate_ship_request import NavigateShipRequest
from openapi_client.models.refuel_ship_request import RefuelShipRequest
from openapi_client.models.sell_cargo_request import SellCargoRequest

from services.api_groups import etl as _etl


def navigate_ship(
    ship_symbol: str,
    waypoint_symbol: str,
    svc: Any = _etl,
) -> Any:
    """Navigate a ship to a waypoint."""
    request = NavigateShipRequest(waypointSymbol=waypoint_symbol)
    return svc.fleet.navigate_ship(ship_symbol, request)


def sell_cargo(
    ship_symbol: str,
    trade_symbol: str,
    units: int,
    svc: Any = _etl,
) -> Any:
    """Sell cargo from a ship."""
    request = SellCargoRequest(symbol=trade_symbol, units=units)
    return svc.fleet.sell_cargo(ship_symbol, request)


def refuel_ship(
    ship_symbol: str,
    units: Optional[int] = None,
    from_cargo: Optional[bool] = None,
    svc: Any = _etl,
) -> Any:
    """Refuel a ship."""
    req = None
    if units is not None or from_cargo is not None:
        req = RefuelShipRequest(units=units, from_cargo=from_cargo)
    return svc.fleet.refuel_ship(ship_symbol, req)
