# tests/market_current_test.py
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone, timedelta

from sqlalchemy import select

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from session import init_db, SessionLocal
from models import MarketTradeGoodCurrent
from services.normalizer import upsert_market_trade_goods_current
from openapi_client.models.market import Market


def run_test_from_sample(path: str = "json_output_samples/market_prices.json") -> None:
    init_db()
    sample = json.load(open(path, "r", encoding="utf-8"))
    market = Market.from_dict(sample["data"])  # build generated model

    t0 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t1 = t0 + timedelta(hours=1)

    print("[DEBUG] waypoint:", market.symbol)
    print("[DEBUG] trade_goods count:", 0 if market.trade_goods is None else len(market.trade_goods))
    with SessionLocal() as session:
        # First upsert with newer time t1
        n1 = upsert_market_trade_goods_current(session, market, observed_at=t1)
        # Second upsert with older time t0 - should not overwrite
        n2 = upsert_market_trade_goods_current(session, market, observed_at=t0)

        print(f"[TEST] current upserts newer then older: {n1}, {n2}")

        waypoint_symbol = market.symbol
        rows = session.execute(
            select(MarketTradeGoodCurrent).where(MarketTradeGoodCurrent.waypoint_symbol == waypoint_symbol)
        ).scalars().all()
        print(f"[DEBUG] current rows count: {len(rows)}")
        if rows:
            print("[DEBUG] first observed_at:", rows[0].observed_at)
        def _eq(a, b):
            if a is None or b is None:
                return False
            if a.tzinfo is None:
                a = a.replace(tzinfo=timezone.utc)
            if b.tzinfo is None:
                b = b.replace(tzinfo=timezone.utc)
            return a == b

        bad = [r for r in rows if not _eq(r.observed_at, t1)]
        for r in bad[:5]:
            print("[DEBUG] mismatch:", r.trade_symbol, r.observed_at)
        assert not bad, "Older snapshot should not downgrade current"
        print("[TEST] current rows verified for freshest observed_at")


if __name__ == "__main__":
    run_test_from_sample()
