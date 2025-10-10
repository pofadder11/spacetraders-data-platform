# adapters/cargo_event_adapter.py
from __future__ import annotations
from typing import Optional
from datetime import datetime
from domain.cargo_event import CargoEvent

def g(obj, *attrs):
    cur = obj
    for a in attrs:
        cur = getattr(cur, a, None)
        if cur is None:
            return None
    return cur

def _waypoint_from_any(resp_dto) -> Optional[str]:
    # Many actions include the ship nav/route/waypoint or transaction.waypoint_symbol.
    # Prefer explicit waypoint on resp if any; fall back to None.
    return (
        getattr(resp_dto, "waypoint_symbol", None)
        or g(resp_dto, "transaction", "waypoint_symbol")
        or g(resp_dto, "nav", "waypoint_symbol")
    )

# ---------------------------
# extract_resources
# ---------------------------
def adapt_extract_to_event(resp_dto, ship_symbol: str) -> CargoEvent:
    """
    Response shape typically includes:
      extraction.ship_symbol (sometimes)
      extraction.yield.symbol/units
      cooldown.total_seconds/expiration
      cargo.units, cargo.inventory (list)
      modifiers (list), events (list)
    """
    return CargoEvent(
        event_type="EXTRACT",
        ship_symbol=ship_symbol,
        waypoint_symbol=_waypoint_from_any(resp_dto),
        timestamp=getattr(resp_dto, "timestamp", None),  # some SDKs include this; OK if None
        yield_symbol=g(resp_dto, "extraction", "yield_", "symbol") or g(resp_dto, "extraction", "yield", "symbol"),
        yield_units=g(resp_dto, "extraction", "yield_", "units") or g(resp_dto, "extraction", "yield", "units"),
        cargo_units_after=g(resp_dto, "cargo", "units"),
        cooldown_total_seconds=g(resp_dto, "cooldown", "total_seconds"),
        cooldown_expiration=g(resp_dto, "cooldown", "expiration"),
        inventory=getattr(resp_dto, "inventory", None) or g(resp_dto, "cargo", "inventory"),
        modifiers=getattr(resp_dto, "modifiers", None),
        events=getattr(resp_dto, "events", None),
    )

# ---------------------------
# ship_refine
# ---------------------------
def adapt_refine_to_event(resp_dto, ship_symbol: str) -> CargoEvent:
    """
    Response typically includes:
      produced: [{trade_symbol, units}]
      consumed: [{trade_symbol, units}]
      cargo.units/inventory, modifiers, cooldown
    """
    return CargoEvent(
        event_type="REFINE",
        ship_symbol=ship_symbol,
        waypoint_symbol=_waypoint_from_any(resp_dto),
        timestamp=getattr(resp_dto, "timestamp", None),
        cargo_units_after=g(resp_dto, "cargo", "units"),
        cooldown_total_seconds=g(resp_dto, "cooldown", "total_seconds"),
        cooldown_expiration=g(resp_dto, "cooldown", "expiration"),
        inventory=g(resp_dto, "cargo", "inventory"),
        modifiers=getattr(resp_dto, "modifiers", None),
        produced=getattr(resp_dto, "produced", None),
        consumed=getattr(resp_dto, "consumed", None),
    )

# ---------------------------
# jettison
# ---------------------------
def adapt_jettison_to_event(resp_dto, ship_symbol: str) -> CargoEvent:
    """
    Response typically includes:
      cargo.units/inventory after jettison
      and the units jettisoned (often in request; sometimes echoed)
    """
    # Try to infer the traded item symbol/units from inventory change is hard; capture units if present.
    units = getattr(resp_dto, "units", None) or g(resp_dto, "jettisoned", "units")
    trade_symbol = getattr(resp_dto, "trade_symbol", None) or g(resp_dto, "jettisoned", "symbol")

    return CargoEvent(
        event_type="JETTISON",
        ship_symbol=ship_symbol,
        waypoint_symbol=_waypoint_from_any(resp_dto),
        timestamp=getattr(resp_dto, "timestamp", None),
        trade_symbol=trade_symbol,
        units=units,
        cargo_units_after=g(resp_dto, "cargo", "units"),
        inventory=g(resp_dto, "cargo", "inventory"),
        # no cooldown, no modifiers usually
    )

# ---------------------------
# transfer_cargo
# ---------------------------
def adapt_transfer_to_event(resp_dto, ship_symbol: str, other_ship_symbol: Optional[str] = None) -> CargoEvent:
    """
    Response typically includes updated cargo for the source (or target) ship:
      cargo.units/inventory
    Pass `other_ship_symbol` if you have it from the request context.
    """
    # Units & symbol may not appear in response; include if present
    units = getattr(resp_dto, "units", None) or g(resp_dto, "transfer", "units")
    trade_symbol = getattr(resp_dto, "trade_symbol", None) or g(resp_dto, "transfer", "trade_symbol")

    return CargoEvent(
        event_type="TRANSFER",
        ship_symbol=ship_symbol,
        other_ship_symbol=other_ship_symbol,
        waypoint_symbol=_waypoint_from_any(resp_dto),
        timestamp=getattr(resp_dto, "timestamp", None),
        trade_symbol=trade_symbol,
        units=units,
        cargo_units_after=g(resp_dto, "cargo", "units"),
        inventory=g(resp_dto, "cargo", "inventory"),
        # no cooldown usually
    )
