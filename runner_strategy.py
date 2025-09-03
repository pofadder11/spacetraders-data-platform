from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable, List, Dict, Optional, Tuple
import math
import json

from dotenv import load_dotenv
from sqlalchemy import select, desc

from session import init_db, SessionLocal
from services.client_service import OpenAPIService
from services.write_through import WriteThrough, default_handlers
from models import MarketTradeGoodCurrent

# OpenAPI request models
from openapi_client.models.navigate_ship_request import NavigateShipRequest
from openapi_client.models.purchase_ship_request import PurchaseShipRequest
from openapi_client.models.transfer_cargo_request import TransferCargoRequest
from openapi_client.models.sell_cargo_request import SellCargoRequest
from openapi_client.models.ship_refine_request import ShipRefineRequest
from openapi_client.models.refuel_ship_request import RefuelShipRequest
from openapi_client.models.ship_type import ShipType
from openapi_client.models.ship_nav_status import ShipNavStatus
from openapi_client.models.waypoint_type import WaypointType
from openapi_client.models.waypoint_trait_symbol import WaypointTraitSymbol


@dataclass
class FleetPick:
    frigate: str
    probe: Optional[str]
    miners: List[str]


def log(msg: str) -> None:
    print(f"[RUNNER] {msg}")


@contextmanager
def session_scope():
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


def my_system_symbol(svc: OpenAPIService) -> str:
    me = svc.d.agents.get_my_agent()
    return "-".join(me.headquarters.split("-")[:2])


def list_waypoints_with_trait(svc: OpenAPIService, system_symbol: str, trait: str) -> List[str]:
    page, limit = 1, 20
    symbols: List[str] = []
    # Convert to enum expected by API serializer
    try:
        trait_enum = WaypointTraitSymbol[trait]
    except Exception:
        trait_enum = WaypointTraitSymbol(trait)
    while True:
        resp = svc.d.systems.get_system_waypoints(system_symbol, page=page, limit=limit, traits=trait_enum)
        if not resp:
            break
        symbols.extend([w.symbol for w in resp])
        if len(resp) < limit:
            break
        page += 1
    return symbols


def list_waypoints_by_type(svc: OpenAPIService, system_symbol: str, waypoint_type: str) -> List[str]:
    page, limit = 1, 20
    symbols: List[str] = []
    # Convert to enum expected by API serializer
    try:
        type_enum = WaypointType[waypoint_type]
    except Exception:
        type_enum = WaypointType(waypoint_type)
    while True:
        resp = svc.d.systems.get_system_waypoints(system_symbol, page=page, limit=limit, type=type_enum)
        if not resp:
            break
        symbols.extend([w.symbol for w in resp])
        if len(resp) < limit:
            break
        page += 1
    return symbols


def list_refuel_stations_coords(svc: OpenAPIService, system_symbol: str) -> List[Tuple[str, int, int]]:
    """
    Return a list of (waypoint_symbol, x, y) for waypoints in-system that can refuel (MARKETPLACE trait).
    Uses get_system_waypoints with trait filter for efficiency.
    """
    page, limit = 1, 20
    coords: List[Tuple[str, int, int]] = []
    try:
        trait_enum = WaypointTraitSymbol.MARKETPLACE
    except Exception:
        trait_enum = WaypointTraitSymbol("MARKETPLACE")
    while True:
        resp = svc.d.systems.get_system_waypoints(system_symbol, page=page, limit=limit, traits=trait_enum)
        if not resp:
            break
        for w in resp:
            coords.append((w.symbol, int(getattr(w, "x", 0)), int(getattr(w, "y", 0))))
        if len(resp) < limit:
            break
        page += 1
    return coords


def _wp_coords(svc: OpenAPIService, system_symbol: str, waypoint_symbol: str) -> Tuple[int, int]:
    w = svc.d.systems.get_waypoint(system_symbol, waypoint_symbol)
    return int(getattr(w, "x", 0)), int(getattr(w, "y", 0))


