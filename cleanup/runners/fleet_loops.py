from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, Iterable, List, Optional

import openapi_client
from openapi_client.models.navigate_ship_request import NavigateShipRequest
from openapi_client.models.sell_cargo_request import SellCargoRequest
from openapi_client.models.transfer_cargo_request import TransferCargoRequest
from openapi_client.models.ship_refine_request import ShipRefineRequest
from openapi_client.models.ship_nav_status import ShipNavStatus
from openapi_client.models.waypoint_trait_symbol import WaypointTraitSymbol
from openapi_client.models.refuel_ship_request import RefuelShipRequest

from db.async_session import SessionLocal
from services import writethrough_async as wt
from services import runner_status as rs
from sqlalchemy import select, func
from models import MarketTradeGoodCurrent


@asynccontextmanager
async def session_scope():
    async with SessionLocal() as sess:
        try:
            yield sess
            await sess.commit()
        except Exception:
            await sess.rollback()
            raise


async def api_call(func, *args, **kwargs):
    """Run a blocking SDK call in a thread with basic 429 Retry-After backoff.

    Retries a few times on ApiException, using Retry-After when provided.
    Re-raises the last exception after exhausting retries.
    """
    last_exc: Exception | None = None
    for _ in range(6):
        try:
            return await asyncio.to_thread(func, *args, **kwargs)
        except openapi_client.exceptions.ApiException as e:
            last_exc = e
            ra = None
            try:
                headers = getattr(e, "headers", {}) or {}
                ra = headers.get("Retry-After")
            except Exception:
                pass
            delay = float(ra) if ra else 0.7
            await asyncio.sleep(delay)
        except Exception as e:
            last_exc = e
            await asyncio.sleep(0.5)
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("api_call exhausted retries without an exception")


def _has_mining_laser(ship: Any) -> bool:
    mounts = getattr(ship, "mounts", []) or []
    return any("MINING_LASER" in getattr(m, "symbol", "") for m in mounts)


def _is_miner(ship: Any) -> bool:
    # True if has mining laser OR is a mining drone OR role suggests mining
    if _has_mining_laser(ship):
        return True
    frame = getattr(getattr(ship, "frame", None), "symbol", "") or ""
    if "MINING_DRONE" in frame.upper() or "DRONE" in frame.upper():
        return True
    role = getattr(getattr(ship, "registration", None), "role", None)
    if str(role).upper() in ("EXCAVATOR", "HARVESTER"):
        return True
    return False


def _is_market_wp(wp: Any) -> bool:
    traits = getattr(wp, "traits", []) or []
    return any(getattr(t, "symbol", "") == "MARKETPLACE" for t in traits)


def _is_engineered_asteroid(wp: Any) -> bool:
    return getattr(wp, "type", None) == "ENGINEERED_ASTEROID"


def _is_shipyard_wp(wp: Any) -> bool:
    traits = getattr(wp, "traits", []) or []
    return any(getattr(t, "symbol", "") == "SHIPYARD" for t in traits)


async def get_nav(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str):
    return (await api_call(fleet.get_ship_nav, ship_symbol)).data


async def ensure_not_in_transit(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str) -> None:
    for _ in range(20):
        nav = await get_nav(fleet, ship_symbol)
        if getattr(nav, "status", None) != ShipNavStatus.IN_TRANSIT:
            return
        await asyncio.sleep(1.0)


async def ensure_docked(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str) -> None:
    await ensure_not_in_transit(fleet, ship_symbol)
    nav = await get_nav(fleet, ship_symbol)
    if getattr(nav, "status", None) == ShipNavStatus.DOCKED:
        return
    for _ in range(6):
        try:
            await api_call(fleet.dock_ship, ship_symbol)
        except openapi_client.exceptions.ApiException as e:
            ra = None
            try:
                ra = getattr(e, "headers", {}).get("Retry-After")
            except Exception:
                pass
            await asyncio.sleep(float(ra) if ra else 0.7)
        nav = await get_nav(fleet, ship_symbol)
        if getattr(nav, "status", None) == ShipNavStatus.DOCKED:
            return


async def ensure_orbit(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str) -> None:
    await ensure_not_in_transit(fleet, ship_symbol)
    nav = await get_nav(fleet, ship_symbol)
    if getattr(nav, "status", None) == ShipNavStatus.IN_ORBIT:
        return
    for _ in range(6):
        try:
            await api_call(fleet.orbit_ship, ship_symbol)
            return
        except openapi_client.exceptions.ApiException as e:
            ra = None
            try:
                ra = getattr(e, "headers", {}).get("Retry-After")
            except Exception:
                pass
            await asyncio.sleep(float(ra) if ra else 0.7)


