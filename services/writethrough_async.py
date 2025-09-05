from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from models import (
    System as DbSystem,
    Waypoint as DbWaypoint,
    FleetNav as DbFleetNav,
    ShipCurrent as DbShipCurrent,
    MarketTradeGoodSnapshot as DbMktSnap,
    MarketTradeGoodCurrent as DbMktCur,
    ShipCargoCurrent as DbCargoCur,
    ShipyardOfferSnapshot as DbYardSnap,
    ShipyardOfferCurrent as DbYardCur,
)


def _enum_str(x):
    return getattr(x, "value", x) if x is not None else None


async def upsert_system(session: AsyncSession, system: Any) -> None:
    row = DbSystem(
        symbol=system.symbol,
        type=getattr(system, "type", None),
        x=getattr(system, "x", None),
        y=getattr(system, "y", None),
    )
    await session.merge(row)


async def upsert_waypoints(session: AsyncSession, waypoints: Iterable[Any]) -> int:
    count = 0
    for w in waypoints:
        row = DbWaypoint(
            symbol=w.symbol,
            system_symbol=getattr(w, "system_symbol", None),
            type=getattr(w, "type", None),
            x=getattr(w, "x", None),
            y=getattr(w, "y", None),
        )
        await session.merge(row)
        count += 1
    return count


async def upsert_ships_current(session: AsyncSession, ships: Iterable[Any]) -> int:
    count = 0
    now = datetime.now(timezone.utc)
    for ship in ships:
        reg = getattr(ship, "registration", None)
        role = getattr(reg, "role", None)
        nav = getattr(ship, "nav", None)
        cargo = getattr(ship, "cargo", None)
        fuel = getattr(ship, "fuel", None)
        row = DbShipCurrent(
            ship_symbol=ship.symbol,
            role=_enum_str(role),
            nav_status=_enum_str(getattr(nav, "status", None)) if nav else None,
            flight_mode=_enum_str(getattr(nav, "flight_mode", None)) if nav else None,
            system_symbol=getattr(nav, "system_symbol", None) if nav else None,
            waypoint_symbol=getattr(nav, "waypoint_symbol", None) if nav else None,
            fuel_current=getattr(fuel, "current", None) if fuel else None,
            fuel_capacity=getattr(fuel, "capacity", None) if fuel else None,
            cargo_units=getattr(cargo, "units", None) if cargo else None,
            updated_at=now,
        )
        await session.merge(row)
        count += 1
    return count


async def upsert_fleet_nav_from_ship(session: AsyncSession, ship: Any) -> bool:
    nav = getattr(ship, "nav", None)
    if nav is None:
        return False
    route = getattr(nav, "route", None)
    dep = getattr(route, "origin", None) if route else None
    dest = getattr(route, "destination", None) if route else None
    row = DbFleetNav(
        ship_symbol=ship.symbol,
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
    await session.merge(row)
    return True


async def upsert_fleet_nav(session: AsyncSession, ships: Iterable[Any]) -> int:
    count = 0
    for ship in ships:
        if await upsert_fleet_nav_from_ship(session, ship):
            count += 1
    return count


async def upsert_market(session: AsyncSession, market: Any) -> int:
    now = datetime.now(timezone.utc)
    count = 0
    wp = getattr(market, "symbol", None)
    goods = getattr(market, "trade_goods", None) or []
    # Snapshot rows
    for g in goods:
        row = DbMktSnap(
            waypoint_symbol=wp,
            trade_symbol=g.symbol,
            observed_at=now,
            type=getattr(g, "type", None),
            trade_volume=getattr(g, "trade_volume", None),
            supply=getattr(g, "supply", None),
            activity=getattr(g, "activity", None),
            purchase_price=getattr(g, "purchase_price", None),
            sell_price=getattr(g, "sell_price", None),
        )
        await session.merge(row)
        count += 1
    # Current table
    for g in goods:
        cur = DbMktCur(
            waypoint_symbol=wp,
            trade_symbol=g.symbol,
            observed_at=now,
            type=getattr(g, "type", None),
            trade_volume=getattr(g, "trade_volume", None),
            supply=getattr(g, "supply", None),
            activity=getattr(g, "activity", None),
            purchase_price=getattr(g, "purchase_price", None),
            sell_price=getattr(g, "sell_price", None),
        )
        await session.merge(cur)
    return count


# -------------------------
# Cargo and extraction yields
# -------------------------
async def update_ship_current_cargo_units(session: AsyncSession, ship_symbol: str, units: int | None) -> None:
    now = datetime.now(timezone.utc)
    row = await session.get(DbShipCurrent, ship_symbol)
    if row is None:
        row = DbShipCurrent(ship_symbol=ship_symbol, updated_at=now)
    row.cargo_units = units
    row.updated_at = now
    await session.merge(row)


async def upsert_ship_cargo_current(session: AsyncSession, ship_symbol: str, cargo: Any) -> int:
    await session.execute(delete(DbCargoCur).where(DbCargoCur.ship_symbol == ship_symbol))
    inv = getattr(cargo, "inventory", None) or []
    now = datetime.now(timezone.utc)
    count = 0
    for item in inv:
        row = DbCargoCur(
            ship_symbol=ship_symbol,
            trade_symbol=getattr(item, "symbol", None),
            units=getattr(item, "units", 0) or 0,
            updated_at=now,
        )
        await session.merge(row)
        count += 1
    return count


async def insert_extraction_yield(
    session: AsyncSession,
    ship_symbol: str,
    trade_symbol: str,
    units: int,
    cooldown: Any,
) -> None:
    # Derive waypoint from fleet_nav if available
    nav_row = await session.get(DbFleetNav, ship_symbol)
    wp = getattr(nav_row, "waypoint_symbol", None) if nav_row else None
    row = DbMktSnap.__class__  # placeholder to appease type checkers
    from models import ExtractionYield as DbYield  # local import to avoid cycles

    y = DbYield(
        ship_symbol=ship_symbol,
        waypoint_symbol=wp,
        trade_symbol=trade_symbol,
        units=units,
        cooldown_total_seconds=getattr(cooldown, "total_seconds", None),
        cooldown_remaining_seconds=getattr(cooldown, "remaining_seconds", None),
        cooldown_expiration=getattr(cooldown, "expiration", None),
        observed_at=datetime.now(timezone.utc),
    )
    await session.merge(y)


# -------------------------
# Shipyards: offers snapshot + current
# -------------------------
async def upsert_shipyard_offers(session: AsyncSession, shipyard: Any) -> int:
    """Persist shipyard offers (snapshot + current)."""
    wp = getattr(shipyard, "symbol", None)
    ships = getattr(shipyard, "ships", None) or []
    now = datetime.now(timezone.utc)
    count = 0
    for s in ships:
        ship_type = getattr(s, "type", None)
        name = getattr(s, "name", None)
        price = getattr(s, "purchase_price", None)
        if not ship_type:
            continue
        snap = DbYardSnap(
            waypoint_symbol=wp,
            ship_type=ship_type,
            observed_at=now,
            name=name,
            purchase_price=price,
        )
        cur = DbYardCur(
            waypoint_symbol=wp,
            ship_type=ship_type,
            observed_at=now,
            name=name,
            purchase_price=price,
        )
        await session.merge(snap)
        await session.merge(cur)
        count += 1
    return count
