# services/normalizer.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Any

from sqlalchemy.orm import Session
from models import FleetNav


def _enum_str(x):
    """
    Enums from the generated client are str subclasses; handle str and Enum robustly.
    """
    return getattr(x, "value", x) if x is not None else None


def normalize_fleet_nav_row(ship) -> FleetNav | None:
    """
    Build a FleetNav ORM row from an API Ship model.
    Returns None if nav is missing.
    """
    nav = getattr(ship, "nav", None)
    if nav is None:
        return None

    route = getattr(nav, "route", None)
    dep = getattr(route, "origin", None) if route else None
    dest = getattr(route, "destination", None) if route else None

    return FleetNav(
        ship_symbol=ship.symbol,
        status=_enum_str(getattr(nav, "status", None)),
        flight_mode=_enum_str(getattr(nav, "flight_mode", None)),

        # Current location
        system_symbol=getattr(nav, "system_symbol", None),
        waypoint_symbol=getattr(nav, "waypoint_symbol", None),

        # Route details (if in transit)
        route_departure_system=getattr(dep, "system_symbol", None) if dep else None,
        route_departure_waypoint=getattr(dep, "symbol", None) if dep else None,
        route_destination_system=getattr(dest, "system_symbol", None) if dest else None,
        route_destination_waypoint=getattr(dest, "symbol", None) if dest else None,
        route_departure_time=getattr(route, "departure_time", None) if route else None,
        route_arrival_time=getattr(route, "arrival", None) if route else None,

        updated_at=datetime.now(timezone.utc),
    )


def upsert_fleet_nav_from_ship(session: Session, ship) -> bool:
    """
    Upsert a single ship's nav row. Returns True if a row was merged, False if ship.nav missing.
    """
    row = normalize_fleet_nav_row(ship)
    if row is None:
        return False
    session.merge(row)
    return True


def upsert_fleet_nav(session: Session, ships: Iterable[Any]) -> int:
    """
    Upsert many ships' nav rows. Returns the count of rows actually merged.
    Commits once at the end for efficiency.
    """
    count = 0
    for ship in ships:
        if upsert_fleet_nav_from_ship(session, ship):
            count += 1
    session.commit()
    return count
