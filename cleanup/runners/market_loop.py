from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, List

from db.async_session import SessionLocal
from services import writethrough_async as wt
from services import runner_status as rs
from openapi_client.models.navigate_ship_request import NavigateShipRequest

import openapi_client


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
    """Run a blocking SDK call in a thread and apply simple 429 backoff."""
    for _ in range(5):
        try:
            return await asyncio.to_thread(func, *args, **kwargs)
        except openapi_client.exceptions.ApiException as e:
            ra = None
            try:
                headers = getattr(e, "headers", {}) or {}
                ra = headers.get("Retry-After")
            except Exception:
                pass
            delay = float(ra) if ra else 0.7
            await asyncio.sleep(delay)
    raise


def _is_market_wp(wp: Any) -> bool:
    traits = getattr(wp, "traits", []) or []
    return any(getattr(t, "symbol", "") == "MARKETPLACE" for t in traits)


async def navigate_and_wait(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str, waypoint_symbol: str) -> None:
    # Skip if already at target
    try:
        cur = (await api_call(fleet.get_ship_nav, ship_symbol)).data
        if getattr(cur, "waypoint_symbol", None) == waypoint_symbol:
            return
    except Exception:
        pass
    req = NavigateShipRequest(waypointSymbol=waypoint_symbol)
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


async def run_market_polling(client: openapi_client.ApiClient, ship_symbol: str) -> None:
    systems = openapi_client.SystemsApi(client)
    fleet = openapi_client.FleetApi(client)

    # Determine current system from nav
    nav = (await api_call(fleet.get_ship_nav, ship_symbol)).data
    sys_sym = getattr(nav, "system_symbol", None)
    wps = (await api_call(systems.get_system_waypoints, sys_sym)).data
    markets = [w for w in wps if _is_market_wp(w)]
    if not markets:
        return

    idx = 0
    await rs.set_loop_state("market", "running", ship=ship_symbol, system=sys_sym)
    while True:
        target = markets[idx % len(markets)]
        idx += 1
        await rs.log("market.navigate", ship=ship_symbol, to=target.symbol)
        await navigate_and_wait(fleet, ship_symbol, target.symbol)
        await api_call(fleet.dock_ship, ship_symbol)
        await rs.log("market.docked", ship=ship_symbol, at=target.symbol)
        market = (await api_call(systems.get_market, sys_sym, target.symbol)).data
        goods = getattr(market, "trade_goods", None) or []
        exports = getattr(market, "exports", None) or []
        imports = getattr(market, "imports", None) or []
        try:
            async with session_scope() as s:
                count = await wt.upsert_market(s, market)
            print(f"[market] {target.symbol}: trade_goods={len(goods)} exports={len(exports)} imports={len(imports)} snapshots={count}")
        except Exception as e:
            print(f"[market] Persist error at {target.symbol}: {e}")
        await rs.log("market.snapshot", ship=ship_symbol, waypoint=target.symbol, goods=len(goods))
        await asyncio.sleep(0.5)