async def refuel_if_needed(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str) -> None:
    """If ship uses fuel and not full, dock, refuel, and return to orbit."""
    ship = (await api_call(fleet.get_my_ship, ship_symbol)).data
    fuel = getattr(ship, "fuel", None)
    cap = getattr(fuel, "capacity", None)
    cur = getattr(fuel, "current", None)
    if cap is not None and cap > 0 and cur is not None and cur < cap:
        await ensure_docked(fleet, ship_symbol)
        try:
            await api_call(fleet.refuel_ship, ship_symbol, RefuelShipRequest())
            await rs.log("fuel.refuel", ship=ship_symbol, before=cur, capacity=cap)
        except Exception:
            pass
        await asyncio.sleep(0.3)
        await ensure_orbit(fleet, ship_symbol)


async def wait_cooldown(cooldown: Any) -> None:
    """Sleep for cooldown remaining if provided."""
    if cooldown is None:
        return
    rem = getattr(cooldown, "remaining_seconds", None)
    if rem is not None and rem > 0:
        await asyncio.sleep(float(rem) + 0.5)
        return
    # Fallback to expiration timestamp
    exp = getattr(cooldown, "expiration", None)
    if exp is not None:
        import datetime as _dt
        now = _dt.datetime.now(_dt.timezone.utc)
        if getattr(exp, "tzinfo", None) is None:
            exp = exp.replace(tzinfo=_dt.timezone.utc)
        wait = max(0.0, (exp - now).total_seconds())
        if wait > 0:
            await asyncio.sleep(wait + 0.5)


async def navigate_and_wait(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str, waypoint_symbol: str) -> None:
    # If already at target waypoint, skip navigation
    try:
        cur = (await api_call(fleet.get_ship_nav, ship_symbol)).data
        if getattr(cur, "waypoint_symbol", None) == waypoint_symbol:
            await rs.log("nav.skip_same_waypoint", ship=ship_symbol, at=waypoint_symbol)
            return
    except Exception:
        pass
    req = NavigateShipRequest(waypointSymbol=waypoint_symbol)
    await rs.log("nav.start", ship=ship_symbol, to=waypoint_symbol)
    # Navigation prep: refuel if applicable
    try:
        await refuel_if_needed(fleet, ship_symbol)
    except Exception:
        pass
    resp = await api_call(fleet.navigate_ship, ship_symbol, req)
    data = getattr(resp, "data", resp)
    nav = getattr(data, "nav", None)
    route = getattr(nav, "route", None) if nav else None
    arrival = getattr(route, "arrival", None) if route else None
    if arrival is not None:
        import datetime as _dt
        now = _dt.datetime.now(_dt.timezone.utc)
        if getattr(arrival, "tzinfo", None) is None:
            arrival = arrival.replace(tzinfo=_dt.timezone.utc)
        wait = max(0.0, (arrival - now).total_seconds())
        await asyncio.sleep(wait + 1)
    await ensure_not_in_transit(fleet, ship_symbol)
    await rs.log("nav.arrived", ship=ship_symbol, at=waypoint_symbol)


async def jettison_low_value(client: openapi_client.ApiClient, ship_symbol: str) -> None:
    fleet = openapi_client.FleetApi(client)
    ship = (await api_call(fleet.get_my_ship, ship_symbol)).data
    inv = getattr(getattr(ship, "cargo", None), "inventory", []) or []
    if not inv:
        return
    # Compute 25th percentile of known prices from DB
    symbols = [getattr(i, "symbol", None) for i in inv if getattr(i, "symbol", None)]
    if not symbols:
        return
    async with session_scope() as s:
        prices: List[int] = []
        price_map: dict[str, Optional[int]] = {}
        for ts in symbols:
            row = (
                await s.execute(
                    select(func.max(MarketTradeGoodCurrent.sell_price)).where(MarketTradeGoodCurrent.trade_symbol == ts)
                )
            ).scalar()
            val = int(row) if row is not None else None
            price_map[ts] = val
            if val is not None:
                prices.append(val)
        if prices:
            v = sorted(prices)
            cut = v[max(0, int(0.25 * (len(v) - 1)))]
        else:
            cut = 0
    # Jettison items below cutoff or unknown
    for item in inv:
        ts = getattr(item, "symbol", None)
        units = getattr(item, "units", 0) or 0
        if not ts or units <= 0:
            continue
        val = price_map.get(ts)
        if val is None or val <= cut:
            try:
                from openapi_client.models.jettison_request import JettisonRequest
                await api_call(fleet.jettison, ship_symbol, JettisonRequest(symbol=ts, units=units))
                await asyncio.sleep(0.2)
                await rs.log("cargo.jettison", ship=ship_symbol, symbol=ts, units=units)
            except Exception:
                pass