def _wp_has_marketplace(svc: OpenAPIService, system_symbol: str, waypoint_symbol: str) -> bool:
    try:
        w = svc.d.systems.get_waypoint(system_symbol, waypoint_symbol)
        traits = getattr(w, "traits", []) or []
        for t in traits:
            sym = getattr(t, "symbol", None)
            sval = getattr(sym, "value", sym)
            if str(sval) == "MARKETPLACE":
                return True
    except Exception:
        pass
    return False


def _dist(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _parse_insufficient_fuel(exc: Exception) -> Optional[Dict[str, int]]:
    """
    If exception is an OpenAPI BadRequest with insufficient fuel, return dict with keys
    {"fuelRequired", "fuelAvailable"}. Otherwise None.
    """
    try:
        # openapi_client.exceptions.ApiException stores a parsed dict at .data when available
        body = getattr(exc, "data", None)
        if not body and hasattr(exc, "body"):
            # fallback: try to decode JSON string body
            try:
                body = json.loads(getattr(exc, "body", "") or "{}")
            except Exception:
                body = None
        if isinstance(body, dict):
            err = body.get("error") or {}
            code = err.get("code") or body.get("code")
            data = err.get("data") or body.get("data") or {}
            # 4203 is Navigate requires more fuel
            if int(code) == 4203 and isinstance(data, dict):
                fr = data.get("fuelRequired")
                fa = data.get("fuelAvailable")
                if isinstance(fr, int) and isinstance(fa, int):
                    return {"fuelRequired": fr, "fuelAvailable": fa}
    except Exception:
        pass
    return None


def pick_fleet(svc: OpenAPIService) -> FleetPick:
    ships = svc.d.fleet.get_my_ships()
    frigate: Optional[str] = None
    probe: Optional[str] = None
    miners: List[str] = []

    for s in ships:
        frame = getattr(s, "frame", None)
        fsym = getattr(frame, "symbol", None)
        if fsym == "FRAME_FRIGATE" and not frigate:
            frigate = s.symbol
        elif fsym == "FRAME_PROBE" and not probe:
            probe = s.symbol

        role = getattr(getattr(s, "registration", None), "role", None)
        role_val = str(getattr(role, "value", role)).upper() if role else ""
        if ("MINER" in role_val) or (fsym and ("DRONE" in fsym or "MINER" in fsym)):
            miners.append(s.symbol)

    if not frigate:
        raise RuntimeError("No FRAME_FRIGATE found in fleet.")
    return FleetPick(frigate=frigate, probe=probe, miners=[m for m in miners if m != frigate])


def ensure_orbit(wt: WriteThrough, ship_symbol: str) -> None:
    try:
        wt.fleet.orbit_ship(ship_symbol)
    except Exception:
        pass


def ensure_dock(wt: WriteThrough, ship_symbol: str) -> None:
    try:
        wt.fleet.dock_ship(ship_symbol)
    except Exception:
        pass


def wait_until_arrival(svc: OpenAPIService, ship_symbol: str, poll_sec: float = 5.0, max_wait_sec: float = 900.0) -> None:
    deadline = time.time() + max_wait_sec
    while time.time() < deadline:
        nav = svc.d.fleet.get_ship_nav(ship_symbol)
        if nav.status != ShipNavStatus.IN_TRANSIT:
            return
        time.sleep(poll_sec)


_NAV_SLEEP_UNTIL: Dict[str, float] = {}


def _to_epoch(dt: Optional[datetime]) -> Optional[float]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.timestamp()


def maybe_sleep_for_ship(svc: OpenAPIService, ship_symbol: str) -> None:
    # If we already have a sleep-until recorded, honor it
    now = time.time()
    ts = _NAV_SLEEP_UNTIL.get(ship_symbol)
    if ts and ts > now:
        time.sleep(ts - now)
        return
    # Otherwise, check current nav status and sleep if in-transit
    try:
        nav = svc.d.fleet.get_ship_nav(ship_symbol)
        if nav.status == ShipNavStatus.IN_TRANSIT:
            arr = _to_epoch(getattr(getattr(nav, "route", None), "arrival", None))
            if arr and arr > time.time():
                _NAV_SLEEP_UNTIL[ship_symbol] = arr
                time.sleep(arr - time.time())
                return
    except Exception:
        return


def navigate_to(wt: WriteThrough, svc: OpenAPIService, ship_symbol: str, waypoint_symbol: str) -> None:
    """
    Fuel-aware navigation:
    - If destination is reachable, navigate directly.
    - If not enough fuel:
      - Refuel at current waypoint if possible (market or from cargo).
      - Otherwise, route via the nearest reachable marketplace(s) and refuel along the way.
    - Always blocks until arrival for the final navigation step.
    """

    def _try_navigate_and_wait(target_wp: str) -> Tuple[bool, Optional[Dict[str, int]]]:
        try:
            maybe_sleep_for_ship(svc, ship_symbol)
            ensure_orbit(wt, ship_symbol)
            res = wt.fleet.navigate_ship(ship_symbol, NavigateShipRequest(waypointSymbol=target_wp))
            # success: set sleep-until gate from response
            try:
                arr = _to_epoch(getattr(getattr(res, "nav", None), "route", None).arrival)
                if arr and arr > time.time():
                    _NAV_SLEEP_UNTIL[ship_symbol] = arr
                    time.sleep(max(0.0, arr - time.time()))
                else:
                    wait_until_arrival(svc, ship_symbol)
            except Exception:
                wait_until_arrival(svc, ship_symbol)
            return True, None
        except Exception as e:
            info = _parse_insufficient_fuel(e)
            if info:
                return False, info
            # Other errors: re-raise
            raise

    def _refuel_here_or_from_cargo() -> bool:
        """Attempt to refuel at current waypoint or from cargo. Returns True if fuel increased/full."""
        try:
            nav = svc.d.fleet.get_ship_nav(ship_symbol)
            sys_sym = nav.system_symbol
            cur, cap = get_ship_fuel_levels(svc, ship_symbol)
            if cap and cur and cur >= int(0.99 * cap):
                return True
            # Try dock and refuel at market
            if _wp_has_marketplace(svc, sys_sym, nav.waypoint_symbol):
                ensure_dock(wt, ship_symbol)
                try:
                    wt.fleet.refuel_ship(ship_symbol)
                    return True
                except Exception as e:
                    log(f"Refuel at {nav.waypoint_symbol} failed: {e}")
            # Try refuel from cargo anywhere
            try:
                # Quick check: do we have FUEL in cargo?
                cargo = current_cargo(svc, ship_symbol)
                has_fuel = any(str(it.symbol) == "FUEL" and it.units > 0 for it in cargo.inventory)
                if has_fuel:
                    ensure_dock(wt, ship_symbol)
                    wt.fleet.refuel_ship(ship_symbol, RefuelShipRequest(fromCargo=True))
                    return True
            except Exception:
                pass
        except Exception:
            pass
        return False

    def _route_via_reachable_market_and_refuel(dest_wp: str) -> bool:
        """Find the nearest reachable marketplace from current position, navigate there, refuel, then return True.
        Returns False if none are reachable.
        """
        nav = svc.d.fleet.get_ship_nav(ship_symbol)
        sys_sym = nav.system_symbol
        cur_wp = nav.waypoint_symbol
        cur_xy = _wp_coords(svc, sys_sym, cur_wp)
        dest_xy = _wp_coords(svc, sys_sym, dest_wp)
        markets = list_refuel_stations_coords(svc, sys_sym)
        # Prefer markets that bring us closer to destination and are near the path
        def score(m: Tuple[str, int, int]) -> Tuple[int, float, float]:
            sym, mx, my = m
            m_xy = (mx, my)
            # primary: is closer to dest than current (bool reversed to sort True first)
            closer = 0 if _dist(m_xy, dest_xy) < _dist(cur_xy, dest_xy) else 1
            # secondary: distance from current (shorter first)
            d_cur = _dist(cur_xy, m_xy)
            # tertiary: perpendicular distance to line segment cur->dest (closer to path first)
            # compute projection metric
            try:
                ax, ay = cur_xy
                bx, by = dest_xy
                px, py = m_xy
                vx, vy = bx - ax, by - ay
                wx, wy = px - ax, py - ay
                v2 = vx * vx + vy * vy
                t = 0.0 if v2 == 0 else max(0.0, min(1.0, (wx * vx + wy * vy) / v2))
                projx, projy = ax + t * vx, ay + t * vy
                perp = math.hypot(px - projx, py - projy)
            except Exception:
                perp = d_cur
            return (closer, d_cur, perp)

        candidates = [m for m in markets if m[0] != cur_wp]
        candidates.sort(key=score)

        for sym, _, _ in candidates:
            try:
                log(f"Routing via refuel station: {sym}")
                ok, info = _try_navigate_and_wait(sym)
                if ok:
                    # Arrived at market: refuel then done
                    ensure_dock(wt, ship_symbol)
                    try:
                        wt.fleet.refuel_ship(ship_symbol)
                    except Exception as e:
                        log(f"Refuel at market {sym} failed: {e}")
                    return True
                # If we failed due to insufficient fuel for this candidate, try a nearer one
                if info:
                    continue
            except Exception as e:
                log(f"Navigate to market {sym} error: {e}")
                continue
        return False

    # 1) If already at destination (and not in transit), no-op
    try:
        _nav_now = svc.d.fleet.get_ship_nav(ship_symbol)
        if _nav_now.status != ShipNavStatus.IN_TRANSIT and _nav_now.waypoint_symbol == waypoint_symbol:
            return
    except Exception:
        pass

    # 2) Log whether destination has refuel opportunity (MARKETPLACE)
    try:
        _nav_now = svc.d.fleet.get_ship_nav(ship_symbol)
        dest_has_refuel = _wp_has_marketplace(svc, _nav_now.system_symbol, waypoint_symbol)
        log(f"Destination {waypoint_symbol} refuel available: {'YES' if dest_has_refuel else 'NO'}")
    except Exception:
        pass

    # 3) Try to go directly
    ok, info = _try_navigate_and_wait(waypoint_symbol)
    if ok:
        return

    # 4) Not enough fuel: try to refuel here or from cargo, then retry
    try:
        if _refuel_here_or_from_cargo():
            ok2, _ = _try_navigate_and_wait(waypoint_symbol)
            if ok2:
                return
    except Exception as e:
        log(f"Refuel attempt error: {e}")

    # 5) Route via nearest reachable marketplace(s)
    hopped_markets: set[str] = set()
    max_hops = 5  # safety
    for _ in range(max_hops):
        hopped = _route_via_reachable_market_and_refuel(waypoint_symbol)
        if not hopped:
            break
        # After refuel hop, try to reach destination directly
        ok3, _ = _try_navigate_and_wait(waypoint_symbol)
        if ok3:
            return
        # If still insufficient, loop to choose next market from new position
    # If we get here, we could not plan a route
    if info:
        req, have = info.get("fuelRequired"), info.get("fuelAvailable")
        log(f"Navigation to {waypoint_symbol} blocked by fuel: need {req}, have {have}. No reachable markets.")
    else:
        log(f"Navigation to {waypoint_symbol} failed and no reachable markets found.")


def get_ship_fuel_levels(svc: OpenAPIService, ship_symbol: str) -> Tuple[Optional[int], Optional[int]]:
    try:
        ships = svc.d.fleet.get_my_ships()
        for s in ships:
            if s.symbol == ship_symbol:
                fuel = getattr(s, "fuel", None)
                return (getattr(fuel, "current", None), getattr(fuel, "capacity", None))
    except Exception:
        pass
    return (None, None)


def purchase_miners_at_shipyard(wt: WriteThrough, svc: OpenAPIService, frigate_symbol: str, system_symbol: str, shipyard_wp: str, each: int = 2) -> None:
    ensure_orbit(wt, frigate_symbol)
    navigate_to(wt, svc, frigate_symbol, shipyard_wp)
    ensure_dock(wt, frigate_symbol)

    y = svc.d.systems.get_shipyard(system_symbol, shipyard_wp)
    available_types = {t.type.value for t in y.ship_types} if y and y.ship_types else set()
    buy_types: List[ShipType] = []
    if "SHIP_MINING_DRONE" in available_types:
        buy_types = [ShipType.SHIP_MINING_DRONE] * each
    else:
        log(f"No miners available at {shipyard_wp}: {sorted(list(available_types))}")
        return

    for typ in buy_types:
        try:
            wt.fleet.purchase_ship(PurchaseShipRequest(shipType=typ, waypointSymbol=shipyard_wp))
            log(f"Purchased {typ} at {shipyard_wp}")
        except Exception as e:
            log(f"Purchase failed at {shipyard_wp} ({typ}): {e}")
            break


def current_cargo(svc: OpenAPIService, ship_symbol: str):
    return svc.d.fleet.get_my_ship_cargo(ship_symbol)


def miner_transfer_all_to_frigate(wt: WriteThrough, svc: OpenAPIService, miner: str, frigate: str) -> None:
    maybe_sleep_for_ship(svc, miner)
    maybe_sleep_for_ship(svc, frigate)
    mnav = svc.d.fleet.get_ship_nav(miner)
    fnav = svc.d.fleet.get_ship_nav(frigate)
    if mnav.system_symbol != fnav.system_symbol or mnav.waypoint_symbol != fnav.waypoint_symbol:
        return
    mcargo = current_cargo(svc, miner)
    for item in mcargo.inventory:
        if item.units <= 0:
            continue
        try:
            wt.fleet.transfer_cargo(miner, TransferCargoRequest(tradeSymbol=item.symbol, units=item.units, shipSymbol=frigate))
            log(f"Transferred {item.units} {item.symbol} from {miner} -> {frigate}")
        except Exception as e:
            log(f"Transfer failed {item.symbol} from {miner}: {e}")


def frigate_refine_loop(wt: WriteThrough, svc: OpenAPIService, frigate: str) -> None:
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
    cargo = current_cargo(svc, frigate)
    tried: set[str] = set()
    for item in cargo.inventory:
        out = refine_map.get(str(item.symbol))
        if not out or out in tried:
            continue
        try:
            wt.fleet.ship_refine(frigate, ShipRefineRequest(produce=out))
            tried.add(out)
            log(f"Refined -> {out}")
        except Exception as e:
            log(f"Refine {out} failed: {e}")


def choose_best_markets_for_cargo(system_symbol: str, cargo_items: Iterable, limit_per_good: int = 1) -> Dict[str, List[Tuple[str, int]]]:
    plan: Dict[str, List[Tuple[str, int]]] = {}
    with session_scope() as s:
        for item in cargo_items:
            sym = str(item.symbol)
            rows = (
                s.execute(
                    select(MarketTradeGoodCurrent)
                    .where(MarketTradeGoodCurrent.trade_symbol == sym)
                    .order_by(desc(MarketTradeGoodCurrent.sell_price))
                )
                .scalars()
                .all()
            )
            candidates = [r for r in rows if r.waypoint_symbol.startswith(system_symbol + "-")] or rows
            targets = candidates[:limit_per_good]
            for r in targets:
                plan.setdefault(r.waypoint_symbol, []).append((sym, item.units))
    return plan


def sell_cargo_at_market(wt: WriteThrough, svc: OpenAPIService, ship_symbol: str, market_wp: str, sell_list: List[Tuple[str, int]]) -> None:
    navigate_to(wt, svc, ship_symbol, market_wp)
    ensure_dock(wt, ship_symbol)
    for sym, units in sell_list:
        if units <= 0:
            continue
        try:
            wt.fleet.sell_cargo(ship_symbol, SellCargoRequest(symbol=sym, units=units))
            log(f"Sold {units} {sym} at {market_wp}")
        except Exception as e:
            log(f"Sell {sym} failed at {market_wp}: {e}")


def miner_loop(wt: WriteThrough, svc: OpenAPIService, miner: str, asteroid_wp: str, frigate: str) -> None:
    try:
        navigate_to(wt, svc, miner, asteroid_wp)
        ensure_orbit(wt, miner)
        while True:
            try:
                wt.fleet.extract_resources(miner)
                log(f"{miner} extracted")
            except Exception as e:
                log(f"{miner} extract error: {e}")
            miner_transfer_all_to_frigate(wt, svc, miner, frigate)
            time.sleep(8)
    except Exception as e:
        log(f"miner loop error ({miner}): {e}")


def probe_market_scan_loop(wt: WriteThrough, svc: OpenAPIService, probe: str, system_symbol: str) -> None:
    if not probe:
        log("No probe available, skipping probe loop")
        return
    markets = list_waypoints_with_trait(svc, system_symbol, "MARKETPLACE")
    if not markets:
        log("No MARKETPLACE waypoints found")
        return

    i = 0
    while True:
        wp = markets[i % len(markets)]
        try:
            navigate_to(wt, svc, probe, wp)
            ensure_dock(wt, probe)
            wt.systems.get_market(system_symbol, wp)
            log(f"Scanned market: {wp}")
        except Exception as e:
            log(f"Probe market scan error at {wp}: {e}")
        i += 1
        time.sleep(5)


def frigate_strategy(wt: WriteThrough, svc: OpenAPIService, frigate_symbol: str, system_symbol: str) -> None:
    yards = list_waypoints_with_trait(svc, system_symbol, "SHIPYARD")
    for y in yards:
        purchase_miners_at_shipyard(wt, svc, frigate_symbol, system_symbol, y, each=2)

    asteroids = list_waypoints_by_type(svc, system_symbol, "ENGINEERED_ASTEROID")
    if not asteroids:
        log("No ENGINEERED_ASTEROID found")
        return
    eng_ast = asteroids[0]
    navigate_to(wt, svc, frigate_symbol, eng_ast)
    ensure_orbit(wt, frigate_symbol)

    while True:
        maybe_sleep_for_ship(svc, frigate_symbol)
        try:
            frigate_refine_loop(wt, svc, frigate_symbol)
        except Exception as e:
            log(f"Frigate refine error: {e}")

        c = current_cargo(svc, frigate_symbol)
        capacity = c.capacity
        if c.units >= int(0.8 * capacity) or c.units == capacity:
            sell_plan = choose_best_markets_for_cargo(system_symbol, c.inventory)
            for market_wp, items in sell_plan.items():
                sell_cargo_at_market(wt, svc, frigate_symbol, market_wp, items)
            navigate_to(wt, svc, frigate_symbol, eng_ast)
            ensure_orbit(wt, frigate_symbol)

        time.sleep(6)


async def amain() -> None:
    load_dotenv()
    init_db()

    svc = OpenAPIService()
    wt = WriteThrough(svc, SessionLocal, handlers=default_handlers())

    system_symbol = my_system_symbol(svc)
    pick = pick_fleet(svc)

    log(f"System: {system_symbol}")
    log(f"FRIGATE: {pick.frigate} | PROBE: {pick.probe} | MINERS: {pick.miners}")

    # Persist system metadata (write-through handler upserts DbSystem)
    try:
        svc.d.systems.get_system(system_symbol)
    except Exception:
        pass

    # Show refuelling stations in this system (symbols and coordinates)
    try:
        stations = list_refuel_stations_coords(svc, system_symbol)
        if stations:
            log("Refuelling stations (MARKETPLACE):")
            for sym, x, y in sorted(stations, key=lambda t: t[0]):
                print(f"  - {sym}: ({x}, {y})")
        else:
            log("No refuelling stations (MARKETPLACE) discovered in system")
    except Exception as e:
        log(f"Listing refuelling stations failed: {e}")

    asteroids = list_waypoints_by_type(svc, system_symbol, "ENGINEERED_ASTEROID")
    if not asteroids:
        log("No ENGINEERED_ASTEROID in system; exiting")
        return
    eng_ast = asteroids[0]

    loop = asyncio.get_running_loop()

    async def run_in_thread(fn, *args, **kwargs):
        return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))

    tasks = []
    if pick.probe:
        tasks.append(asyncio.create_task(run_in_thread(probe_market_scan_loop, wt, svc, pick.probe, system_symbol)))
    tasks.append(asyncio.create_task(run_in_thread(frigate_strategy, wt, svc, pick.frigate, system_symbol)))
    for m in pick.miners:
        tasks.append(asyncio.create_task(run_in_thread(miner_loop, wt, svc, m, eng_ast, pick.frigate)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        log("Shutting down.")
