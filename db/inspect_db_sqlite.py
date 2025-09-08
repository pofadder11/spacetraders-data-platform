#!/usr/bin/env python3
"""
inspect_db_sqlite.py — pretty-print recent rows from spacetraders.db using sqlite3 only.

Usage:
  python inspect_db_sqlite.py           # show last 10 rows per table
  python inspect_db_sqlite.py 5         # show last 5 rows per table

It expects tables created via db/auto_repo_sqlite.py:
  - ships_activity
  - ships_specs
"""

from __future__ import annotations
import sys
import sqlite3
from typing import Any, List, Dict


DB_PATH = "spacetraders.db"
TABLES = ["ships_activity", "ships_specs"]


def open_conn(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


def table_exists(con: sqlite3.Connection, table: str) -> bool:
    cur = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    )
    return cur.fetchone() is not None


def get_columns(con: sqlite3.Connection, table: str) -> List[str]:
    cur = con.execute(f"PRAGMA table_info({table})")
    cols = [row["name"] for row in cur.fetchall()]
    return cols


def fetch_recent(con: sqlite3.Connection, table: str, limit: int) -> List[Dict[str, Any]]:
    cols = get_columns(con, table)
    order_col = "updated_at" if "updated_at" in cols else "rowid"
    cur = con.execute(
        f"SELECT * FROM {table} ORDER BY {order_col} DESC LIMIT ?",
        (limit,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    return rows


def print_table(title: str, rows: List[Dict[str, Any]]) -> None:
    print(f"\n=== {title} (rows={len(rows)}) ===")
    if not rows:
        print("(no rows)")
        return
    # Determine column order: keys from first row
    cols = list(rows[0].keys())
    # Compute widths
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    # Header
    header = " | ".join(c.ljust(widths[c]) for c in cols)
    sep = "-+-".join("-" * widths[c] for c in cols)
    print(header)
    print(sep)
    # Rows
    for r in rows:
        print(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))


def main() -> None:
    try:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except Exception:
        limit = 10

    con = open_conn(DB_PATH)
    try:
        for t in TABLES:
            if not table_exists(con, t):
                print(f"\n=== {t} ===")
                print("(table not found — write something first with your runner)")
                continue
            rows = fetch_recent(con, t, limit)
            print_table(t, rows)
    finally:
        con.close()


if __name__ == "__main__":
    main()
