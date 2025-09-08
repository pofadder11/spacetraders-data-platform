#!/usr/bin/env python3
# async_testrunner_sqlite.py
from __future__ import annotations

import asyncio
import inspect
import os
import sys
import sqlite3
from typing import Any, Iterable

# --- env loader ---------------------------------------------------------------
def _load_env_token() -> str | None:
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        if os.path.exists(".env"):
            try:
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        if k.strip() == "BEARER_TOKEN":
                            os.environ.setdefault("BEARER_TOKEN", v.strip())
            except Exception:
                pass
    return os.getenv("BEARER_TOKEN")

# --- domain & adapters --------------------------------------------------------
from domain.ships_activity import ShipsActivity
from domain.ships_specs import ShipsSpecs
from adapters.ships_activity_adapter import (
    adapt_ships_activity_from_ship,
    merge_activity_with_nav,
)
from adapters.ships_specs_adapter import adapt_ships_specs_from_ship

# --- generated client ---------------------------------------------------------
from openapi_client import Configuration, ApiClient
from openapi_client.api.fleet_api import FleetApi

# --- db auto-repo (DRY) -------------------------------------------------------
# Make sure you have db/auto_repo_sqlite.py as provided earlier
from db.auto_repo_sqlite import TableSpec, upsert_many

# --- helpers ------------------------------------------------------------------
def unwrap_data(resp: Any) -> Any:
    return getattr(resp, "data", resp)

def setup_client_from_env() -> ApiClient:
    token = _load_env_token()
    if not token:
        print("[FATAL] Missing token. Put BEARER_TOKEN in .env.")
        sys.exit(1)

    cfg = Configuration()
    try:
        cfg.host = "https://api.spacetraders.io/v2"
    except Exception:
        pass

    try:
        cfg.api_key = getattr(cfg, "api_key", {}) or {}
        cfg.api_key["Authorization"] = token
        cfg.api_key_prefix = getattr(cfg, "api_key_prefix", {}) or {}
        cfg.api_key_prefix["Authorization"] = "Bearer"
    except Exception:
        pass

    try:
        cfg.access_token = token
    except Exception:
        pass

    return ApiClient(cfg)

async def maybe_await(api_obj: Any, method_name: str, *args, **kwargs) -> Any:
    fn = getattr(api_obj, method_name)
    if inspect.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    result = fn(*args, **kwargs)
    if inspect.isawaitable(result):
        return await result
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))

def print_activity(a: ShipsActivity) -> None:
    print(f"- {a.symbol}: status={a.status}, wp={a.current_waypoint}, dest={a.destination_waypoint}")
    print(f"  fuel {a.fuel_current}/{a.fuel_capacity} -> fuel_level={a.fuel_level}")
    print(f"  cargo {a.cargo_units}/{a.cargo_capacity}, cooldown={a.cooldown_remaining_seconds}s")

def print_specs(s: ShipsSpecs) -> None:
    print(f"- {s.symbol}: role={s.role}, frame={s.frame_name}, engine={s.engine_name}, speed={s.speed}")
    print(f"  mounts={s.mounts} modules={s.modules} capacity={s.capacity}")

# --- pull + persist system waypoints based on agent HQ (robust) --------------
import sqlite3
from db.auto_repo_sqlite import TableSpec, upsert_many
from openapi_client.api.systems_api import SystemsApi
from openapi_client.api.agents_api import AgentsApi
from adapters.waypoint_adapter import adapt_waypoints