async def transfer_all_to(client: openapi_client.ApiClient, ship_from: str, ship_to: str) -> None:
    fleet = openapi_client.FleetApi(client)
    ship = (await api_call(fleet.get_my_ship, ship_from)).data
    inv = getattr(getattr(ship, "cargo", None), "inventory", []) or []
    for item in inv:
        ts = getattr(item, "symbol", None)
        units = getattr(item, "units", 0) or 0
        if not ts or units <= 0:
            continue
        try:
            req = TransferCargoRequest(trade_symbol=ts, units=units, ship_symbol=ship_to)
            await api_call(fleet.transfer_cargo, ship_from, req)
            await asyncio.sleep(0.2)
            await rs.log("cargo.transfer", ship_from=ship_from, ship_to=ship_to, symbol=ts, units=units)
        except Exception:
            pass


async def refine_what_you_can(client: openapi_client.ApiClient, frigate_symbol: str) -> None:
    fleet = openapi_client.FleetApi(client)
    ship = (await api_call(fleet.get_my_ship, frigate_symbol)).data
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
        "ICE_WATER": "FUEL",
    }
    for raw, out in refine_map.items():
        if have.get(raw):
            try:
                await api_call(fleet.ship_refine, frigate_symbol, ShipRefineRequest(produce=out))
                await asyncio.sleep(0.3)
                await rs.log("refine", ship=frigate_symbol, produce=out)
            except Exception:
                pass


async def sell_all_high_value(client: openapi_client.ApiClient, frigate_symbol: str) -> None:
    systems = openapi_client.SystemsApi(client)
    fleet = openapi_client.FleetApi(client)
    nav = (await api_call(fleet.get_ship_nav, frigate_symbol)).data
    sys_sym = getattr(nav, "system_symbol", None)
    wps = (await api_call(systems.get_system_waypoints, sys_sym)).data
    markets = [w for w in wps if _is_market_wp(w)]
    if not markets:
        return
    ship = (await api_call(fleet.get_my_ship, frigate_symbol)).data
    inv = getattr(getattr(ship, "cargo", None), "inventory", []) or []
    for item in inv:
        ts = getattr(item, "symbol", None)
        units = getattr(item, "units", 0) or 0
        if not ts or units <= 0:
            continue
        best = None
        best_price = -1
        async with session_scope() as s:
            for w in markets:
                price = (
                    await s.execute(
                        select(MarketTradeGoodCurrent.sell_price).where(
                            MarketTradeGoodCurrent.waypoint_symbol == w.symbol,
                            MarketTradeGoodCurrent.trade_symbol == ts,
                        )
                    )
                ).scalar()
                if price is not None and price > best_price:
                    best_price = price
                    best = w
        if best is None:
            continue
        await navigate_and_wait(fleet, frigate_symbol, best.symbol)
        await ensure_docked(fleet, frigate_symbol)
        try:
            await api_call(fleet.sell_cargo, frigate_symbol, SellCargoRequest(symbol=ts, units=units))
            await asyncio.sleep(0.2)
            await rs.log("sell", ship=frigate_symbol, symbol=ts, units=units, price=best_price)
        except Exception:
            pass


