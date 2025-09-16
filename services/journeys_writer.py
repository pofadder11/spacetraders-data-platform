# services/journeys_writer.py
from __future__ import annotations
from typing import Any, Optional, Dict
from datetime import datetime, timezone

import sqlite3

from db.auto_repo_sqlite import TableSpec, upsert_many
from domain.journey import JourneyRow

def g(obj, *attrs):
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _journey_id(ship_symbol: str, origin: str, dest: str, dep: str, arr: str) -> str:
    # Deterministic, stable across retries
    return f"{ship_symbol}#{origin}>{dest}@{dep}->{arr}"

def build_journey_from_nav(
    ship_symbol: str,
    nav_dto: Any,
    *,
    ship_dto_for_counters: Optional[Any] = None,
    observed_at: Optional[datetime] = None,
) -> Optional[JourneyRow]:
    """
    Create a JourneyRow directly from a ShipNav-like DTO.
    Only emits when nav.status == 'IN_TRANSIT' and route has origin/dest/dep/arr.
    """
    status = getattr(nav_dto, "status", None)
    if status != "IN_TRANSIT":
        return None

    origin = g(nav_dto, "route", "origin", "symbol")
    dest   = g(nav_dto, "route", "destination", "symbol")
    dep    = g(nav_dto, "route", "departure_time")
    arr    = g(nav_dto, "route", "arrival")
    mode   = getattr(nav_dto, "flight_mode", None)

    if not (ship_symbol and origin and dest and dep and arr):
        return None

    fuel_departure = g(ship_dto_for_counters, "fuel", "current") if ship_dto_for_counters else None
    cargo_departure = g(ship_dto_for_counters, "cargo", "units") if ship_dto_for_counters else None

    return JourneyRow(
        id=_journey_id(ship_symbol, origin, dest, str(dep), str(arr)),
        ship_symbol=ship_symbol,
        origin_waypoint=origin,
        destination_waypoint=dest,
        departure_time=str(dep),
        arrival_time=str(arr),
        flight_mode=mode,
        fuel_departure=fuel_departure,
        cargo_departure=cargo_departure,
        observed_at=observed_at or _now_utc(),
    )

def append_journey_from_nav(
    ship_symbol: str,
    nav_dto: Any,
    *,
    ship_dto_for_counters: Optional[Any] = None,
    observed_at: Optional[datetime] = None,
) -> Optional[JourneyRow]:
    """
    Build + write a JourneyRow using auto_repo_sqlite (no manual DDL).
    Returns the JourneyRow if written; None if nothing to log.
    """
    jr = build_journey_from_nav(
        ship_symbol,
        nav_dto,
        ship_dto_for_counters=ship_dto_for_counters,
        observed_at=observed_at,
    )
    if jr is None:
        return None
    
    conn = sqlite3.Connection("spacetraders.db")
    # Append-only semantics via deterministic PK `id`
    upsert_many(conn, TableSpec(table="journeys", pk="id"), [jr])
    return jr
