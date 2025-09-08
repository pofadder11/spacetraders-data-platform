from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any

from config.settings import settings
from db.async_session import SessionLocal, init_db_async
from services import writethrough_async as wt
from services import runner_status as rs
from api.server import run_server
from runners.market_loop import run_market_polling
from runners.fleet_loops import (
    select_frigate_and_miners,
    select_probe_frigate_by_frame,
    miners_from_ships,
    find_asteroid_waypoint,
    miners_loop,
    frigate_loop,
    frigate_buy_drones,
)

# Use the generated sync client in a thread for API calls
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
    return await asyncio.to_thread(func, *args, **kwargs)


async def bootstrap() -> tuple[str, list[Any]]:
    cfg = openapi_client.Configuration(access_token=settings.bearer_token)
    cli = openapi_client.ApiClient(cfg)
    agents = openapi_client.AgentsApi(cli)
    systems = openapi_client.SystemsApi(cli)
    fleet = openapi_client.FleetApi(cli)

    me = (await api_call(agents.get_my_agent)).data
    hq = getattr(me, "headquarters", None)
    system_symbol = "-".join(hq.split("-")[:2]) if hq else None
    if not system_symbol:
        raise RuntimeError("Cannot determine system from headquarters")

    sys_data = (await api_call(systems.get_system, system_symbol)).data
    wps = (await api_call(systems.get_system_waypoints, system_symbol)).data
    ships = (await api_call(fleet.get_my_ships)).data

    async with session_scope() as s:
        await wt.upsert_system(s, sys_data)
        await wt.upsert_waypoints(s, wps)
        await wt.upsert_ships_current(s, ships)
        await wt.upsert_fleet_nav(s, ships)

    return system_symbol, ships


async def main() -> None:
    await init_db_async()
    system_symbol, ships = await bootstrap()
    print(f"Bootstrapped system {system_symbol} with {len(ships)} ships.")

    # Choose probe/frigate by frame when possible
    probe, frigate_by_frame = select_probe_frigate_by_frame(ships)
    # Fallbacks
    ship_symbol = probe or (getattr(ships[0], "symbol", None) if ships else None)
    if not ship_symbol:
        print("No ships found; exiting.")
        return

    cfg = openapi_client.Configuration(access_token=settings.bearer_token)
    client = openapi_client.ApiClient(cfg)

    # Find asteroid waypoint
    asteroid = await find_asteroid_waypoint(client, system_symbol)
    if not asteroid:
        print("No suitable asteroid waypoint found; exiting.")
        return

    # Role selection: prefer frame-identified frigate, else heuristic
    if frigate_by_frame:
        frigate = frigate_by_frame
    else:
        fr, _mn = select_frigate_and_miners(ships)
        frigate = fr
    if not frigate:
        print("Could not identify frigate; exiting.")
        return

    # Launch market polling immediately on probe
    print(f"Starting market polling with probe {ship_symbol}...")
    async def probe_factory():
        await rs.set_loop_state("market", "starting", ship=ship_symbol)
        await run_market_polling(client, ship_symbol)
    probe_task = asyncio.create_task(supervise("market", probe_factory))

    # Ensure we have at least 3 mining drones before loops
    print("Scanning shipyards to purchase mining drones (target: 3)...")
    bought = await frigate_buy_drones(client, frigate, system_symbol, desired_count=3)
    print(f"Purchased {bought} mining drones (if available).")

    # Refresh fleet and pick miners, excluding frigate
    fleet = openapi_client.FleetApi(client)
    ships2 = (await asyncio.to_thread(fleet.get_my_ships)).data
    miners = miners_from_ships(ships2, exclude_symbol=frigate)
    if not miners:
        # Fallback: use heuristic selector and drop frigate from miners
        _fr, _mn = select_frigate_and_miners(ships2)
        miners = [m for m in _mn if m != frigate]
    if not miners:
        print("No miners with MINING_LASER found; exiting.")
        return

    print(f"Starting loops: frigate({frigate}), miners({', '.join(miners)}) @ {asteroid}")
    async def frigate_factory():
        await rs.set_loop_state("frigate", "starting", ship=frigate, asteroid=asteroid)
        await frigate_loop(client, frigate, asteroid)
    async def miners_factory():
        await rs.set_loop_state("miners", "starting", ships=miners, asteroid=asteroid)
        await miners_loop(client, miners, asteroid, frigate)

    # Start FastAPI service in the background (don't block loops)
    async def api_factory():
        await rs.set_loop_state("api", "starting")
        await run_server()
    asyncio.create_task(supervise("api", api_factory))

    # Supervise loops so they restart on errors
    await asyncio.gather(
        probe_task,
        supervise("frigate", frigate_factory),
        supervise("miners", miners_factory),
    )


async def supervise(name: str, factory):
    """Restart a loop if it exits with an exception; log status."""
    while True:
        try:
            await rs.set_loop_state(name, "running")
            await factory()
            await rs.set_loop_state(name, "stopped")
            return
        except Exception as e:
            await rs.set_loop_state(name, "error", error=str(e))
            await asyncio.sleep(1.0)


if __name__ == "__main__":
    asyncio.run(main())
