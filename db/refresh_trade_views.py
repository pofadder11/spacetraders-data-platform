#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SpaceTraders Market Analytics — SQLite wiring (env-driven)
---------------------------------------------------------
This module:
  * Ensures views/tables exist (from db_schema_sqlite.sql)   [optional]
  * Refreshes materialized "trade_arbitrage"
  * Appends to "trade_arbitrage_history" (hour buckets)
  * Rolls up "market_goods_snapshots" into hourly OHLC in "market_goods_ohlc_hourly"

Usage (CLI):
  python -m db.refresh_trade_views --lookback-hours 72
  # or explicitly:
  python -m db.refresh_trade_views /path/to/spacetraders.db --lookback-hours 72 --no-create-schema

Usage (from runners):
  from db.refresh_trade_views import refresh_trade_views
  refresh_trade_views(lookback_hours=72, create_schema=True)  # DB path read from .env by default
"""

from __future__ import annotations
import argparse
import os
import sqlite3
from pathlib import Path
from typing import Optional

# Optional: load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

SCHEMA_FILE = Path(__file__).with_name("db_schema_sqlite.sql")

REFRESH_ARBITRAGE_SQL = """
DELETE FROM trade_arbitrage;

INSERT INTO trade_arbitrage (
  trade_symbol, buy_waypoint, buy_price, sell_waypoint, sell_price,
  delta, buy_observed_at, sell_observed_at, computed_at
)
WITH latest AS (
  SELECT * FROM market_goods_latest
),
min_buy AS (
  SELECT trade_symbol, MIN(purchase_price) AS best_buy_price
  FROM latest
  WHERE purchase_price IS NOT NULL
  GROUP BY trade_symbol
),
buy_candidates AS (
  SELECT
    l.trade_symbol,
    l.waypoint_symbol   AS buy_waypoint,
    l.purchase_price    AS buy_price,
    l.observed_at       AS buy_observed_at
  FROM latest l
  JOIN min_buy mb
    ON mb.trade_symbol    = l.trade_symbol
   AND mb.best_buy_price  = l.purchase_price
),
buy_pick AS (
  SELECT *
  FROM (
    SELECT
      *,
      ROW_NUMBER() OVER (
        PARTITION BY trade_symbol
        ORDER BY buy_observed_at DESC, buy_waypoint ASC
      ) AS rn
    FROM buy_candidates
  )
  WHERE rn = 1
),
max_sell AS (
  SELECT trade_symbol, MAX(sell_price) AS best_sell_price
  FROM latest
  WHERE sell_price IS NOT NULL
  GROUP BY trade_symbol
),
sell_candidates AS (
  SELECT
    l.trade_symbol,
    l.waypoint_symbol   AS sell_waypoint,
    l.sell_price        AS sell_price,
    l.observed_at       AS sell_observed_at
  FROM latest l
  JOIN max_sell ms
    ON ms.trade_symbol     = l.trade_symbol
   AND ms.best_sell_price  = l.sell_price
),
sell_pick AS (
  SELECT *
  FROM (
    SELECT
      *,
      ROW_NUMBER() OVER (
        PARTITION BY trade_symbol
        ORDER BY sell_observed_at DESC, sell_waypoint ASC
      ) AS rn
    FROM sell_candidates
  )
  WHERE rn = 1
)
SELECT
  b.trade_symbol,
  b.buy_waypoint,
  b.buy_price,
  s.sell_waypoint,
  s.sell_price,
  (s.sell_price - b.buy_price) AS delta,
  b.buy_observed_at,
  s.sell_observed_at,
  CURRENT_TIMESTAMP AS computed_at
FROM buy_pick b
JOIN sell_pick s USING (trade_symbol)
WHERE s.sell_price > b.buy_price
;
"""

APPEND_ARBITRAGE_HISTORY_SQL = """
INSERT OR IGNORE INTO trade_arbitrage_history (
  trade_symbol, buy_waypoint, buy_price, sell_waypoint, sell_price,
  delta, computed_bucket, computed_at
)
SELECT
  trade_symbol, buy_waypoint, buy_price, sell_waypoint, sell_price, delta,
  strftime('%Y-%m-%d %H:00:00', computed_at) AS computed_bucket,
  computed_at
