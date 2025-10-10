# adapters/waypoint_adapter.py
from __future__ import annotations
from typing import Iterable, List
from domain.waypoint_ref import WaypointRef

def g(obj, *attrs):
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def adapt_waypoint(dto) -> WaypointRef:
    """
    Map a SystemsApi.get_system_waypoints(...) waypoint DTO (snake_case) to WaypointRef.
    """
    # orbitals, traits, modifiers are lists of model objects; keep as raw objects
    # (auto_repo_sqlite will JSON-serialize them on write)
    return WaypointRef(
        symbol=getattr(dto, "symbol", None),
        type=getattr(dto, "type", None),
        x=getattr(dto, "x", None),
        y=getattr(dto, "y", None),
        orbitals=getattr(dto, "orbitals", None),
        faction_symbol=g(dto, "faction", "symbol"),
        modifiers=getattr(dto, "modifiers", None),
        is_under_construction=getattr(dto, "is_under_construction", None),
    )

def adapt_waypoints(list_dto: Iterable[object]) -> List[WaypointRef]:
    return [adapt_waypoint(wp) for wp in list_dto]
