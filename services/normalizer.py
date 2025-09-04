# services/normalizer.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Any

from sqlalchemy.orm import Session
from models import (
    FleetNav,
    MarketTradeGoodSnapshot,
    MarketTradeGoodCurrent,
    ShipCurrent,
    Waypoint,
    System as DbSystem,
    ExtractionYield as DbExtractionYield,
    ShipCargoCurrent,
)
from sqlalchemy import delete


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


# -------------------------
# Market trade goods
# -------------------------
def normalize_market_trade_goods_rows(market, observed_at: datetime) -> list[MarketTradeGoodSnapshot]:
    """
    Build snapshot rows for Market.trade_goods at a given observation time.
    `market` is an instance of openapi_client.models.Market.
    """
    rows: list[MarketTradeGoodSnapshot] = []
    waypoint_symbol = getattr(market, "symbol", None)
    goods = getattr(market, "trade_goods", None)
    if not waypoint_symbol or not goods:
        return rows
    for g in goods:
        rows.append(
            MarketTradeGoodSnapshot(
                waypoint_symbol=waypoint_symbol,
                trade_symbol=g.symbol,
                observed_at=observed_at,
                type=getattr(g, "type", None),
                trade_volume=getattr(g, "trade_volume", None),
                supply=getattr(g, "supply", None),
                activity=getattr(g, "activity", None),
                purchase_price=getattr(g, "purchase_price", None),
                sell_price=getattr(g, "sell_price", None),
            )
        )
    return rows


def upsert_market_trade_goods(session: Session, market, observed_at: datetime | None = None) -> int:
    """
    Insert/merge snapshot rows for the market's trade goods.
    observed_at defaults to now() UTC when not provided.
    """
    if observed_at is None:
        observed_at = datetime.now(timezone.utc)
    rows = normalize_market_trade_goods_rows(market, observed_at)
    for row in rows:
        session.merge(row)
    session.commit()
    return len(rows)


def upsert_market_trade_goods_current(session: Session, market, observed_at: datetime | None = None) -> int:
    """
    Upsert the latest/current view per (waypoint_symbol, trade_symbol).
    If an existing row is newer than observed_at, keep it.
    """
    if observed_at is None:
        observed_at = datetime.now(timezone.utc)
    
    def _to_epoch(dt: datetime | None) -> float | None:
        if dt is None:
            return None
        # Normalize to UTC and compare as epoch seconds to avoid tz issues
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt.timestamp()
    waypoint_symbol = getattr(market, "symbol", None)
    goods = getattr(market, "trade_goods", None)
    if not waypoint_symbol or not goods:
        return 0
    updated = 0
    for g in goods:
        pk = (waypoint_symbol, g.symbol)
        existing = session.get(MarketTradeGoodCurrent, pk)
        if existing and existing.observed_at and _to_epoch(existing.observed_at) >= _to_epoch(observed_at):
            continue  # keep newer
        row = existing or MarketTradeGoodCurrent(
            waypoint_symbol=waypoint_symbol,
            trade_symbol=g.symbol,
        )
        row.observed_at = observed_at
        row.type = getattr(g, "type", None)
        row.trade_volume = getattr(g, "trade_volume", None)
        row.supply = getattr(g, "supply", None)
        row.activity = getattr(g, "activity", None)
        row.purchase_price = getattr(g, "purchase_price", None)
        row.sell_price = getattr(g, "sell_price", None)
        session.merge(row)
        updated += 1
    session.commit()
    return updated


# -------------------------
# Fleet nav updates from navigate responses
# -------------------------
def upsert_fleet_nav_from_nav(session: Session, ship_symbol: str, nav) -> None:
    """
    Update FleetNav row using a ShipNav model (from navigate or get_ship_nav).
    """
    route = getattr(nav, "route", None)
    dep = getattr(route, "origin", None) if route else None
    dest = getattr(route, "destination", None) if route else None
    session.merge(
        FleetNav(
            ship_symbol=ship_symbol,
            status=_enum_str(getattr(nav, "status", None)),
            flight_mode=_enum_str(getattr(nav, "flight_mode", None)),
            system_symbol=getattr(nav, "system_symbol", None),
            waypoint_symbol=getattr(nav, "waypoint_symbol", None),
            route_departure_system=getattr(dep, "system_symbol", None) if dep else None,
            route_departure_waypoint=getattr(dep, "symbol", None) if dep else None,
            route_destination_system=getattr(dest, "system_symbol", None) if dest else None,
            route_destination_waypoint=getattr(dest, "symbol", None) if dest else None,
            route_departure_time=getattr(route, "departure_time", None) if route else None,
            route_arrival_time=getattr(route, "arrival", None) if route else None,
            updated_at=datetime.now(timezone.utc),
        )
    )
    session.commit()


