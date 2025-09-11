from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShipsActivity(BaseModel):
    symbol: str

    # nav / status
    status: Optional[str] = None
    dep_time: Optional[datetime] = None
    arr_time: Optional[datetime] = None
    flight_mode: Optional[str] = None

    # cooldown
    cooldown_remaining_seconds: Optional[int] = None
    cooldown_expiration: Optional[datetime] = None

    # cargo / fuel
    cargo_units: Optional[int] = None
    cargo_capacity: Optional[int] = None
    fuel_current: Optional[int] = None
    fuel_capacity: Optional[int] = None

    # waypoints
    current_waypoint: Optional[str] = None
    destination_waypoint: Optional[str] = None

    # misc
    condition: Optional[float] = None

    @property
    def fuel_level(self) -> float | None:
        if self.fuel_current is None or self.fuel_capacity in (None, 0):
            return None
        return self.fuel_current / self.fuel_capacity

    @property
    def transit_check(self) -> bool:
        if self.status == "IN_TRANSIT":
            print("waiting for flight to end")
            return True
        else:
            print("Not in transit, READY")
            return False

    @property
    def refuel_check(self) -> bool:
        if self.fuel_level is not None and self.fuel_level < 1:
            print("refueling")
            return True
        else:
            print("Fuel tank full, READY")
            return False

    @property
    def in_orbit_check(self) -> bool:
        if self.status == "IN_ORBIT":
            print("In orbit, READY TO NAVIGATE")
            return True
        else:
            print("Not in orbit, going into orbit now")
            return False
