from __future__ import annotations

# %% [markdown]
# Test: Frigate scan_waypoints payload and cooldown handling

# %%
import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
import openapi_client

load_dotenv()


async def to_thread(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


async def pick_frigate(fleet: openapi_client.api.fleet_api.FleetApi) -> Optional[str]:
    ships = (await to_thread(fleet.get_my_ships)).data
    # Prefer frame containing FRIGATE; else role COMMAND/HAULER/REFINERY; else first
    for s in ships:
        frame = getattr(getattr(s, "frame", None), "symbol", "") or ""
        if "FRIGATE" in frame.upper():
            return getattr(s, "symbol", None)
    for s in ships:
        role = getattr(getattr(s, "registration", None), "role", None)
        if str(role).upper() in ("COMMAND", "HAULER", "REFINERY"):
            return getattr(s, "symbol", None)
    return getattr(ships[0], "symbol", None) if ships else None


async def wait_cooldown(cooldown) -> None:
    if cooldown is None:
        return
    rem = getattr(cooldown, "remaining_seconds", None)
    if rem is not None and rem > 0:
        print(f"[cooldown] waiting {rem}s")
        await asyncio.sleep(float(rem) + 0.5)


async def main_scan_frigate() -> None:
    token = os.getenv("BEARER_TOKEN")
    if not token:
        raise RuntimeError("Missing BEARER_TOKEN")
    cfg = openapi_client.Configuration(access_token=token)
    client = openapi_client.ApiClient(cfg)
    fleet = openapi_client.FleetApi(client)

    frig = await pick_frigate(fleet)
    if not frig:
        print("[err] No frigate-like ship found.")
        return
    print(f"[info] Using frigate {frig}")
    resp = fleet.create_ship_waypoint_scan(frig)
    print("[DEBUG]: printing resp called directly from resp = fleet.create_ship_waypoint_scan(frig) without await: ",resp)

    # Check mounts for SENSOR_ARRAY
    ship = (await to_thread(fleet.get_my_ship, frig)).data
    mounts = getattr(ship, "mounts", []) or []
    has_sensor = any("SENSOR_ARRAY" in str(getattr(m, "symbol", "")).upper() for m in mounts)
    print(f"[info] Has SENSOR_ARRAY: {has_sensor}")
    """
    try:
        resp = await to_thread(fleet.create_ship_waypoint_scan(frig))
    except openapi_client.exceptions.ApiException as e:
        print("[err] scan API error:", getattr(e, "body", str(e)))
        return
    """

    wps = getattr(resp, "waypoints", None) or []
    cooldown = getattr(resp, "cooldown", None)
    print(f"[ok] Received {len(wps)} waypoints; cooldown: {getattr(cooldown, 'remaining_seconds', None)}s")
    for w in wps[:5]:
        print("   -", getattr(w, "symbol", None), getattr(w, "type", None))
    await wait_cooldown(cooldown)


if __name__ == "__main__":
    asyncio.run(main_scan_frigate())

