# domain/journey.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JourneyRow(BaseModel):
    id: str
    ship_symbol: str
    origin_waypoint: Optional[str] = None
    destination_waypoint: Optional[str] = None
    departure_time: Optional[str] = None   # keep as TEXT from API
    arrival_time: Optional[str] = None     # keep as TEXT from API
    flight_mode: Optional[str] = None
    fuel_departure: Optional[int] = None
    cargo_departure: Optional[int] = None
    observed_at: datetime                  # snapshot timestamp (UTC)
