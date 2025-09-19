-- ===============================
-- SpaceTraders Market Analytics — SQLite Schema (dashboard-friendly)
-- ===============================

PRAGMA foreign_keys = ON;

-- 0) Your raw facts table (assumed existing); included here for reference.
-- CREATE TABLE IF NOT EXISTS market_goods_snapshots (
--   id TEXT PRIMARY KEY,
--   waypoint_symbol TEXT NOT NULL,
--   trade_symbol TEXT NOT NULL,
--   type TEXT,
--   trade_volume INTEGER,
--   supply TEXT,
--   activity TEXT,
--   purchase_price INTEGER,
--   sell_price INTEGER,
--   observed_at TEXT NOT NULL,
--   updated_at TEXT
-- );

-- 1) Helper: "latest" per (waypoint, trade)
DROP VIEW IF EXISTS market_goods_latest;
CREATE VIEW market_goods_latest AS
WITH ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY waypoint_symbol, trade_symbol
      ORDER BY observed_at DESC
    ) AS rn
  FROM market_goods_snapshots
)
SELECT *
FROM ranked
WHERE rn = 1;

-- 2) Current best arbitrage (materialized)
CREATE TABLE IF NOT EXISTS trade_arbitrage (
  trade_symbol      TEXT PRIMARY KEY,
  buy_waypoint      TEXT NOT NULL,
  buy_price         INTEGER NOT NULL,
  sell_waypoint     TEXT NOT NULL,
  sell_price        INTEGER NOT NULL,
  delta             INTEGER NOT NULL,
  buy_observed_at   TEXT NOT NULL,
  sell_observed_at  TEXT NOT NULL,
  computed_at       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_arbitrage_delta_desc ON trade_arbitrage(delta DESC);
CREATE INDEX IF NOT EXISTS idx_arbitrage_buy ON trade_arbitrage(buy_waypoint);
CREATE INDEX IF NOT EXISTS idx_arbitrage_sell ON trade_arbitrage(sell_waypoint);

-- 3) Arbitrage history (append-only, hourly)
CREATE TABLE IF NOT EXISTS trade_arbitrage_history (
  trade_symbol      TEXT NOT NULL,
  buy_waypoint      TEXT NOT NULL,
  buy_price         INTEGER NOT NULL,
  sell_waypoint     TEXT NOT NULL,
  sell_price        INTEGER NOT NULL,
  delta             INTEGER NOT NULL,
  computed_bucket   TEXT NOT NULL,  -- 'YYYY-MM-DD HH:00:00'
  computed_at       TEXT NOT NULL,
  PRIMARY KEY (trade_symbol, computed_bucket)
);
CREATE INDEX IF NOT EXISTS idx_arbitrage_hist_bucket ON trade_arbitrage_history(computed_bucket);
CREATE INDEX IF NOT EXISTS idx_arbitrage_hist_delta ON trade_arbitrage_history(delta);

-- 4) Hourly OHLC per (waypoint, trade)
CREATE TABLE IF NOT EXISTS market_goods_ohlc_hourly (
  waypoint_symbol   TEXT NOT NULL,
  trade_symbol      TEXT NOT NULL,
  bucket_start      TEXT NOT NULL,  -- 'YYYY-MM-DD HH:00:00'
  open_buy          INTEGER,
  high_buy          INTEGER,
  low_buy           INTEGER,
  close_buy         INTEGER,
  open_sell         INTEGER,
  high_sell         INTEGER,
  low_sell          INTEGER,
  close_sell        INTEGER,
  sample_count      INTEGER NOT NULL,
  PRIMARY KEY (waypoint_symbol, trade_symbol, bucket_start)
);
CREATE INDEX IF NOT EXISTS idx_ohlc_hourly_symbol ON market_goods_ohlc_hourly(trade_symbol);
CREATE INDEX IF NOT EXISTS idx_ohlc_hourly_bucket ON market_goods_ohlc_hourly(bucket_start);