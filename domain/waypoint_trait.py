# domain/waypoint_trait.py
from __future__ import annotations
from typing import Optional, Iterable, List
from pydantic import BaseModel

class WaypointTraitRow(BaseModel):
    # Deterministic PK: waypoint + trait (keeps upserts idempotent)
    id: str

    waypoint_symbol: str
    type: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None

    trait_symbol: str
    trait_description: Optional[str] = None

    # Fast helper to list unique waypoint symbols that have the MARKETPLACE trait
    @staticmethod
    def list_marketplaces(rows: Iterable["WaypointTraitRow"]) -> List[str]:
        seen = set()
        out: List[str] = []
        for r in rows:
            # hot-path checks first
            if getattr(r, "trait_symbol", None) != "MARKETPLACE":
                continue
            wp = getattr(r, "waypoint_symbol", None)
            if not wp or wp in seen:
                continue
            seen.add(wp)
            out.append(wp)
        return out