# -------------------------
# Ships current
# -------------------------
def normalize_ship_current_row_from_ship(ship) -> ShipCurrent:
    """
    Build a ShipCurrent row from a full Ship model.
    """
    registration = getattr(ship, "registration", None)
    role = getattr(registration, "role", None)
    nav = getattr(ship, "nav", None)
    cargo = getattr(ship, "cargo", None)
    fuel = getattr(ship, "fuel", None)
    return ShipCurrent(
        ship_symbol=ship.symbol,
        role=_enum_str(role),
        nav_status=_enum_str(getattr(nav, "status", None)) if nav else None,
        flight_mode=_enum_str(getattr(nav, "flight_mode", None)) if nav else None,
        system_symbol=getattr(nav, "system_symbol", None) if nav else None,
        waypoint_symbol=getattr(nav, "waypoint_symbol", None) if nav else None,
        fuel_current=getattr(fuel, "current", None) if fuel else None,
        fuel_capacity=getattr(fuel, "capacity", None) if fuel else None,
        cargo_units=getattr(cargo, "units", None) if cargo else None,
        updated_at=datetime.now(timezone.utc),
    )


def upsert_ships_current(session: Session, ships: Iterable[Any]) -> int:
    count = 0
    for ship in ships:
        row = normalize_ship_current_row_from_ship(ship)
        session.merge(row)
        count += 1
    session.commit()
    return count


def upsert_ship_current_from_nav_fuel(session: Session, ship_symbol: str, nav=None, fuel=None) -> None:
    """
    Update ShipCurrent row using ShipNav and ShipFuel (from navigate/patch responses).
    """
    # fetch existing or create new
    existing = session.get(ShipCurrent, ship_symbol)
    row = existing or ShipCurrent(ship_symbol=ship_symbol, updated_at=datetime.now(timezone.utc))
    if nav is not None:
        row.nav_status = _enum_str(getattr(nav, "status", None))
        row.flight_mode = _enum_str(getattr(nav, "flight_mode", None))
        row.system_symbol = getattr(nav, "system_symbol", None)
        row.waypoint_symbol = getattr(nav, "waypoint_symbol", None)
    if fuel is not None:
        row.fuel_current = getattr(fuel, "current", None)
        row.fuel_capacity = getattr(fuel, "capacity", None)
    row.updated_at = datetime.now(timezone.utc)
    session.merge(row)
    session.commit()


def upsert_ship_current_from_nav(session: Session, ship_symbol: str, nav) -> None:
    """
    Update ShipCurrent row from ShipNav only (dock/orbit/get_ship_nav responses).
    """
    upsert_ship_current_from_nav_fuel(session, ship_symbol, nav=nav, fuel=None)


# -------------------------
# Cargo and Yield from extraction/siphon
# -------------------------
def update_ship_current_cargo_units(session: Session, ship_symbol: str, units: int | None) -> None:
    existing = session.get(ShipCurrent, ship_symbol)
    row = existing or ShipCurrent(ship_symbol=ship_symbol, updated_at=datetime.now(timezone.utc))
    row.cargo_units = units
    row.updated_at = datetime.now(timezone.utc)
    session.merge(row)
    session.commit()


def upsert_ship_cargo_current(session: Session, ship_symbol: str, cargo) -> int:
    """Replace the current inventory for a ship based on ShipCargo."""
    # wipe existing rows for the ship, then insert fresh snapshot
    session.execute(delete(ShipCargoCurrent).where(ShipCargoCurrent.ship_symbol == ship_symbol))
    count = 0
    inventory = getattr(cargo, "inventory", None) or []
    now = datetime.now(timezone.utc)
    for item in inventory:
        session.merge(
            ShipCargoCurrent(
                ship_symbol=ship_symbol,
                trade_symbol=getattr(item, "symbol", None),
                units=getattr(item, "units", 0) or 0,
                updated_at=now,
            )
        )
        count += 1
    session.commit()
    return count


def _current_waypoint_for_ship(session: Session, ship_symbol: str) -> str | None:
    nav = session.get(FleetNav, ship_symbol)
    return getattr(nav, "waypoint_symbol", None) if nav is not None else None


def insert_extraction_yield(
    session: Session,
    ship_symbol: str,
    trade_symbol: str,
    units: int,
    cooldown,
) -> None:
    wp = _current_waypoint_for_ship(session, ship_symbol)
    row = DbExtractionYield(
        ship_symbol=ship_symbol,
        waypoint_symbol=wp,
        trade_symbol=trade_symbol,
        units=units,
        cooldown_total_seconds=getattr(cooldown, "total_seconds", None),
        cooldown_remaining_seconds=getattr(cooldown, "remaining_seconds", None),
        cooldown_expiration=getattr(cooldown, "expiration", None),
        observed_at=datetime.now(timezone.utc),
    )
    session.add(row)
    session.commit()


# -------------------------
# Systems and Waypoints
# -------------------------
def upsert_system_row(session: Session, system) -> None:
    """
    Persist a System model into DbSystem.
    """
    session.merge(
        DbSystem(
            symbol=system.symbol,
            type=getattr(system, "type", None),
            x=getattr(system, "x", None),
            y=getattr(system, "y", None),
        )
    )
    session.commit()


def upsert_waypoints_from_list(session: Session, waypoints: Iterable[Any]) -> int:
    count = 0
    for w in waypoints:
        session.merge(
            Waypoint(
                symbol=w.symbol,
                system_symbol=getattr(w, "system_symbol", None),
                type=getattr(w, "type", None),
                x=getattr(w, "x", None),
                y=getattr(w, "y", None),
            )
        )
        count += 1
    session.commit()
    return count
