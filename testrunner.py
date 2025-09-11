#!/usr/bin/env python3
# async_testrunner_sqlite.py (slim)
from __future__ import annotations

import asyncio
import sqlite3
from typing import Any, Iterable

# Bring in all plumbing from runtime_support
from runtime_support import (
    setup_client_from_env,
    maybe_await,
    unwrap_data,
    print_activity,
    print_specs,
    load_waypoints_from_agent,
)

# Generated API
from openapi_client.api.fleet_api import FleetApi

# Domain adapters
from adapters.ships_activity_adapter import adapt_ships_activity_from_ship, merge_activity_with_nav
from adapters.ships_specs_adapter import adapt_ships_specs_from_ship

# DB
from db.auto_repo_sqlite import TableSpec, upsert_many


async def async_main() -> None:
    conn = sqlite3.connect("spacetraders.db")

    try:
        with setup_client_from_env() as client:
            # 1) Optional seed: waypoints + traits from agent HQ
            try:
                await load_waypoints_from_agent(conn, client)
            except Exception as e:
                import traceback
                print("[WAYPOINTS][FATAL] Unexpected error:", repr(e))
                traceback.print_exc()

            # 2) Fleet snapshot → domain → DB
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
