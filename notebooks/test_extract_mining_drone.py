from __future__ import annotations

# %% [markdown]
# Test: Mining drone extract_resources payload and cooldown

# %%
import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
import openapi_client
from openapi_client.models.navigate_ship_request import NavigateShipRequest

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


async def ensure_orbit(fleet: openapi_client.api.fleet_api.FleetApi, ship_symbol: str) -> None:
    nav = (await to_thread(fleet.get_ship_nav, ship_symbol)).data
    if getattr(nav, "status", None) == "IN_ORBIT":
        return
    await to_thread(fleet.orbit_ship, ship_symbol)


async def wait_cooldown(cooldown) -> None:
    if cooldown is None:
        return
    rem = getattr(cooldown, "remaining_seconds", None)
    if rem is not None and rem > 0:
        print(f"[cooldown] waiting {rem}s")
        await asyncio.sleep(float(rem) + 0.5)


async def pick_miner(fleet: openapi_client.api.fleet_api.FleetApi) -> Optional[str]:
    ships = (await to_thread(fleet.get_my_ships)).data
    for s in ships:
        frame = getattr(getattr(s, "frame", None), "symbol", "") or ""
        mounts = getattr(s, "mounts", []) or []
        if "DRONE" in frame.upper() or any("MINING_LASER" in str(getattr(m, "symbol", "")).upper() for m in mounts):
            return getattr(s, "symbol", None)
    return getattr(ships[0], "symbol", None) if ships else None


async def pick_asteroid(systems: openapi_client.api.systems_api.SystemsApi, system_symbol: str) -> Optional[str]:
    resp = await to_thread(systems.get_system_waypoints, system_symbol)
    data = getattr(resp, "data", None) or resp.data
    for w in data or []:
        if getattr(w, "type", None) in ("ENGINEERED_ASTEROID", "ASTEROID_FIELD", "ASTEROID"):
            return getattr(w, "symbol", None)
    return None


async def main_extract() -> None:
    token = os.getenv("BEARER_TOKEN")
    if not token:
        raise RuntimeError("Missing BEARER_TOKEN")
    cfg = openapi_client.Configuration(access_token=token)
    client = openapi_client.ApiClient(cfg)
    systems = openapi_client.SystemsApi(client)
    fleet = openapi_client.FleetApi(client)
    agents = openapi_client.AgentsApi(client)

    miner = await pick_miner(fleet)
    print("The miner is: ", miner)
    if not miner:
        print("[err] No miner-like ship found.")
        return
    # Determine system symbol via agent (preferred) to avoid extra calls
    me = (await to_thread(agents.get_my_agent)).data
    hq = getattr(me, "headquarters", None)
    sys_sym = "-".join(hq.split("-")[:2]) if hq else None
    target = await pick_asteroid(systems, sys_sym)
    if not target:
        print("[err] No asteroid-like waypoint found in system.")
        return
    print(f"[info] Using miner {miner}; navigating to {target}")
    await navigate_and_wait(fleet, miner, target)
    await ensure_orbit(fleet, miner)

    try:
        resp = await to_thread(fleet.extract_resources, miner)
    except openapi_client.exceptions.ApiException as e:
        print("[err] extract API error:", getattr(e, "body", str(e)))
        return
    data = getattr(resp, "data", resp)
    cooldown = getattr(data, "cooldown", None)
    cargo = getattr(data, "cargo", None)
    extraction = getattr(data, "extraction", None)
    print("[ok] Extracted; cooldown:", getattr(cooldown, "remaining_seconds", None))
    print("   cargo units:", getattr(cargo, "units", None))
    if extraction is not None:
        y = getattr(extraction, "var_yield", None)
        print("   yield:", getattr(y, "symbol", None), getattr(y, "units", None))
    await wait_cooldown(cooldown)


if __name__ == "__main__":
    asyncio.run(main_extract())
