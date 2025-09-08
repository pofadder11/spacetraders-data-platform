#!/usr/bin/env bash
set -euo pipefail

# ---- 0) Project init ---------------------------------------------------------
mkdir -p domain adapters services
touch __init__.py domain/__init__.py adapters/__init__.py services/__init__.py

# ---- 1) pyproject (pydantic v2) ---------------------------------------------
cat > pyproject.toml <<'PYPROJ'
[project]
name = "st-domain-slices"
version = "0.1.0"
description = "SpaceTraders domain slices (activity/specs) + adapters"
readme = "README.md"
requires-python = ">=3.10"
dependencies = ["pydantic>=2.6,<3"]

[tool.ruff]
line-length = 100
PYPROJ

# ---- 2) domain models --------------------------------------------------------
cat > domain/ships_activity.py <<'PY'
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ShipsActivity(BaseModel):
    """
    Telemetry slice for a ship: status, cooldown, cargo/fuel, condition, waypoints.
    Immutable to avoid accidental mutation in async/state code.
    """
    model_config = ConfigDict(frozen=True)

    symbol: str

    # nav / status
    status: Optional[str] = None
    flight_mode: Optional[str] = None

    # cooldown
    cooldown_remaining_seconds: Optional[int] = None
    cooldown_expiration: Optional[datetime] = None

    # cargo / fuel
    cargo_units: Optional[int] = None
    cargo_capacity: Optional[int] = None
    fuel_current: Optional[int] = None
    fuel_capacity: Optional[int] = None

    # condition
    condition: Optional[float] = None

    # waypoints
    current_waypoint: Optional[str] = None
    destination_waypoint: Optional[str] = None

    # derived
    @property
    def fuel_level(self) -> Optional[float]:
        """0.0 -> empty, 1.0 -> full; None if capacity unknown."""
        if self.fuel_current is None or not self.fuel_capacity:
            return None
        return self.fuel_current / self.fuel_capacity

    @property
    def cargo_load(self) -> Optional[float]:
        """0.0 -> empty, 1.0 -> full; None if capacity unknown."""
        if self.cargo_units is None or not self.cargo_capacity:
            return None
        return self.cargo_units / self.cargo_capacity
PY

cat > domain/ships_specs.py <<'PY'
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
PY

# ---- 3) adapters (DTO -> domain) --------------------------------------------
cat > adapters/util.py <<'PY'
from typing import Any

def safe_get(obj: Any, path: str, default=None):
    """
    Safe navigation of nested attributes and dict keys using dotted paths.
    Example: safe_get(dto, "nav.route.destination.symbol")
    """
    cur = obj
    for part in path.split("."):
        if cur is None:
            return default
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            cur = getattr(cur, part, None)
    return cur if cur is not None else default
PY

cat > adapters/ships_activity_adapter.py <<'PY'
from __future__ import annotations
from domain.ships_activity import ShipsActivity
from .util import safe_get

def adapt_ships_activity_from_ship(dto) -> ShipsActivity:
    """
    Build ShipsActivity from a full Ship DTO (from get_my_ships()).
    Works with camelCase DTOs from OpenAPI Generator.
    """
    dest_wp = (
        safe_get(dto, "nav.route.destination.symbol")
        or safe_get(dto, "nav.route.destinationSymbol")
    )
    condition = safe_get(dto, "condition") or safe_get(dto, "frame.condition")

    return ShipsActivity(
        symbol=getattr(dto, "symbol", None),
        status=safe_get(dto, "nav.status"),
        flight_mode=safe_get(dto, "nav.flightMode"),
        cooldown_remaining_seconds=safe_get(dto, "cooldown.remainingSeconds"),
        cooldown_expiration=safe_get(dto, "cooldown.expiration"),
        cargo_units=safe_get(dto, "cargo.units"),
        cargo_capacity=safe_get(dto, "cargo.capacity"),
        fuel_current=safe_get(dto, "fuel.current"),
        fuel_capacity=safe_get(dto, "fuel.capacity"),
        condition=condition,
        current_waypoint=safe_get(dto, "nav.waypointSymbol"),
        destination_waypoint=dest_wp,
    )

def merge_activity_with_nav(existing: ShipsActivity, nav_dto) -> ShipsActivity:
    """
    Patch activity using a ShipNav DTO (from get_ship_nav()).
    Only updates fields expected from nav.
    """
    dest_wp = (
        safe_get(nav_dto, "route.destination.symbol")
        or safe_get(nav_dto, "route.destinationSymbol")
    )
    return existing.model_copy(update={
        "status": safe_get(nav_dto, "status") or existing.status,
        "flight_mode": safe_get(nav_dto, "flightMode") or existing.flight_mode,
        "current_waypoint": safe_get(nav_dto, "waypointSymbol") or existing.current_waypoint,
        "destination_waypoint": dest_wp or existing.destination_waypoint,
    })

def merge_activity_with_cooldown(existing: ShipsActivity, cooldown_dto) -> ShipsActivity:
    """Patch cooldown fields from a cooldown DTO."""
    return existing.model_copy(update={
        "cooldown_remaining_seconds": safe_get(cooldown_dto, "remainingSeconds"),
        "cooldown_expiration": safe_get(cooldown_dto, "expiration"),
    })
PY

cat > adapters/ships_specs_adapter.py <<'PY'
from __future__ import annotations
from domain.ships_specs import ShipsSpecs
from .util import safe_get

