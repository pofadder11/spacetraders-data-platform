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

# --- main ---------------------------------------------------------------------
async def async_main() -> None:
    # Single sqlite connection (auto-repo will create/alter tables as needed)
    conn = sqlite3.connect("spacetraders.db")

    try:
        with setup_client_from_env() as client:
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
            print("DEBUG first activity model_dump:", activities[0].model_dump())
            specs = [adapt_ships_specs_from_ship(d) for d in ships]

            print("\n=== ShipsActivity (telemetry) ===")
            for a in activities[:5]:
                print_activity(a)

            print("\n=== ShipsSpecs (reference) ===")
            for s in specs[:5]:
                print_specs(s)

            print("\n[3/5] Writing to SQLite (spacetraders.db) via auto-repo...")
            for a in activities[:3]:
                print("DEBUG upsert row:", a.symbol, a.status, a.flight_mode, a.cooldown_remaining_seconds)
            upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), activities)
            upsert_many(conn, TableSpec(table="ships_specs", pk="symbol"), specs)
            print("    ✓ Upserts complete.")

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
                        # write the updated activity row back to SQLite
                        upsert_many(conn, TableSpec(table="ships_activity", pk="symbol"), [updated])
                        print("    ✓ Updated activity written to SQLite.")
                except Exception as e:
                    print(f"[WARN] get_ship_nav failed for {symbol}: {e}")

            print("\n[5/5] Done. Tables: ships_specs, ships_activity (ordered by updated_at in inspector).")
    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(async_main())
