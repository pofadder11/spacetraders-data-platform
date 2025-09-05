from __future__ import annotations

# %% [markdown]
# Test: Probe fetches market payload at a marketplace waypoint
#
# Requirements:
# - .env with BEARER_TOKEN
# - Installs: openapi_client, python-dotenv

# %%
import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
import openapi_client
from openapi_client.models.navigate_ship_request import NavigateShipRequest
from openapi_client.models.waypoint_trait_symbol import WaypointTraitSymbol

load_dotenv()


async def to_thread(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


async def navigate_and_wait(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str, waypoint_symbol: str) -> None:
    # Skip if already at target
    try:
        cur = (await to_thread(fleet.get_ship_nav, ship_symbol)).data
        if getattr(cur, "waypoint_symbol", None) == waypoint_symbol:
            return
    except Exception:
        pass
    req = NavigateShipRequest(waypointSymbol=waypoint_symbol)
    resp = await to_thread(fleet.navigate_ship, ship_symbol, req)
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
        print(f"[nav] Waiting ~{wait:.1f}s for arrival...")
        await asyncio.sleep(wait + 1)


async def ensure_docked(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str) -> None:
    nav = (await to_thread(fleet.get_ship_nav, ship_symbol)).data
    if getattr(nav, "status", None) == "DOCKED":
        return
    await to_thread(fleet.dock_ship, ship_symbol)


async def pick_probe(fleet: openapi_client.api.fleet_api.FleetApi) -> Optional[str]:
    ships = (await to_thread(fleet.get_my_ships)).data
    for s in ships:
        frame = getattr(getattr(s, "frame", None), "symbol", "") or ""
        if "PROBE" in frame.upper():
            return getattr(s, "symbol", None)
    return getattr(ships[0], "symbol", None) if ships else None


async def pick_market_waypoint(systems: openapi_client.api.systems_api.SystemsApi, system_symbol: str) -> Optional[str]:
    try:
        resp = await to_thread(systems.get_system_waypoints, system_symbol, traits=WaypointTraitSymbol.MARKETPLACE)
        data = getattr(resp, "data", None) or resp.data
    except Exception:
        resp = await to_thread(systems.get_system_waypoints, system_symbol)
        data = getattr(resp, "data", None) or resp.data
    for w in data or []:
        traits = getattr(w, "traits", []) or []
        if any(getattr(t, "symbol", "") == "MARKETPLACE" for t in traits):
            return getattr(w, "symbol", None)
    return None


async def main_market_probe() -> None:
    token = os.getenv("BEARER_TOKEN")
    if not token:
        raise RuntimeError("Missing BEARER_TOKEN in environment")

    cfg = openapi_client.Configuration(access_token=token)
    client = openapi_client.ApiClient(cfg)
    systems = openapi_client.SystemsApi(client)
    fleet = openapi_client.FleetApi(client)
    agents = openapi_client.AgentsApi(client)

    ships = (await to_thread(fleet.get_my_ships)).data
    if not ships:
        print("[err] No ships found.")
        return
    ship_symbol = await pick_probe(fleet)
    # Prefer using cached system symbol from env to avoid extra API calls
    sys_sym = os.getenv("SYSTEM_SYMBOL")
    if not sys_sym:
        me = (await to_thread(agents.get_my_agent)).data
        hq = getattr(me, "headquarters", None)
        sys_sym = "-".join(hq.split("-")[:2]) if hq else None
    print(f"[info] Using ship={ship_symbol} in system={sys_sym}")

    target_wp = await pick_market_waypoint(systems, sys_sym)
    if not target_wp:
        print("[err] No marketplace waypoint found in this system.")
        return
    print(f"[step] Navigating to market {target_wp}...")
    await navigate_and_wait(fleet, ship_symbol, target_wp)
    print("[step] Docking...")
    await ensure_docked(fleet, ship_symbol)

    for attempt in range(5):
        market = (await to_thread(systems.get_market, sys_sym, target_wp)).data
        goods = getattr(market, "trade_goods", None) or []
        print(f"[market] attempt={attempt+1} goods={len(goods)} exports={len(market.exports or [])} imports={len(market.imports or [])}")
        if goods:
            print("[ok] Market payload includes trade_goods. Sample:")
            for g in goods[:5]:
                print("   -", getattr(g, "symbol", None), "sell=", getattr(g, "sell_price", None))
            break
        await asyncio.sleep(1.0)
    else:
        print("[warn] No trade_goods visible; ensure ship is docked at a MARKETPLACE waypoint.")


if __name__ == "__main__":
    asyncio.run(main_market_probe())
