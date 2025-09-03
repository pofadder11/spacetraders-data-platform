# services/ingestion.py
from __future__ import annotations
from sqlalchemy.orm import Session
from services.client_service import OpenAPIService
from services.normalizer import upsert_fleet_nav

def refresh_fleet_nav(svc: OpenAPIService, session: Session) -> int:
    # Using the data-proxy so this returns the inner .data directly
    ships = svc.d.fleet.get_my_ships()
    return upsert_fleet_nav(session, ships)
