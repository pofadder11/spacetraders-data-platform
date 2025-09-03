# runner_state.py
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

FRESH_TTL = timedelta(minutes = 2)

class ShipState(BaseModel):
    symbol: str
    nav_status: Optional[str] = None
    system_symbol: Optional[str] = None
    waypoint_symbol: Optional[str] = None
    cargo_units: Optional[int] = None
    updated_at: datetime

    @classmethod
    def from_api(cls, api_ship) -> "ShipState":
        # Adjust attribute names to match your generated client
        return cls(
            symbol=api_ship.symbol,
            nav_status=getattr(api_ship.nav, "status", None),
            system_symbol=getattr(getattr(api_ship.nav, "route", None), "system_symbol", None) or getattr(api_ship.nav, "system_symbol", None),
            waypoint_symbol=getattr(getattr(api_ship.nav, "route", None), "waypoint_symbol", None) or getattr(api_ship.nav, "waypoint_symbol", None),
            cargo_units=getattr(getattr(api_ship, "cargo", None), "units", None),
            updated_at=datetime.utcnow(),
        )
