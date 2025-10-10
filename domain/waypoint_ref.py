# domain/waypoint_ref.py
from __future__ import annotations
from typing import Optional, Any, List
from pydantic import BaseModel

class WaypointRef(BaseModel):
    # Primary key
    symbol: str

    # Core attributes
    type: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None

    # Arrays (auto_repo will JSON-encode)
    orbitals: Optional[List[Any]] = None            # e.g., [{"symbol": "..."}]
    modifiers: Optional[List[Any]] = None           # e.g., [{"symbol","description"}]

    # Nested scalar
    faction_symbol: Optional[str] = None

    # Construction flag
    is_under_construction: Optional[bool] = None
