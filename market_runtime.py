# =================================================================================================
# market_runtime.py
# -------------------------------------------------------------------------------------------------
# Helpers to fetch SpaceTraders market data and adapt it into domain rows using adapters/market_adapter.py
# Works alongside runtime_support.py (reuses call_sdk/unwrap_data if you import them).
# =================================================================================================
from __future__ import annotations

import sys
import os
import asyncio
import sqlite3
import math
from typing import Any, Dict, Iterable, List, Tuple, Callable, Optional
from sdk_runtime_helper import call_sdk, unwrap_data


from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.agents_api import AgentsApi  
from openapi_client.api.systems_api import SystemsApi

from openapi_client import Configuration, ApiClient

from db.auto_repo_sqlite import snapshot_many, TableSpec, upsert_many

from domain.market_rows import (
    MarketExportRow, MarketImportRow, MarketExchangeRow,
    MarketTransactionRow, MarketGoodRow
)
from adapters.market_adapter import (
    adapt_market_all,
)



def _load_env_token() -> Optional[str]:
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass
    return os.getenv("BEARER_TOKEN")

def setup_client_from_env() -> ApiClient:
    token = _load_env_token()
    if not token:
        print("[FATAL] Missing BEARER_TOKEN in environment or .env")
        sys.exit(1)
    cfg = Configuration()
    cfg.host = "https://api.spacetraders.io/v2"
    cfg.api_key = {"Authorization": token}
    cfg.api_key_prefix = {"Authorization": "Bearer"}
    cfg.access_token = token
    return ApiClient(cfg)

with setup_client_from_env() as client:
    fleet_api = FleetApi(client)
    agents_api = AgentsApi(client)
    systems_api = SystemsApi(client)

# -----------------------------------------------------------------------------------------------
# Small utils
# -----------------------------------------------------------------------------------------------
def system_symbol_from_waypoint(waypoint_symbol: str) -> str:
    """
    Convert e.g. 'X1-Q51-A1' -> 'X1-Q51'. Robust to extra parts like 'X1-Q51-AB5A'.
    """
    parts = (waypoint_symbol or "").split("-")
    if len(parts) < 2:
        raise ValueError(f"Invalid waypoint symbol: {waypoint_symbol}")
    return "-".join(parts[:2])

def distance_from_origin(x: Optional[int], y: Optional[int]) -> float:
    return math.hypot(x or 0, y or 0)

# -----------------------------------------------------------------------------------------------
# Safe API wrapper for GET /systems/{systemSymbol}/waypoints/{waypointSymbol}/market
# (SDKs sometimes put this on SystemsApi as `get_market` or similar.)
# -----------------------------------------------------------------------------------------------
async def api_get_market(systems_api: SystemsApi, waypoint_symbol: str) -> Any:
    """
    Returns the raw market DTO (OpenAPI model or dict-like), unwrapped from .data if present.
    Handles possible SDK method name differences via getattr.
    """
    system_symbol = system_symbol_from_waypoint(waypoint_symbol)

    # Common generated name is "get_market"
    if hasattr(systems_api, "get_market"):
        resp = await call_sdk(
            systems_api, "get_market",
            system_symbol=system_symbol,
            waypoint_symbol=waypoint_symbol
        )
        return unwrap_data(resp)

    # Some clients might expose it as "get_system_waypoint_market" (less common)
    if hasattr(systems_api, "get_system_waypoint_market"):
        resp = await call_sdk(
            systems_api, "get_system_waypoint_market",
            system_symbol=system_symbol,
            waypoint_symbol=waypoint_symbol
        )
        return unwrap_data(resp)

    # Last-resort: try generic call name people sometimes add
    if hasattr(systems_api, "get_waypoint_market"):
        resp = await call_sdk(
            systems_api, "get_waypoint_market",
            system_symbol=system_symbol,
            waypoint_symbol=waypoint_symbol
        )
        return unwrap_data(resp)

    raise AttributeError("Your SystemsApi client does not have a market getter (get_market / get_system_waypoint_market / get_waypoint_market).")

# -----------------------------------------------------------------------------------------------
# Adaptation helpers
# -----------------------------------------------------------------------------------------------
def adapt_market_rows(market_dto: Any, waypoint_symbol: str) -> Tuple[
    List[MarketExportRow], List[MarketImportRow], List[MarketExchangeRow],
    List[MarketTransactionRow], List[MarketGoodRow]
]:
    """
    Use your adapters/market_adapter.py to convert the raw market DTO into domain rows.
    """
    return adapt_market_all(market_dto, waypoint_symbol)

