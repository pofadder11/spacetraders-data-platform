from typing import Any, Dict, Iterable, List, Optional, Tuple
from dataclasses import dataclass, field
from domain.ships_activity import ShipsActivity
from domain.ships_specs import ShipsSpecs
from domain.ship_market import ShipMarketRow
from adapters.ships_activity_adapter import merge_activity_with_nav

@dataclass
class FleetState:
    """Local, easily-referenced state for your session."""
    # Activity & Specs keyed by ship symbol
    activities: Dict[str, ShipsActivity] = field(default_factory=dict)
    specs: Dict[str, ShipsSpecs] = field(default_factory=dict)

    # Shipyard listings cached by waypoint
    ship_market: Dict[str, List[ShipMarketRow]] = field(default_factory=dict)

    def ensure_activity(self, symbol: str) -> ShipsActivity:
        a = self.activities.get(symbol)
        if a is None:
            a = ShipsActivity(symbol=symbol)
            self.activities[symbol] = a
        return a

    def update_activity_from_nav(self, symbol: str, nav_dto: Any) -> ShipsActivity:
        current = self.ensure_activity(symbol)
        updated = merge_activity_with_nav(current, nav_dto)
        self.activities[symbol] = updated
        return updated

    def update_activity_from_refuel(self, symbol: str, resp_dto: Any) -> ShipsActivity:
        """Use refuel response to update fuel state in local activity."""
        current = self.ensure_activity(symbol)
        fuel_cur = getattr(getattr(resp_dto, "fuel", None), "current", None)
        fuel_cap = getattr(getattr(resp_dto, "fuel", None), "capacity", None)
        patched = current.model_copy(update={
            "fuel_current": fuel_cur if fuel_cur is not None else current.fuel_current,
            "fuel_capacity": fuel_cap if fuel_cap is not None else current.fuel_capacity,
        })
        self.activities[symbol] = patched
        return patched