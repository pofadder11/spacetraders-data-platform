# services/ingestion.py
from __future__ import annotations
from sqlalchemy.orm import Session
from services.client_service import OpenAPIService
from services.normalizer import upsert_fleet_nav, upsert_market_trade_goods, upsert_ships_current

def refresh_fleet_nav(svc: OpenAPIService, session: Session) -> int:
    # Using the data-proxy so this returns the inner .data directly
    ships = svc.d.fleet.get_my_ships()
    return upsert_fleet_nav(session, ships)


def refresh_market_from_api(
    svc: OpenAPIService, session: Session, system_symbol: str, waypoint_symbol: str
) -> int:
    """
    Fetch market via API and persist trade goods snapshot.
    Returns number of rows upserted.
    """
    market = svc.d.systems.get_market(system_symbol, waypoint_symbol)
    return upsert_market_trade_goods(session, market)


def refresh_ships_current(svc: OpenAPIService, session: Session) -> tuple[int, int]:
    """
    Fetch fleet and upsert both ships_current and fleet_nav. Returns (ships_current_count, fleet_nav_count).
    """
    ships = svc.d.fleet.get_my_ships()
    c1 = upsert_ships_current(session, ships)
    c2 = upsert_fleet_nav(session, ships)
    return c1, c2