async def capture_market_for_waypoint(
    systems_api: SystemsApi,
    waypoint_symbol: str,
) -> Dict[str, List[Any]]:
    """
    Fetch and adapt all market data for a single waypoint.
    Returns a dict with keys: exports, imports, exchange, transactions, goods.
    """
    dto = await api_get_market(systems_api, waypoint_symbol)
    exports, imports, exchange, transactions, goods = adapt_market_rows(dto, waypoint_symbol)
    return {
        "exports": exports,
        "imports": imports,
        "exchange": exchange,
        "transactions": transactions,
        "goods": goods,
    }

# -----------------------------------------------------------------------------------------------
# Batch capture helpers
# -----------------------------------------------------------------------------------------------
async def capture_markets_for_waypoints(
    systems_api: SystemsApi,
    waypoint_symbols: Iterable[str],
    *,
    on_batch: Optional[Callable[[str, Dict[str, List[Any]]], None]] = None,
    delay_seconds: float = 0.0,
) -> Dict[str, Dict[str, List[Any]]]:
    """
    Capture markets for many waypoints. If `on_batch` is provided, it is called per-waypoint with
    (waypoint_symbol, rows_dict). Otherwise results are collected and returned.

    `delay_seconds` can be used to be gentle with API rate limits.
    """
    out: Dict[str, Dict[str, List[Any]]] = {}

    for wp in waypoint_symbols:
        try:
            rows = await capture_market_for_waypoint(systems_api, wp)
            if on_batch:
                on_batch(wp, rows)  # e.g., persist rows to DB here
            else:
                out[wp] = rows
        except Exception as e:
            # Keep going on individual failures
            print(f"[WARN] Failed to capture market for {wp}: {e}")
        if delay_seconds > 0:
            await asyncio.sleep(delay_seconds)

    return out

# -----------------------------------------------------------------------------------------------
# Convenience: compute nearest MARKETPLACE waypoints from traits (in-memory), then capture markets
# -----------------------------------------------------------------------------------------------
def nearest_marketplace_symbols(
    traits_by_wp: Dict[str, List[Any]],  # values should have .trait_symbol, .x, .y
    n: int = 5,
) -> List[str]:
    """
    Returns up to N waypoint symbols that have a MARKETPLACE trait, nearest to (0,0).
    """
    rows: List[Tuple[str, float]] = []
    for wp_symbol, rows_list in traits_by_wp.items():
        # any MARKETPLACE on this waypoint?
        has_market = False
        x_val: Optional[int] = None
        y_val: Optional[int] = None
        for row in rows_list:
            if getattr(row, "trait_symbol", None) == "MARKETPLACE":
                has_market = True
                # prefer the MARKETPLACE row's coords; if missing, use the first row’s coords
                x_val = getattr(row, "x", None) if getattr(row, "x", None) is not None else x_val
                y_val = getattr(row, "y", None) if getattr(row, "y", None) is not None else y_val
                # break NOT strictly necessary; keep scanning to find coords if first MARKETPLACE had None
        if has_market:
            # fallbacks: take coords from any row on the same waypoint if MARKETPLACE row lacked them
            if x_val is None or y_val is None:
                for r in rows_list:
                    if x_val is None:
                        x_val = getattr(r, "x", None)
                    if y_val is None:
                        y_val = getattr(r, "y", None)
                    if x_val is not None and y_val is not None:
                        break
            dist = distance_from_origin(x_val, y_val)
            rows.append((wp_symbol, dist))

    rows.sort(key=lambda t: t[1])
    return [wp for wp, _ in rows[:n]]

async def capture_markets_for_nearest_marketplaces(
    systems_api: SystemsApi,
    traits_by_wp: Dict[str, List[Any]],
    *,
    n: int = 5,
    on_batch: Optional[Callable[[str, Dict[str, List[Any]]], None]] = None,
    delay_seconds: float = 0.0,
) -> Dict[str, Dict[str, List[Any]]]:
    """
    Compute the N nearest MARKETPLACE waypoints (by Euclidean distance from origin) from the
    in-memory traits dict (state.traits.by_wp), then fetch + adapt market rows for each.

    If `on_batch` is provided, it's called per waypoint so you can persist immediately.
    Otherwise returns a dict mapping waypoint_symbol -> rows dict.
    """
    targets = nearest_marketplace_symbols(traits_by_wp, n=n)
    print(f"[INFO] Capturing markets for nearest {len(targets)} marketplace(s): {targets}")
    return await capture_markets_for_waypoints(
        systems_api,
        targets,
        on_batch=on_batch,
        delay_seconds=delay_seconds,
    )

async def market_to_db(waypoint: str) -> None:
    # Fetch first (network I/O), then write to DB (short-lived connection)
    rows = await capture_market_for_waypoint(systems_api, waypoint)
    with sqlite3.connect("spacetraders.db") as conn:
        snapshot_many(conn, "market_goods", MarketGoodRow, rows["goods"])  # append-only history
        if rows["transactions"]:
            upsert_many(conn, TableSpec(table="market_transactions", pk="id"), rows["transactions"])
