"""Async runner that orchestrates basic gameplay loops.

- List waypoints in DB
- Probe cycles markets to collect price data
- Frigate visits shipyards to buy mining drones
- Miners extract at an ENGINEERED_ASTEROID and transfer to frigate
- Jettison low-value cargo before transfer
- Frigate refines when possible; sells when full and returns
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, List, Optional

from dotenv import load_dotenv
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from services import api_groups
from services import actions as act
from openapi_client.models.purchase_ship_request import PurchaseShipRequest
from openapi_client.models.ship_type import ShipType
from openapi_client.models.transfer_cargo_request import TransferCargoRequest
from openapi_client.models.jettison_request import JettisonRequest
from openapi_client.models.ship_refine_request import ShipRefineRequest

from session import init_db, SessionLocal
from models import Waypoint, MarketTradeGoodCurrent, ShipCurrent


load_dotenv()


# -------------------------
# DB helpers
# -------------------------
def list_db_waypoints() -> List[str]:
    with SessionLocal() as s:
        return [w.symbol for w in s.execute(select(Waypoint)).scalars().all()]


def best_sell_price(s: Session, trade_symbol: str) -> Optional[int]:
    row = (
        s.execute(
            select(func.max(MarketTradeGoodCurrent.sell_price)).where(
                MarketTradeGoodCurrent.trade_symbol == trade_symbol
            )
        )
        .scalars()
        .first()
    )
    return int(row) if row is not None else None


# -------------------------
# First-pass bootstrap for blank DB
# -------------------------
def bootstrap_initial_state() -> None:
    """Populate DB with initial fleet and waypoint data for a new run.

    - Gets agent headquarters to determine the starting system
    - Persists system + waypoints via write-through handlers
    - Persists fleet and current nav for each ship
    """
    # Determine starting system from agent HQ
    agent = api_groups.api.get_my_agent()
    hq = getattr(agent, "headquarters", None)
    if not hq:
        return
    system_symbol = "-".join(hq.split("-")[:2])

    # Persist system + waypoints
    try:
        api_groups.etl.systems.get_system(system_symbol)
    except Exception:
        pass
    try:
        api_groups.etl.systems.get_system_waypoints(system_symbol)
    except Exception:
        pass

    # Persist fleet + nav (explicitly via normalizer to ensure DB seed)
    from services.normalizer import (
        upsert_ships_current,
        upsert_fleet_nav,
        upsert_ship_current_from_nav,
        upsert_fleet_nav_from_ship,
    )
    # Fetch ships via data-proxy (no write-through), then upsert explicitly
    try:
        ships = api_groups.api.get_my_ships()
    except Exception:
        ships = []
    if ships:
        with SessionLocal() as s:
            try:
                upsert_fleet_nav(s, ships)
                upsert_ships_current(s, ships)
            except Exception:
                pass
    # Ensure nav row is present/updated
    for ship in ships or []:
        sym = getattr(ship, "symbol", None)
        if not sym:
            continue
        try:
            nav = api_groups.api.get_ship_nav(sym)
            with SessionLocal() as s:
                upsert_ship_current_from_nav(s, sym, nav)
                # also ensure FleetNav has latest nav
                upsert_fleet_nav_from_ship(s, ship)
        except Exception:
            pass


# -------------------------
# Fleet/role helpers
# -------------------------
def pick_frigate_ship_symbol() -> Optional[str]:
    with SessionLocal() as s:
        rows = s.execute(select(ShipCurrent.ship_symbol, ShipCurrent.role)).all()
        def _find(*roles: str) -> Optional[str]:
            for sym, role in rows:
                if role in roles:
                    return sym
            return None
        return _find("REFINERY") or _find("COMMAND", "HAULER") or (rows[0][0] if rows else None)


def pick_probe_ship_symbol() -> Optional[str]:
    with SessionLocal() as s:
        rows = s.execute(select(ShipCurrent.ship_symbol, ShipCurrent.role)).all()
        for sym, role in rows:
            if role in ("EXPLORER", "SURVEYOR"):
                return sym
        return rows[0][0] if rows else None


# -------------------------
# Waypoint helpers
# -------------------------
async def current_system_for(ship_symbol: str) -> Optional[str]:
    nav = await act.get_ship_nav_async(ship_symbol)
    return getattr(nav, "system_symbol", None)


async def system_waypoints(system_symbol: str) -> list[Any]:
    return api_groups.api.get_system_waypoints(system_symbol)


def is_market_wp(wp: Any) -> bool:
    traits = getattr(wp, "traits", []) or []
    return any(getattr(t, "symbol", "") == "MARKETPLACE" for t in traits)


def is_shipyard_wp(wp: Any) -> bool:
    traits = getattr(wp, "traits", []) or []
    return any(getattr(t, "symbol", "") == "SHIPYARD" for t in traits)


def is_engineered_asteroid(wp: Any) -> bool:
    return getattr(wp, "type", None) == "ENGINEERED_ASTEROID"


# -------------------------
# Tasks
# -------------------------
async def probe_market_cycler(probe_symbol: str) -> None:
    sys_sym = await current_system_for(probe_symbol)
    if not sys_sym:
        return
    wps = await system_waypoints(sys_sym)
    markets = [w for w in wps if is_market_wp(w)]
    if not markets:
        return
    idx = 0
    while True:
        target = markets[idx % len(markets)]
        idx += 1
        await act.navigate_with_prep_async(probe_symbol, target.symbol)
        await asyncio.sleep(0.2)
        # Ensure not in transit and dock with backoff
        await act.ensure_docked_async(probe_symbol)
        await asyncio.sleep(0.2)
        api_groups.etl.systems.get_market(sys_sym, target.symbol)
        await asyncio.sleep(1.0)


async def frigate_buy_drones(frigate_symbol: str, desired_count: int = 3) -> None:
    sys_sym = await current_system_for(frigate_symbol)
    if not sys_sym:
        return
    wps = await system_waypoints(sys_sym)
    yards = [w for w in wps if is_shipyard_wp(w)]
    if not yards:
        return
    bought = 0
    for yard in yards:
        if bought >= desired_count:
            break
        await act.navigate_with_prep_async(frigate_symbol, yard.symbol)
        await asyncio.sleep(0.2)
        await act.ensure_docked_async(frigate_symbol)
        await asyncio.sleep(0.2)
        yard_info = api_groups.api.get_shipyard(sys_sym, yard.symbol)
        available = []
        if hasattr(yard_info, "ship_types") and yard_info.ship_types:
            available = [getattr(t, "type", None) for t in yard_info.ship_types]
        elif hasattr(yard_info, "ships") and yard_info.ships:
            available = [getattr(s, "type", None) for s in yard_info.ships]
        if ShipType.SHIP_MINING_DRONE not in available:
            continue
        req = PurchaseShipRequest(ship_type=ShipType.SHIP_MINING_DRONE, waypoint_symbol=yard.symbol)
        try:
            api_groups.etl.fleet.purchase_ship(req)
            bought += 1
        except Exception:
            pass


def has_mining_laser(ship: Any) -> bool:
    mounts = getattr(ship, "mounts", []) or []
    return any("MINING_LASER" in getattr(m, "symbol", "") for m in mounts)


async def ensure_orbit(ship_symbol: str) -> None:
    nav = await act.get_ship_nav_async(ship_symbol)
    if getattr(nav, "status", None) != "IN_ORBIT":
        await act.orbit_ship_async(ship_symbol)
        await asyncio.sleep(0.2)


def percentile(values: List[int], p: float) -> int:
    if not values:
        return 0
    v = sorted(values)
    k = max(0, min(len(v) - 1, int(p * (len(v) - 1))))
    return v[k]


async def jettison_low_value(ship_symbol: str) -> None:
    ship = await act.get_my_ship_async(ship_symbol)
    inv = getattr(getattr(ship, "cargo", None), "inventory", []) or []
    if not inv:
        return
    with SessionLocal() as s:
        values = []
        per_item = {}
        for item in inv:
            ts = getattr(item, "symbol", None)
            val = best_sell_price(s, ts) if ts else None
            if val is not None:
                values.append(val)
            per_item[ts] = val
        cutoff = percentile(values, 0.25) if values else 0
    for item in inv:
        ts = getattr(item, "symbol", None)
        units = getattr(item, "units", 0) or 0
        if not ts or units <= 0:
            continue
        val = per_item.get(ts)
        if val is None or val <= cutoff:
            try:
                req = JettisonRequest(symbol=ts, units=units)
                api_groups.api.jettison(ship_symbol, req)
                await asyncio.sleep(0.1)
            except Exception:
                pass


async def transfer_all_to(ship_from: str, ship_to: str) -> None:
    ship = await act.get_my_ship_async(ship_from)
    inv = getattr(getattr(ship, "cargo", None), "inventory", []) or []
    for item in inv:
        ts = getattr(item, "symbol", None)
        units = getattr(item, "units", 0) or 0
        if not ts or units <= 0:
            continue
        try:
            req = TransferCargoRequest(trade_symbol=ts, units=units, ship_symbol=ship_to)
            api_groups.etl.fleet.transfer_cargo(ship_from, req)
            await asyncio.sleep(0.1)
        except Exception:
            pass


async def refine_what_you_can(frigate_symbol: str) -> None:
    ship = await act.get_my_ship_async(frigate_symbol)
    inv = getattr(getattr(ship, "cargo", None), "inventory", []) or []
    have = {getattr(i, "symbol", None): getattr(i, "units", 0) or 0 for i in inv}
    refine_map = {
        "IRON_ORE": "IRON",
        "COPPER_ORE": "COPPER",
        "SILVER_ORE": "SILVER",
        "GOLD_ORE": "GOLD",
        "ALUMINUM_ORE": "ALUMINUM",
        "PLATINUM_ORE": "PLATINUM",
        "URANITE_ORE": "URANITE",
        "MERITIUM_ORE": "MERITIUM",
    }
    for raw, out in refine_map.items():
        if have.get(raw):
            try:
                api_groups.etl.fleet.ship_refine(frigate_symbol, ShipRefineRequest(produce=out))
                await asyncio.sleep(0.2)
            except Exception:
                pass


async def sell_all_high_value(frigate_symbol: str) -> None:
    with SessionLocal() as s:
        nav = await act.get_ship_nav_async(frigate_symbol)
        sys_sym = getattr(nav, "system_symbol", None)
        if not sys_sym:
            return
        wps = await system_waypoints(sys_sym)
        markets = [w for w in wps if is_market_wp(w)]
        if not markets:
            return
        ship = await act.get_my_ship_async(frigate_symbol)
        inv = getattr(getattr(ship, "cargo", None), "inventory", []) or []
        for item in inv:
            ts = getattr(item, "symbol", None)
            units = getattr(item, "units", 0) or 0
            if not ts or units <= 0:
                continue
            best_wp = None
            best_price = -1
            for w in markets:
                price = (
                    s.execute(
                        select(MarketTradeGoodCurrent.sell_price).where(
                            MarketTradeGoodCurrent.waypoint_symbol == w.symbol,
                            MarketTradeGoodCurrent.trade_symbol == ts,
                        )
                    )
                    .scalars()
                    .first()
                )
                if price is not None and price > best_price:
                    best_price = price
                    best_wp = w
            if best_wp is None:
                continue
            await act.navigate_with_prep_async(frigate_symbol, best_wp.symbol)
            await asyncio.sleep(0.2)
            await act.dock_ship_async(frigate_symbol)
            await asyncio.sleep(0.2)
            from openapi_client.models.sell_cargo_request import SellCargoRequest
            try:
                api_groups.etl.fleet.sell_cargo(
                    frigate_symbol,
                    SellCargoRequest(symbol=ts, units=units),
                )
                await asyncio.sleep(0.2)
            except Exception:
                pass


async def miners_loop(miner_symbols: list[str], target_wp: str, frigate_symbol: str) -> None:
    while True:
        tasks = [act.navigate_with_prep_async(sym, target_wp) for sym in miner_symbols]
        await asyncio.gather(*tasks)
        await asyncio.gather(*(ensure_orbit(sym) for sym in miner_symbols))
        for sym in miner_symbols:
            try:
                api_groups.etl.fleet.extract_resources(sym)
            except Exception:
                pass
        await asyncio.sleep(1.0)
        for sym in miner_symbols:
            await jettison_low_value(sym)
            nav_m = await act.get_ship_nav_async(sym)
            nav_f = await act.get_ship_nav_async(frigate_symbol)
            if getattr(nav_m, "waypoint_symbol", None) == getattr(nav_f, "waypoint_symbol", None):
                await transfer_all_to(sym, frigate_symbol)
        await asyncio.sleep(1.0)


async def frigate_loop(frigate_symbol: str, asteroid_wp: str) -> None:
    while True:
        await act.navigate_with_prep_async(frigate_symbol, asteroid_wp)
        await asyncio.sleep(0.2)
        await ensure_orbit(frigate_symbol)
        await refine_what_you_can(frigate_symbol)
        ship = await act.get_my_ship_async(frigate_symbol)
        cargo = getattr(getattr(ship, "cargo", None), "units", 0) or 0
        capacity = getattr(getattr(ship, "cargo", None), "capacity", 0) or 0
        if capacity and cargo > max(10, int(0.9 * capacity)):
            await sell_all_high_value(frigate_symbol)
        await asyncio.sleep(1.0)


async def main() -> None:
    init_db()
    # First-pass persist so later steps have data to work with
    bootstrap_initial_state()

    wps = list_db_waypoints()
    print(f"Known waypoints in DB: {len(wps)}")
    for w in wps:
        print(" -", w)

    act.list_ships(api=api_groups.etl)

    frigate = pick_frigate_ship_symbol()
    probe = pick_probe_ship_symbol()
    if not frigate or not probe:
        print("[error] Set FRIGATE_SYMBOL/PROBE_SYMBOL in .env or ensure ships are persisted.")
        return

    sys_sym = await current_system_for(frigate)
    wps_live = await system_waypoints(sys_sym)
    asteroid = next((w for w in wps_live if is_engineered_asteroid(w)), None)
    if not asteroid:
        print("[warn] No ENGINEERED_ASTEROID; falling back to ASTEROID_FIELD/ASTEROID")
        asteroid = next((w for w in wps_live if getattr(w, "type", None) in ("ASTEROID_FIELD", "ASTEROID")), None)
    if not asteroid:
        print("[error] No suitable mining waypoint found.")
        return

    await frigate_buy_drones(frigate, desired_count=3)

    ships = act.list_ships(api=api_groups.api)
    miners = []
    for s in ships:
        if has_mining_laser(s):
            miners.append(getattr(s, "symbol", None))
        if len(miners) >= 4:
            break
    if not miners:
        print("[error] No mining-capable ships found.")
        return

    tasks = [
        asyncio.create_task(probe_market_cycler(probe)),
        asyncio.create_task(miners_loop([m for m in miners if m != frigate], asteroid.symbol, frigate)),
        asyncio.create_task(frigate_loop(frigate, asteroid.symbol)),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
