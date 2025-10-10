from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ShipsSpecs(BaseModel):
    """
    Reference/spec slice for a ship: mounts, modules, speed, capacity, role, frame.
    Immutable so it can be shared safely across readers.
    """
    model_config = ConfigDict(frozen=True)

    symbol: str
    role: Optional[str] = None

    # frame & engine
    frame_name: Optional[str] = None
    frame_module_slots: Optional[int] = None
    frame_mounting_points: Optional[int] = None
    engine_name: Optional[str] = None
    speed: Optional[int] = None  # often from engine.speed

    # mounts/modules
    mounts: List[str] = []
    modules: List[str] = []

    # keep capacity here too (per your preference)
    capacity: Optional[int] = None
