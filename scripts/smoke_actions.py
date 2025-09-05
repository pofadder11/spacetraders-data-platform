"""Lightweight smoke test for services.api_groups and services.actions.

Defaults to read-only (no API writes) and in-memory DB to avoid creating files.

Usage examples:
  - Read-only, in-memory DB (default):
      python scripts/smoke_actions.py

  - Use write-through ETL namespace (persists to DB handlers) but still GET-only:
      python scripts/smoke_actions.py --mode etl

  - Persist to local DB (uses DATABASE_URL or sqlite file):
      python scripts/smoke_actions.py --persist-db
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["api", "etl"],
        default="api",
        help="Use read-only data-proxy ('api') or write-through ('etl') namespace.",
    )
    parser.add_argument(
        "--persist-db",
        action="store_true",
        help="Persist to DATABASE_URL instead of using in-memory sqlite.",
    )
    args = parser.parse_args()

    # Avoid creating local sqlite files by default
    if not args.persist_db:
        os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

    # Ensure project root is on sys.path, then load env before imports
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    # Load env before importing service modules
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        load_dotenv = lambda: None  # no-op if dotenv is unavailable
    load_dotenv()

    if not os.getenv("BEARER_TOKEN"):
        print("[error] Missing BEARER_TOKEN in environment. Create .env or set env var.")
        return 2

    # Now import services
    from services import api_groups
    from services import actions as act

    # If using ETL, ensure DB schema exists
    if args.mode == "etl":
        try:
            from session import init_db
            init_db()
        except Exception as e:
            print(f"[warn] Could not initialize DB: {e}")

    # Select API handle
    api_handle: Any = api_groups.api if args.mode == "api" else api_groups.etl

    print(f"[info] Mode: {args.mode}")
    print("[step] Listing ships via actions.list_ships()")
    try:
        ships = act.list_ships(api=api_handle)
    except Exception as e:
        print(f"[fail] list_ships failed: {e}")
        return 1

    n = len(ships) if hasattr(ships, "__len__") else "?"
    print(f"[ok] Got ships: {n}")
    if n:
        ship = ships[0]
        symbol = getattr(ship, "symbol", None)
        print(f"[info] First ship: {symbol}")

        # Get nav synchronously through api proxy (read-only)
        print("[step] Fetching ship nav via api proxy (read-only)")
        try:
            # Use cross-group shortcut on the proxy
            nav = api_groups.api.get_ship_nav(symbol)
            status = getattr(nav, "status", None)
            print(f"[ok] Nav status: {status}")
        except Exception as e:
            print(f"[warn] get_ship_nav (sync) failed: {e}")

    print("[done] Smoke test completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
