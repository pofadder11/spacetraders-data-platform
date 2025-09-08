# domain/cargo_event.py
from __future__ import annotations
from typing import Optional, Literal, Any
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field

CargoEventType = Literal["EXTRACT", "REFINE", "JETTISON", "TRANSFER"]

class CargoEvent(BaseModel):
    # Primary key for DB (string uuid so auto_repo primary key works)
    event_id: str = Field(default_factory=lambda: str(uuid4()))

    # What happened / who / where / when
    event_type: CargoEventType
    ship_symbol: str
    waypoint_symbol: Optional[str] = None
    timestamp: Optional[datetime] = None          # if API provides, else None

    # Action specifics
    # For EXTRACT: yield_symbol/units
    yield_symbol: Optional[str] = None
    yield_units: Optional[int] = None

    # For TRANSFER: other ship and trade symbol/units (if available)
    other_ship_symbol: Optional[str] = None
    trade_symbol: Optional[str] = None
    units: Optional[int] = None                    # generic quantity where applicable

    # Convenience snapshots after operation
    cargo_units_after: Optional[int] = None

    # Optional cooldown fields (EXTRACT/REFINE often include cooldown)
    cooldown_total_seconds: Optional[int] = None
    cooldown_expiration: Optional[datetime] = None

    # Free-form payload pieces captured as JSON via auto_repo serialization
    # (lists/dicts will be serialized automatically by auto_repo)
    inventory: Optional[list[Any]] = None          # e.g. [{"symbol","name","units",...}, ...]
    modifiers: Optional[list[Any]] = None          # e.g. [{"symbol","name","description"}, ...]
    produced: Optional[list[Any]] = None           # REFINE: [{"tradeSymbol","units"}, ...]
    consumed: Optional[list[Any]] = None           # REFINE: [{"tradeSymbol","units"}, ...]
    events: Optional[list[Any]] = None             # e.g. [{"symbol","component","name","description"}, ...]