async def load_waypoints_from_agent(conn: sqlite3.Connection, client) -> None:
    """
    Fetch agent HQ, derive system symbol, then fetch all system waypoints (with pagination)
    and upsert them into the 'waypoints' table.
    """
    agents_api = AgentsApi(client)
    systems_api = SystemsApi(client)

    # 1) get_my_agent (sync or async)
    try:
        agent_resp = await maybe_await(agents_api, "get_my_agent")
        agent = unwrap_data(agent_resp)
        print("[WAYPOINTS] get_my_agent OK")
    except Exception as e:
        print(f"[WAYPOINTS][ERROR] get_my_agent failed: {e!r}")
        return

    # 2) derive system from agent.headquarters (e.g., X1-Q51-A1 -> X1-Q51)
    hq_wp = getattr(agent, "headquarters", None)
    if not hq_wp or not isinstance(hq_wp, str) or "-" not in hq_wp:
        print(f"[WAYPOINTS][WARN] Unexpected headquarters value: {hq_wp!r}")
        return
    parts = hq_wp.split("-")
    if len(parts) < 2:
        print(f"[WAYPOINTS][WARN] Cannot derive system from HQ: {hq_wp!r}")
        return
    system_symbol = "-".join(parts[:2])
    print(f"[WAYPOINTS] Agent HQ={hq_wp}, derived system={system_symbol}")

        # 3) fetch all pages of system waypoints (page+limit only; no per_page)
    all_dtos = []
    page = 1
    limit = 20  # adjust if you want more per page
    while True:
        try:
            # Most OpenAPI Python clients use (system_symbol, page=?, limit=?)
            wps_resp = await maybe_await(
                systems_api,
                "get_system_waypoints",
                system_symbol=system_symbol,
                page=page,
                limit=limit,
            )
            wps_data = unwrap_data(wps_resp)
        except TypeError:
            # Some clients don't expose page/limit at all -> single page
            wps_resp = await maybe_await(
                systems_api,
                "get_system_waypoints",
                system_symbol=system_symbol,
            )
            wps_data = unwrap_data(wps_resp)

        # Normalize to a list:
        # - some SDKs return a plain list
        # - others return a wrapper with .data / .waypoints
        if wps_data is None:
            break
        if isinstance(wps_data, (list, tuple)):
            batch = list(wps_data)
        else:
            batch = []
            # common wrappers
            maybe = getattr(wps_data, "data", None)
            if maybe is not None:
                batch = list(maybe) if isinstance(maybe, (list, tuple)) else list(getattr(maybe, "waypoints", []) or [])
            else:
                batch = list(getattr(wps_data, "waypoints", []) or [])

        print(f"[WAYPOINTS] page={page} got {len(batch)}")
        all_dtos.extend(batch)

        # If pagination not supported or last page is short, stop
        if not batch or len(batch) < limit:
            break
        page += 1


    if not all_dtos:
        print("[WAYPOINTS][WARN] No waypoints returned for system", system_symbol)
        return

    # 4) adapt and upsert
    from adapters.waypoint_trait_adapter import adapt_traits_from_waypoint_dtos
    try:
        waypoints = adapt_waypoints(all_dtos)
        # flatten and write traits directly from DTOs
        trait_rows = adapt_traits_from_waypoint_dtos(all_dtos)
        upsert_many(conn, TableSpec(table="waypoints", pk="symbol", add_updated_at=True), waypoints)
        if trait_rows:
            upsert_many(conn, TableSpec(table="waypoint_traits", pk="id", add_updated_at=True), trait_rows)
        upsert_many(conn, TableSpec(table="waypoints", pk="symbol", add_updated_at=True), waypoints)
        print(f"✓ Upserted {len(waypoints)} waypoints and {len(trait_rows)} waypoint_traits")
    except Exception as e:
        print(f"[WAYPOINTS][ERROR] adapt/upsert failed: {e!r}")

# --- main ---------------------------------------------------------------------
async def async_main() -> None:
    import sqlite3
    conn = sqlite3.connect("spacetraders.db")

    try:
        # client is only valid INSIDE this context manager
        with setup_client_from_env() as client:
            # ------------------------------------------------------------------
            # 1) seed waypoints based on agent HQ (this uses AgentsApi + SystemsApi)
            # ------------------------------------------------------------------
            try:
                await load_waypoints_from_agent(conn, client)
            except Exception as e:
                import traceback
                print("[WAYPOINTS][FATAL] Unexpected error:", repr(e))
                traceback.print_exc()

            # ------------------------------------------------------------------
            # 2) existing fleet flow (get_my_ships, adapt, write, etc.)
            # ------------------------------------------------------------------
            fleet = FleetApi(client)

            print("[1/5] Fetching my ships...")
            resp = await maybe_await(fleet, "get_my_ships")
            ships: Iterable[Any] = unwrap_data(resp)
            ships = list(ships)
            if not ships:
                print("No ships returned. Check BEARER_TOKEN and that your agent has ships.")
                return

            print(f"[2/5] Adapting {len(ships)} ship(s) to domain slices...")
            activities = [adapt_ships_activity_from_ship(d) for d in ships]
            specs = [adapt_ships_specs_from_ship(d) for d in ships]

            print("\n=== ShipsActivity (telemetry) ===")
            for a in activities[:5]:
                print_activity(a)

            print("\n=== ShipsSpecs (reference) ===")
            for s in specs[:5]:
                print_specs(s)

            from db.auto_repo_sqlite import TableSpec, upsert_many
            upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), activities)
            upsert_many(conn, TableSpec(table="ships_specs", pk="symbol"), specs)

            symbol = getattr(ships[0], "symbol", None)
            if symbol:
                print(f"\n[4/5] Fetching nav for {symbol} and merging into activity...")
                try:
                    nav_resp = await maybe_await(fleet, "get_ship_nav", ship_symbol=symbol)
                    nav_dto = unwrap_data(nav_resp)
                    act0 = next((a for a in activities if a.symbol == symbol), None)
                    if act0:
                        updated = merge_activity_with_nav(act0, nav_dto)
                        print("\n=== After nav update ===")
                        print_activity(updated)
                        upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), [updated])
                        print("    ✓ Updated activity written to SQLite.")
                except Exception as e:
                    print(f"[WARN] get_ship_nav failed for {symbol}: {e}")

            print("\n[5/5] Done.")

    finally:
        conn.close()


if __name__ == "__main__":
    asyncio.run(async_main())
