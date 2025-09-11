# adapters/shipyard_adapter.py
from __future__ import annotations
from typing import List
from domain.ship_market import ShipMarketRow

def g(obj, *attrs):
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def adapt_ship_market_rows(shipyard_dto, waypoint_symbol: str) -> List[ShipMarketRow]:
    """
    Map SystemsApi.get_shipyard(...) response to ShipMarketRow list.
    We iterate over 'ships' (purchasable listings). Some SDKs also expose 'ship_types'
    (strings) but the rich details live on 'ships'.
    """
    rows: List[ShipMarketRow] = []
    listings = getattr(shipyard_dto, "ships", None) or []
    mod_fee = getattr(shipyard_dto, "modifications_fee", None)

    for s in listings:
        ship_type = getattr(s, "type", None) or getattr(s, "symbol", None)
        if not ship_type:
            continue

        rows.append(ShipMarketRow(
            id=f"{waypoint_symbol}#{ship_type}",
            waypoint_symbol=waypoint_symbol,
            ship_type=ship_type,
            description=getattr(s, "description", None),
            purchase_price=getattr(s, "purchase_price", None),

            # frame
            frame_symbol=g(s, "frame", "symbol"),
            frame_condition=g(s, "frame", "condition"),
            frame_integrity=g(s, "frame", "integrity"),
            frame_module_slots=g(s, "frame", "module_slots"),
            frame_mounting_points=g(s, "frame", "mounting_points"),
            frame_fuel_capacity=g(s, "frame", "fuel_capacity"),
            frame_quality=g(s, "frame", "quality"),

            # reactor
            reactor_symbol=g(s, "reactor", "symbol"),
            reactor_condition=g(s, "reactor", "condition"),
            reactor_power_output=g(s, "reactor", "power_output"),
            reactor_quality=g(s, "reactor", "quality"),

            # engine
            engine_symbol=g(s, "engine", "symbol"),
            engine_condition=g(s, "engine", "condition"),
            engine_integrity=g(s, "engine", "integrity"),
            engine_speed=g(s, "engine", "speed"),
            engine_quality=g(s, "engine", "quality"),

            # fees
            modifications_fee=mod_fee,
        ))
    return rows
