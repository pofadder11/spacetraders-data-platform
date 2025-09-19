# domain/ship_market.py
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

class ShipMarketRow(BaseModel):
    # One row per purchasable ship type at a waypoint_shipyard
    id: str                               # f"{waypoint_symbol}#{ship_type}"

    waypoint_symbol: str                  # shipyard location
    ship_type: str                        # e.g., "SHIP_MINER", "SHIP_DRONE"
    description: Optional[str] = None
    purchase_price: Optional[int] = None

    # frame
    frame_symbol: Optional[str] = None
    frame_condition: Optional[float] = None
    frame_integrity: Optional[float] = None
    frame_module_slots: Optional[int] = None
    frame_mounting_points: Optional[int] = None
    frame_fuel_capacity: Optional[int] = None
    frame_quality: Optional[int] = None

    # reactor
    reactor_symbol: Optional[str] = None
    reactor_condition: Optional[float] = None
    reactor_power_output: Optional[int] = None
    reactor_quality: Optional[int] = None

    # engine
    engine_symbol: Optional[str] = None
    engine_condition: Optional[float] = None
    engine_integrity: Optional[float] = None
    engine_speed: Optional[int] = None
    engine_quality: Optional[int] = None

    modules: Optional[list] = None
    mounts: Optional[list] = None
    crew_required: Optional[int] = None
    crew_capacity: Optional[int] = None

    # fees
    modifications_fee: Optional[int] = None
   
