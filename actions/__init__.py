"""High level action wrappers used by the runner.

The functions exposed here are intentionally small and synchronous.  They
thinly wrap calls to the :class:`OpenAPIService` so the runner only needs
compose decision logic and is not tied to the underlying API client.
"""

from __future__ import annotations

from services.client_service import OpenAPIService
from openapi_client.models.navigate_ship_request import NavigateShipRequest


def list_ships(svc: OpenAPIService):
    """Return the agent's ships using the Fleet API."""

    return svc.d.fleet.get_my_ships()


def orbit(svc: OpenAPIService, ship_symbol: str):
    """Move ``ship_symbol`` into orbit."""

    return svc.d.fleet.orbit_ship(ship_symbol)


def dock(svc: OpenAPIService, ship_symbol: str):
    """Dock ``ship_symbol`` at its current waypoint."""

    return svc.d.fleet.dock_ship(ship_symbol)


def navigate(svc: OpenAPIService, ship_symbol: str, destination: str):
    """Navigate ``ship_symbol`` to ``destination`` waypoint."""

    req = NavigateShipRequest(waypoint_symbol=destination)
    return svc.d.fleet.navigate_ship(ship_symbol, navigate_ship_request=req)