async def miners_loop(client: openapi_client.ApiClient, miner_symbols: list[str], asteroid_wp: str, frigate_symbol: str) -> None:
    fleet = openapi_client.FleetApi(client)
    while True:
        # Move miners to target and ensure orbit
        for sym in miner_symbols:
            await navigate_and_wait(fleet, sym, asteroid_wp)
        for sym in miner_symbols:
            await ensure_orbit(fleet, sym)
        # Extract resources
        for sym in miner_symbols:
            try:
                resp = await api_call(fleet.extract_resources, sym)
                data = getattr(resp, "data", resp)  # has cargo, cooldown, extraction
                cargo = getattr(data, "cargo", None)
                cooldown = getattr(data, "cooldown", None)
                extraction = getattr(data, "extraction", None)
                ex_yield = getattr(extraction, "var_yield", None) if extraction else None
                async with session_scope() as s:
                    if cargo is not None:
                        await wt.update_ship_current_cargo_units(s, sym, getattr(cargo, "units", None))
                        await wt.upsert_ship_cargo_current(s, sym, cargo)
                    if ex_yield is not None:
                        await wt.insert_extraction_yield(
                            s,
                            sym,
                            getattr(ex_yield, "symbol", None),
                            getattr(ex_yield, "units", 0) or 0,
                            cooldown,
                        )
                await rs.log("extract", ship=sym, yield_symbol=getattr(ex_yield, "symbol", None), units=getattr(ex_yield, "units", None))
                # Respect cooldown after extraction
                await wait_cooldown(cooldown)
            except Exception:
                pass
        # Housekeeping: jettison low-value and transfer when co-located with frigate
        for sym in miner_symbols:
            await jettison_low_value(client, sym)
            nav_m = (await api_call(fleet.get_ship_nav, sym)).data
            nav_f = (await api_call(fleet.get_ship_nav, frigate_symbol)).data
            if getattr(nav_m, "waypoint_symbol", None) == getattr(nav_f, "waypoint_symbol", None):
                await transfer_all_to(client, sym, frigate_symbol)
        # Sleep a short interval to avoid hammering
        await asyncio.sleep(1.0)


async def frigate_loop(client: openapi_client.ApiClient, frigate_symbol: str, asteroid_wp: str) -> None:
    fleet = openapi_client.FleetApi(client)
    while True:
        # Scan waypoints periodically to populate DB (once per cycle if cooldown allows)
        try:
            # Check for Sensor Array mount before scanning
            ship = (await api_call(fleet.get_my_ship, frigate_symbol)).data
            mounts = getattr(ship, "mounts", []) or []
            has_sensor = any("SENSOR_ARRAY" in str(getattr(m, "symbol", "")).upper() for m in mounts)
            if not has_sensor:
                await rs.log("scan.skipped_no_sensor", ship=frigate_symbol)
            else:
                resp = await api_call(fleet.create_ship_waypoint_scan, frigate_symbol)
                waypoints = getattr(resp, "waypoints", None)
                cooldown = getattr(resp, "cooldown", None)
                if waypoints:
                    async with session_scope() as s:
                        await wt.upsert_waypoints(s, waypoints)
                await rs.log("scan.waypoints", ship=frigate_symbol, count=len(waypoints or []))
                await wait_cooldown(cooldown)
        except openapi_client.exceptions.ApiException as e:
            await rs.log("scan.error", ship=frigate_symbol, error=str(e), body=getattr(e, "body", None))

        # Navigate to asteroid, refine, and possibly sell
        await navigate_and_wait(fleet, frigate_symbol, asteroid_wp)
        await ensure_orbit(fleet, frigate_symbol)
        await refine_what_you_can(client, frigate_symbol)
        ship = (await api_call(fleet.get_my_ship, frigate_symbol)).data
        cargo = getattr(getattr(ship, "cargo", None), "units", 0) or 0
        capacity = getattr(getattr(ship, "cargo", None), "capacity", 0) or 0
        if capacity and cargo > max(10, int(0.9 * capacity)):
            await sell_all_high_value(client, frigate_symbol)
        await asyncio.sleep(1.0)


def select_frigate_and_miners(ships: Iterable[Any]) -> tuple[Optional[str], list[str]]:
    frigate: Optional[str] = None
    miners: list[str] = []
    for s in ships:
        sym = getattr(s, "symbol", None)
        role = getattr(getattr(s, "registration", None), "role", None)
        if frigate is None and role in ("REFINERY", "COMMAND", "HAULER"):
            frigate = sym
        if _has_mining_laser(s):
            miners.append(sym)
    # Keep at most 4 miners
    miners = [m for m in miners if m and m != frigate][:4]
    return frigate, miners


async def find_asteroid_waypoint(client: openapi_client.ApiClient, system_symbol: str) -> Optional[str]:
    systems = openapi_client.SystemsApi(client)
    wps = (await api_call(systems.get_system_waypoints, system_symbol)).data
    ea = next((w for w in wps if _is_engineered_asteroid(w)), None)
    if ea:
        return ea.symbol
    alt = next((w for w in wps if getattr(w, "type", None) in ("ASTEROID_FIELD", "ASTEROID")), None)
    return getattr(alt, "symbol", None) if alt else None


