# adapters/waypoint_trait_adapter.py
from __future__ import annotations
from typing import Iterable, List
from domain.waypoint_trait import WaypointTraitRow

def adapt_traits_from_waypoint_dtos(waypoints_dto: Iterable[object]) -> List[WaypointTraitRow]:
    """
    Flatten traits directly from SystemsApi.get_system_waypoints(...) DTOs.
    No dependency on WaypointRef shape; uses snake_case attributes.
    """
    rows: List[WaypointTraitRow] = []
    for dto in waypoints_dto:
        wp_symbol = getattr(dto, "symbol", None)
        if not wp_symbol:
            continue
        wptype = getattr(dto, "type", None)
        x = getattr(dto, "x", None)
        y = getattr(dto, "y", None)

        traits = getattr(dto, "traits", None) or []
        # DTO traits are usually model objects with .symbol / .description;
        # support dicts too just in case.
        for t in traits:
            t_sym = getattr(t, "symbol", None) if hasattr(t, "symbol") else (t.get("symbol") if isinstance(t, dict) else None)
            if not t_sym:
                continue
            t_desc = getattr(t, "description", None) if hasattr(t, "description") else (t.get("description") if isinstance(t, dict) else None)

            rows.append(
                WaypointTraitRow(
                    id=f"{wp_symbol}#{t_sym}",
                    waypoint_symbol=wp_symbol,
                    type=wptype,
                    x=x,
                    y=y,
                    trait_symbol=t_sym,
                    trait_description=t_desc,
                )
            )
    return rows
