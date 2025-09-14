# services/trade_runner.py
from __future__ import annotations
import asyncio
from typing import Optional

from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.systems_api import SystemsApi

from runtime_support import api_navigate_ship, api_get_ship_nav
from services.market_ops import buy_and_scan, sell_and_scan
from services.arbitrage_repo import top_arbitrage

async def compute_affordable_units(fleet_api: FleetApi, ship_symbol: str, buy_price: int) -> int:
    """
    Replace with your real cargo/credits query. Keep it simple for now.
    """
    # Example placeholders:
    # credits = (await api_get_my_agent(...)).credits
    # capacity_free = ship.cargo.capacity - ship.cargo.units
    # return max(0, min(capacity_free, credits // buy_price))
    return 10  # TEMP: choose a small safe value while testing

async def run_one_highest_delta_trade(
    fleet_api: FleetApi,
    systems_api: SystemsApi,
    ship_symbol: str,
    *,
    min_delta: int = 1,
) -> Optional[str]:
    """
    Executes a single buy→fly→sell based on the top row in `trade_arbitrage`.
    Returns a short summary string or None if nothing to do.
    """
    df = top_arbitrage(limit=1)
    if df.empty:
        return None

    row = df.iloc[0]
    if row["delta"] < min_delta:
        return None

    trade_symbol = row["trade_symbol"]
    buy_wp, buy_price = row["buy_waypoint"], int(row["buy_price"])
    sell_wp, sell_price = row["sell_waypoint"], int(row["sell_price"])

    # 1) Go to buy market
    await api_navigate_ship(fleet_api, ship_symbol, buy_wp)

    # 2) Decide units (credits & cargo constraints)
    units = await compute_affordable_units(fleet_api, ship_symbol, buy_price)
    if units <= 0:
        return f"[{ship_symbol}] Skipped: no capacity or credits for {trade_symbol} at {buy_wp}."

    # 3) BUY (auto-scan & refresh inside)
    await buy_and_scan(
        fleet_api=fleet_api,
        systems_api=systems_api,
        ship_symbol=ship_symbol,
        waypoint=buy_wp,
        trade_symbol=trade_symbol,
        units=units,
    )

    # 4) Fly to sell market
    await api_navigate_ship(fleet_api, ship_symbol, sell_wp)

    # 5) SELL (auto-scan & refresh inside)
    await sell_and_scan(
        fleet_api=fleet_api,
        systems_api=systems_api,
        ship_symbol=ship_symbol,
        waypoint=sell_wp,
        trade_symbol=trade_symbol,
        units=units,
    )

    return (f"[{ship_symbol}] Traded {units}× {trade_symbol}: "
            f"buy {buy_price} @ {buy_wp} → sell {sell_price} @ {sell_wp} (Δ={sell_price - buy_price})")
