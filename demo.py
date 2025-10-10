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
