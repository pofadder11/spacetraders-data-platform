# tests/market_trade_goods_test.py
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

from sqlalchemy import select

# Ensure project root on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from session import init_db, SessionLocal
from models import MarketTradeGoodSnapshot
from services.normalizer import upsert_market_trade_goods
from openapi_client.models.market import Market


def run_test_from_sample(path: str = "json_output_samples/market_prices.json") -> None:
    init_db()
    sample = json.load(open(path, "r", encoding="utf-8"))
    market = Market.from_dict(sample["data"])  # build generated model

    with SessionLocal() as session:
        n = upsert_market_trade_goods(session, market, observed_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
        print(f"[TEST] upserted rows: {n}")

        # Verify rows exist for the waypoint in the sample
        waypoint_symbol = market.symbol
        rows = session.execute(
            select(MarketTradeGoodSnapshot).where(MarketTradeGoodSnapshot.waypoint_symbol == waypoint_symbol)
        ).scalars().all()
        print(f"[TEST] rows in DB for {waypoint_symbol}: {len(rows)}")
        # Show a couple of entries
        for row in rows[:3]:
            print("[TEST] sample row:", row.trade_symbol, row.type, row.purchase_price, row.sell_price)


if __name__ == "__main__":
    run_test_from_sample()
