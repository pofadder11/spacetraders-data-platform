from __future__ import annotations
from domain.ships_activity import ShipsActivity

def g(obj, *attrs):
    """Safe nested getattr: g(dto, 'nav','route','destination','symbol')."""
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def adapt_ships_activity_from_ship(dto) -> ShipsActivity:
    """
    Build ShipsActivity from a full Ship DTO (from FleetApi.get_my_ships()).
    Assumes generator produced snake_case attributes (Python convention).
    """
    return ShipsActivity(
        symbol=getattr(dto, "symbol", None),

        # nav / status + times
        status=g(dto, "nav", "status"),
        dep_time=g(dto, "nav", "route", "departure_time"),
        arr_time=g(dto, "nav", "route", "arrival"),
        flight_mode=g(dto, "nav", "flight_mode"),

        # cooldown
        cooldown_remaining_seconds=g(dto, "cooldown", "remaining_seconds"),
        cooldown_expiration=g(dto, "cooldown", "expiration"),

        # cargo / fuel
        cargo_units=g(dto, "cargo", "units"),
        cargo_capacity=g(dto, "cargo", "capacity"),
        fuel_current=g(dto, "fuel", "current"),
        fuel_capacity=g(dto, "fuel", "capacity"),

        # waypoints
        current_waypoint=g(dto, "nav", "waypoint_symbol"),
        destination_waypoint=g(dto, "nav", "route", "destination", "symbol"),

        # condition (often on frame, sometimes on ship root)
        condition=(g(dto, "frame", "condition") or getattr(dto, "condition", None)),
    )

def merge_activity_with_nav(existing: ShipsActivity, nav_dto) -> ShipsActivity:
    """
    Patch activity using a ShipNav DTO (from FleetApi.get_ship_nav()).
    Only updates nav-related fields.
    """
    return existing.model_copy(update={
        "status": getattr(nav_dto, "status", None) or existing.status,
        "dep_time": g(nav_dto, "route", "departure_time") or existing.dep_time,
        "arr_time": g(nav_dto, "route", "arrival") or existing.arr_time,
        "flight_mode": getattr(nav_dto, "flight_mode", None) or existing.flight_mode,
        "current_waypoint": getattr(nav_dto, "waypoint_symbol", None) or existing.current_waypoint,
        "destination_waypoint": g(nav_dto, "route", "destination", "symbol") or existing.destination_waypoint,
        # cooldown is not part of ShipNav; keep existing
    })