def adapt_ships_specs_from_ship(dto) -> ShipsSpecs:
    mounts = [safe_get(m, "symbol") or safe_get(m, "name") for m in (safe_get(dto, "mounts") or [])]
    modules = [safe_get(m, "symbol") or safe_get(m, "name") for m in (safe_get(dto, "modules") or [])]
    return ShipsSpecs(
        symbol=getattr(dto, "symbol", None),
        role=safe_get(dto, "registration.role"),
        frame_name=safe_get(dto, "frame.name"),
        frame_module_slots=safe_get(dto, "frame.moduleSlots"),
        frame_mounting_points=safe_get(dto, "frame.mountingPoints"),
        engine_name=safe_get(dto, "engine.name"),
        speed=safe_get(dto, "engine.speed"),
        mounts=[m for m in mounts if m],
        modules=[m for m in modules if m],
        capacity=safe_get(dto, "cargo.capacity"),
    )
PY

# ---- 4) demo script (no real API needed) ------------------------------------
cat > demo.py <<'PY'
from datetime import datetime, timedelta

# fake DTO classes that look like OpenAPI-generated objects (camelCase)
class RouteDest:
    def __init__(self, symbol): self.symbol = symbol

class Route:
    def __init__(self, destination): self.destination = destination

class Nav:
    def __init__(self, systemSymbol, waypointSymbol, status, flightMode, route=None):
        self.systemSymbol = systemSymbol
        self.waypointSymbol = waypointSymbol
        self.status = status
        self.flightMode = flightMode
        self.route = route

class Cargo:
    def __init__(self, capacity, units): self.capacity = capacity; self.units = units

class Fuel:
    def __init__(self, current, capacity): self.current = current; self.capacity = capacity

class Frame:
    def __init__(self, name, moduleSlots, mountingPoints=None, condition=None):
        self.name = name; self.moduleSlots = moduleSlots
        self.mountingPoints = mountingPoints; self.condition = condition

class Engine:
    def __init__(self, name, speed=None): self.name = name; self.speed = speed

class Registration:
    def __init__(self, role): self.role = role

class Cooldown:
    def __init__(self, remainingSeconds, expiration):
        self.remainingSeconds = remainingSeconds; self.expiration = expiration

class Mount:  # e.g. {"symbol": "MOUNT_MINING_LASER_I"}
    def __init__(self, symbol=None, name=None): self.symbol = symbol; self.name = name

class Module:
    def __init__(self, symbol=None, name=None): self.symbol = symbol; self.name = name

class ShipDTO:
    def __init__(self, symbol, registration, frame, engine, cargo, fuel, nav, mounts=None, modules=None, cooldown=None, condition=None):
        self.symbol = symbol
        self.registration = registration
        self.frame = frame
        self.engine = engine
        self.cargo = cargo
        self.fuel = fuel
        self.nav = nav
        self.mounts = mounts or []
        self.modules = modules or []
        self.cooldown = cooldown
        self.condition = condition  # sometimes at ship-level

# import the code we generated
from adapters.ships_activity_adapter import adapt_ships_activity_from_ship, merge_activity_with_nav
from adapters.ships_specs_adapter import adapt_ships_specs_from_ship
from domain.ships_activity import ShipsActivity

def main():
    # build a fake ship DTO resembling get_my_ships()
    dto = ShipDTO(
        symbol="X1-HA25-1",
        registration=Registration(role="EXPLORER"),
        frame=Frame(name="FRIGATE", moduleSlots=6, mountingPoints=4, condition=0.97),
        engine=Engine(name="ION_DRIVE", speed=4),
        cargo=Cargo(capacity=60, units=12),
        fuel=Fuel(current=54, capacity=100),
        nav=Nav(
            systemSymbol="X1-HA25",
            waypointSymbol="X1-HA25-A1",
            status="IN_ORBIT",
            flightMode="CRUISE",
            route=Route(destination=RouteDest(symbol="X1-HA25-A2"))
        ),
        mounts=[Mount(symbol="MOUNT_MINING_LASER_I"), Mount(symbol="MOUNT_SURVEYOR_I")],
        modules=[Module(symbol="MODULE_CARGO_HOLD_I")],
        cooldown=Cooldown(
            remainingSeconds=120,
            expiration=(datetime.utcnow() + timedelta(seconds=120)).isoformat() + "Z"
        ),
        condition=None,  # present at frame.level above
    )

    # adapt to our domain slices
    activity = adapt_ships_activity_from_ship(dto)
    specs = adapt_ships_specs_from_ship(dto)

    print("=== ShipsActivity (telemetry) ===")
    print(activity)
    print("fuel_level:", activity.fuel_level, "cargo_load:", activity.cargo_load)

    print("\n=== ShipsSpecs (reference) ===")
    print(specs)

    # pretend we fetched a fresher nav
    class ShipNavDTO:
        def __init__(self): 
            self.status = "IN_TRANSIT"
            self.flightMode = "CRUISE"
            self.waypointSymbol = "X1-HA25-A1"
            class Route: 
                def __init__(self): 
                    class Dest: 
                        def __init__(self): self.symbol = "X1-HA25-A3"
                    self.destination = Dest()
            self.route = Route()

    updated_nav = ShipNavDTO()
    activity2: ShipsActivity = merge_activity_with_nav(activity, updated_nav)

    print("\n=== ShipsActivity after nav update ===")
    print(activity2)
    print("fuel_level:", activity2.fuel_level, "cargo_load:", activity2.cargo_load)

if __name__ == "__main__":
    main()
PY

# ---- 5) install deps & run demo ---------------------------------------------
python - <<'PY'
import sys, subprocess, json
print("Python:", sys.version)
print("Installing deps (pydantic>=2)...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pydantic>=2.6,<3"])
print("Done.")
PY

echo
echo "✔ Project scaffolded."
echo "Run the demo with:  python demo.py"
