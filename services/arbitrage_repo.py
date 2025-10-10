# services/arbitrage_repo.py
import sqlite3
import pandas as pd
from typing import Optional, Tuple, List

DB_PATH = "spacetraders.db"

def top_arbitrage(limit: int = 20) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        q = """
        SELECT
          trade_symbol,
          buy_waypoint,  buy_price,
          sell_waypoint, sell_price,
          delta,
          buy_observed_at, sell_observed_at, computed_at
        FROM trade_arbitrage
        WHERE delta > 0
        ORDER BY delta DESC, computed_at DESC
        LIMIT ?
        """
        return pd.read_sql_query(q, conn, params=(limit,))

def best_for_symbol(trade_symbol: str) -> Optional[Tuple[str, int, str, int, int]]:
    """
    Returns (buy_waypoint, buy_price, sell_waypoint, sell_price, delta) for one symbol,
    or None if not found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        q = """
        SELECT buy_waypoint, buy_price, sell_waypoint, sell_price, delta
        FROM trade_arbitrage
        WHERE trade_symbol = ?
        """
        row = conn.execute(q, (trade_symbol,)).fetchone()
        return tuple(row) if row else None
    
def best_arb_at_waypoint(waypoint: str):
    with sqlite3.connect(DB_PATH) as conn:
        q = """
        SELECT
          trade_symbol,
          buy_waypoint,
          buy_price,
          sell_waypoint,
          sell_price,
          delta,
          computed_at
        FROM trade_arbitrage
        WHERE buy_waypoint = ?
        ORDER BY delta DESC, computed_at DESC
        LIMIT 1
        """
        row = conn.execute(q, (waypoint,)).fetchone()
    return row  # tuple, or None if no match

