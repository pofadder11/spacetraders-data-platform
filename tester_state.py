# =================================================================================================
# tester_state_nav.py
# -------------------------------------------------------------------------------------------------
# Example runner that:
# - Initializes all in-memory state (fleet activity, waypoints, traits, HQ)
# - Uses only state + helpers (no direct DTOs) to prep, navigate to HQ, wait 15s, and return.
# =================================================================================================
from __future__ import annotations

import asyncio
from typing import Optional

from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.agents_api import AgentsApi
from openapi_client.api.systems_api import SystemsApi

from runtime_support import setup_client_from_env
from core_helpers import (
    init_world_state,
    ensure_ready_to_navigate,
    navigate_and_wait,
)

async def async_main() -> None:
    target_symbol = "TROOTS-1"

    with setup_client_from_env() as client:
        fleet_api = FleetApi(client)
        agents_api = AgentsApi(client)
        systems_api = SystemsApi(client)

        # Build all in-memory objects once (fleet_activity_obj, waypoints_ref_obj, waypoint_traits_obj, HQ)
        state = await init_world_state(fleet_api, agents_api, systems_api)
        print(f"[BOOT] fleet={len(state.fleet.by_symbol)} ships, waypoints={len(state.waypoints.by_symbol)} (system), traits={sum(len(v) for v in state.traits.by_wp.values())}")

        # Pick ship (fallback to any if target not present)
        if target_symbol not in state.fleet.by_symbol:
            if state.fleet.by_symbol:
                target_symbol = next(iter(state.fleet.by_symbol.keys()))
            else:
                raise SystemExit("[FATAL] No ships in fleet state.")

        # Snapshot start
        start_wp = getattr(state.fleet.get(target_symbol), "current_waypoint", None)
        print(f"[START] {target_symbol} at {start_wp} → HQ {state.agent_hq}")

        # Prep & go to HQ
        await ensure_ready_to_navigate(fleet_api, state, target_symbol, state.agent_hq)
        await navigate_and_wait(fleet_api, state, target_symbol, state.agent_hq)

        # Pause 15s
        print("[PAUSE] Sleeping 15 seconds at HQ …")
        await asyncio.sleep(15)

        # Return to starting waypoint if different
        if start_wp and start_wp != state.agent_hq:
            print(f"[RETURN] Back to {start_wp}")
            await ensure_ready_to_navigate(fleet_api, state, target_symbol, start_wp)
            await navigate_and_wait(fleet_api, state, target_symbol, start_wp)
        else:
            print("[RETURN] No distinct original waypoint (or same as HQ).")

        # Final log
        final = state.fleet.get(target_symbol)
        print(f"[DONE] {target_symbol}: status={final.status}, wp={final.current_waypoint}, fuel_level={final.fuel_level}")

if __name__ == "__main__":
    asyncio.run(async_main())
