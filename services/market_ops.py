# services/market_ops.py
from __future__ import annotations
import asyncio
import sqlite3
from typing import Dict, Any, Optional

from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.systems_api import SystemsApi

from market_runtime import capture_market_for_waypoint
from db.auto_repo_sqlite import snapshot_many, TableSpec, upsert_many
from domain.market_rows import MarketGoodRow, MarketTransactionRow

# If you put the refresh helper in your repo as suggested earlier:
from analytics_refresh import refresh_market_analytics

DB_PATH = "spacetraders.db"

async def _scan_market(systems_api: SystemsApi, waypoint: str) -> None:
    rows: Dict[str, Any] = await capture_market_for_waypoint(systems_api, waypoint)
    with sqlite3.connect(DB_PATH) as conn:
        # append-only goods snapshot
        snapshot_many(conn, "market_goods", MarketGoodRow, rows["goods"])
        # upsert transactions (if your capture returns them)
        if rows.get("transactions"):
            upsert_many(conn, TableSpec(table="market_transactions", pk="id"), rows["transactions"])

def _refresh_analytics() -> None:
    # Light, runs in-process; safe to call after inserts commit
    refresh_market_analytics(DB_PATH, lookback_hours=72, create_schema=False)

async def buy_and_scan(
    fleet_api: FleetApi,
    systems_api: SystemsApi,
    ship_symbol: str,
    waypoint: str,
    trade_symbol: str,
    units: int,
) -> Dict[str, Any]:
    """
    Purchase at `waypoint`, then scan that market and refresh analytics tables.
    Returns the purchase response payload.
    """
    # 1) Execute purchase via OpenAPI client
    resp = await fleet_api.purchase_cargo(ship_symbol, {"symbol": trade_symbol, "units": units})
    # 2) Persist a scan *immediately* after buy
    await _scan_market(systems_api, waypoint)
    # 3) Refresh materialized tables so the planner & dashboard see the change
    await asyncio.to_thread(_refresh_analytics)
    return resp

async def sell_and_scan(
    fleet_api: FleetApi,
    systems_api: SystemsApi,
    ship_symbol: str,
    waypoint: str,
    trade_symbol: str,
    units: int,
) -> Dict[str, Any]:
    resp = await fleet_api.sell_cargo(ship_symbol, {"symbol": trade_symbol, "units": units})
    await _scan_market(systems_api, waypoint)
    await asyncio.to_thread(_refresh_analytics)
    return resp