FROM trade_arbitrage;
"""

ROLLUP_OHLC_SQL_TMPL = """
INSERT OR REPLACE INTO market_goods_ohlc_hourly (
  waypoint_symbol, trade_symbol, bucket_start,
  open_buy, high_buy, low_buy, close_buy,
  open_sell, high_sell, low_sell, close_sell,
  sample_count
)
WITH src AS (
  SELECT
    waypoint_symbol,
    trade_symbol,
    strftime('%Y-%m-%d %H:00:00', observed_at) AS bucket_start,
    observed_at,
    purchase_price,
    sell_price
  FROM market_goods_snapshots
  WHERE observed_at >= datetime('now','-{lookback} hours')
),
ordered AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY waypoint_symbol, trade_symbol, bucket_start
      ORDER BY observed_at ASC
    ) AS rn_open,
    ROW_NUMBER() OVER (
      PARTITION BY waypoint_symbol, trade_symbol, bucket_start
      ORDER BY observed_at DESC
    ) AS rn_close
  FROM src
),
agg AS (
  SELECT
    waypoint_symbol,
    trade_symbol,
    bucket_start,
    MAX(purchase_price) AS high_buy,
    MIN(purchase_price) AS low_buy,
    MAX(sell_price)     AS high_sell,
    MIN(sell_price)     AS low_sell,
    COUNT(*) AS sample_count
  FROM src
  GROUP BY 1,2,3
),
opens AS (
  SELECT waypoint_symbol, trade_symbol, bucket_start,
         purchase_price AS open_buy,
         sell_price     AS open_sell
  FROM ordered WHERE rn_open = 1
),
closes AS (
  SELECT waypoint_symbol, trade_symbol, bucket_start,
         purchase_price AS close_buy,
         sell_price     AS close_sell
  FROM ordered WHERE rn_close = 1
)
SELECT
  a.waypoint_symbol,
  a.trade_symbol,
  a.bucket_start,
  o.open_buy,
  a.high_buy,
  a.low_buy,
  c.close_buy,
  o.open_sell,
  a.high_sell,
  a.low_sell,
  c.close_sell,
  a.sample_count
FROM agg a
LEFT JOIN opens  o USING (waypoint_symbol, trade_symbol, bucket_start)
LEFT JOIN closes c USING (waypoint_symbol, trade_symbol, bucket_start);
"""

# ------------------------ helpers ------------------------

def _resolve_db_path(env_override: Optional[str] = None) -> str:
    """
    Resolve DB path with this priority:
      1) explicit `env_override` (or CLI positional),
      2) SPACETRADERS_DB_PATH,
      3) ST_DB_PATH,
      4) DATABASE_PATH,
      5) DATABASE_URL (expects sqlite:///absolute/or/relative/path).
    """
    if env_override:
        return env_override

    candidates = [
        os.getenv("SPACETRADERS_DB_PATH"),
        os.getenv("ST_DB_PATH"),
        os.getenv("DB_PATH"),
        #_from_database_url(os.getenv("DATABASE_URL")),
    ]
    for c in candidates:
        if c:
            return c
    raise SystemExit(
        "No DB path found. Set SPACETRADERS_DB_PATH (or ST_DB_PATH / DATABASE_PATH), "
        "or provide DATABASE_URL=sqlite:///path/to/spacetraders.db"
    )

def _from_database_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    u = url.strip()
    if u.startswith("sqlite:///"):
        return u[len("sqlite:///"):]
    if u.startswith("file:"):  # sqlite uri mode; let sqlite handle it as-is
        return u
    return None

def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_schema(conn: sqlite3.Connection) -> None:
    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_FILE}")
    sql = SCHEMA_FILE.read_text(encoding="utf-8")
    conn.executescript(sql)

def refresh(conn: sqlite3.Connection, lookback_hours: int = 72) -> None:
    conn.executescript(REFRESH_ARBITRAGE_SQL)
    conn.executescript(APPEND_ARBITRAGE_HISTORY_SQL)
    ohlc_sql = ROLLUP_OHLC_SQL_TMPL.format(lookback=lookback_hours)
    conn.executescript(ohlc_sql)

# --------------------- public entrypoints ---------------------

def refresh_trade_views(
    db_path: Optional[str] = None,
    *,
    lookback_hours: int = 72,
    create_schema: bool = True,
) -> None:
    """
    Call this from runners. If db_path is None, it is resolved from environment/.env.
    """
    path = _resolve_db_path(db_path)
    conn = _connect(path)
    try:
        if create_schema:
            init_schema(conn)
        refresh(conn, lookback_hours=lookback_hours)
        conn.commit()
    finally:
        conn.close()

def main(
    db_path: Optional[str] = None,
    *,
    lookback_hours: int = 72,
    create_schema: bool = True,
) -> None:
    refresh_trade_views(db_path=db_path, lookback_hours=lookback_hours, create_schema=create_schema)

# -------------------------- CLI -----------------------------

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Initialize and refresh SpaceTraders market analytics tables for SQLite.")
    ap.add_argument("db_path", nargs="?", help="Path to your SQLite DB file (if omitted, read from .env)")
    ap.add_argument("--lookback-hours", type=int, default=72, help="Hours to roll up into OHLC (default: 72)")
    ap.add_argument("--no-create-schema", action="store_true", help="Skip applying schema file (use if already created)")
    args = ap.parse_args()

    main(
        db_path=args.db_path,
        lookback_hours=args.lookback_hours,
        create_schema=not args.no_create_schema,
    )
