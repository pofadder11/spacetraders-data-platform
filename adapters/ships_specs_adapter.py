from __future__ import annotations
from domain.ships_specs import ShipsSpecs

def g(obj, *attrs):
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def adapt_ships_specs_from_ship(dto) -> ShipsSpecs:
    """
    Build ShipsSpecs from a full Ship DTO (from FleetApi.get_my_ships()).
    Snake_case only.
    """
    # mounts/modules are arrays of objects with .symbol or .name
    raw_mounts = getattr(dto, "mounts", None) or []
    raw_modules = getattr(dto, "modules", None) or []
    mounts = [getattr(m, "symbol", None) or getattr(m, "name", None) for m in raw_mounts]
    modules = [getattr(m, "symbol", None) or getattr(m, "name", None) for m in raw_modules]

    return ShipsSpecs(
        symbol=getattr(dto, "symbol", None),
        role=g(dto, "registration", "role"),

        # frame & engine
        frame_name=g(dto, "frame", "name"),
        frame_module_slots=g(dto, "frame", "module_slots"),
        frame_mounting_points=g(dto, "frame", "mounting_points"),
        engine_name=g(dto, "engine", "name"),
        speed=g(dto, "engine", "speed"),

        # lists
        mounts=[m for m in mounts if m],
        modules=[m for m in modules if m],

        # capacity (mirroring from cargo)
        capacity=g(dto, "cargo", "capacity"),
    )