def select_probe_frigate_by_frame(ships: Iterable[Any]) -> tuple[Optional[str], Optional[str]]:
    probe: Optional[str] = None
    frigate: Optional[str] = None
    for s in ships:
        sym = getattr(s, "symbol", None)
        frame = getattr(getattr(s, "frame", None), "symbol", "") or ""
        up = str(frame).upper()
        if probe is None and "PROBE" in up:
            probe = sym
        if frigate is None and "FRIGATE" in up:
            frigate = sym
    return probe, frigate


def miners_from_ships(ships: Iterable[Any], exclude_symbol: Optional[str]) -> list[str]:
    out: list[str] = []
    for s in ships:
        sym = getattr(s, "symbol", None)
        if not sym or (exclude_symbol and sym == exclude_symbol):
            continue
        if _is_miner(s):
            out.append(sym)
    return out[:4]


async def frigate_buy_drones(
    client: openapi_client.ApiClient,
    frigate_symbol: str,
    system_symbol: str,
    desired_count: int = 3,
) -> int:
    """Visit shipyards and purchase SHIP_MINING_DRONE until total >= desired_count.

    Returns the number of drones purchased in this call (best effort).
    """
    systems = openapi_client.SystemsApi(client)
    fleet = openapi_client.FleetApi(client)
    from openapi_client.models.ship_type import ShipType
    from openapi_client.models.purchase_ship_request import PurchaseShipRequest

    # Count existing drones by frame containing DRONE
    ships = (await api_call(fleet.get_my_ships)).data
    def _is_drone(ship: Any) -> bool:
        f = getattr(getattr(ship, "frame", None), "symbol", "") or ""
        return "DRONE" in str(f).upper()
    existing = sum(1 for s in ships if _is_drone(s))
    to_buy = max(0, desired_count - existing)
    if to_buy <= 0:
        return 0

    print(f"[shipyard] Scanning system {system_symbol} for shipyards with frigate {frigate_symbol}")
    # Query waypoints with an explicit trait filter, then fall back to client-side filtering
    try:
        wps = (await api_call(
            systems.get_system_waypoints,
            system_symbol,
            traits=WaypointTraitSymbol.SHIPYARD,
        )).data
    except Exception:
        wps = (await api_call(systems.get_system_waypoints, system_symbol)).data
    yards = [w for w in wps if _is_shipyard_wp(w)]
    print(f"[shipyard] Found {len(yards)} shipyard waypoints")
    bought = 0
    for yard in yards:
        if bought >= to_buy:
            break
        # Travel + dock
        print(f"[shipyard] Navigating to {yard.symbol}...")
        try:
            await navigate_and_wait(fleet, frigate_symbol, yard.symbol)
        except Exception as e:
            print(f"[shipyard] Navigation failed to {yard.symbol}: {e}; moving on.")
            continue
        await ensure_docked(fleet, frigate_symbol)
        print(f"[shipyard] Docked at {yard.symbol}. Querying shipyard...")
        # Check if yard sells mining drones
        try:
            y = (await api_call(systems.get_shipyard, system_symbol, yard.symbol)).data
        except Exception:
            print(f"[shipyard] Failed to get shipyard data at {yard.symbol}")
            continue
        # Persist shipyard offers
        try:
            from services import writethrough_async as wt
            async with session_scope() as s:
                c = await wt.upsert_shipyard_offers(s, y)
                print(f"[shipyard] Upserted {c} offers for {yard.symbol}")
        except Exception as e:
            print(f"[shipyard] Persist error at {yard.symbol}: {e}")
        available: list[str] = []
        if getattr(y, "ship_types", None):
            available = [getattr(t, "type", None) for t in y.ship_types]
        elif getattr(y, "ships", None):
            available = [getattr(s, "type", None) for s in y.ships]
        print(f"[shipyard] Available types at {yard.symbol}: {available}")
        if ShipType.SHIP_MINING_DRONE not in available:
            print(f"[shipyard] No mining drones at {yard.symbol}, moving on.")
            continue
        # Attempt purchase
        try:
            await api_call(fleet.purchase_ship, PurchaseShipRequest(ship_type=ShipType.SHIP_MINING_DRONE, waypoint_symbol=yard.symbol))
            bought += 1
            print(f"[shipyard] Purchased mining drone at {yard.symbol} ({bought}/{to_buy})")
            await asyncio.sleep(0.5)
        except Exception:
            # credits or cooldown issues: move on
            print(f"[shipyard] Purchase failed at {yard.symbol}, moving on.")
            await asyncio.sleep(0.5)
            continue
    return bought
