-- -----------------------------
-- Waypoints & Traits
-- -----------------------------
CREATE TABLE IF NOT EXISTS waypoints (
    symbol TEXT PRIMARY KEY,
    system_symbol TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS traits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waypoint_symbol TEXT NOT NULL,
    trait_symbol TEXT NOT NULL,
    FOREIGN KEY (waypoint_symbol) REFERENCES waypoints(symbol)
);

-- -----------------------------
-- Shipyards
-- -----------------------------
CREATE TABLE IF NOT EXISTS shipyards (
    shipyard_symbol TEXT PRIMARY KEY,
    waypoint_symbol TEXT NOT NULL,
    system_symbol TEXT NOT NULL,
    is_under_construction INTEGER DEFAULT 0,
    faction_symbol TEXT
);

-- -----------------------------
-- Ships available in shipyards
-- -----------------------------
CREATE TABLE IF NOT EXISTS shipyard_ships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waypoint_symbol TEXT NOT NULL,
    ship_type TEXT NOT NULL,
    purchase_price INTEGER,
    quality INTEGER,
    supply TEXT,
    reactor_symbol TEXT,
    engine_symbol TEXT,
    FOREIGN KEY (waypoint_symbol) REFERENCES waypoints(symbol)
);

-- -----------------------------
-- Fleet Tables
-- -----------------------------
-- Navigation / work attributes
CREATE TABLE IF NOT EXISTS fleet_nav (
    ship_symbol TEXT PRIMARY KEY,
    name TEXT,
    faction_symbol TEXT,
    role TEXT,
    system_symbol TEXT,
    waypoint_symbol TEXT,
    route_origin_symbol TEXT,
    route_origin_type TEXT,
    route_destination_symbol TEXT,
    route_destination_type TEXT,
    status TEXT,
    flight_mode TEXT,
    fuel_current INTEGER,
    fuel_capacity INTEGER,
    cargo_capacity INTEGER,
    cargo_units INTEGER,
    cooldown_remaining_seconds INTEGER
);

-- Technical / ship specs
CREATE TABLE IF NOT EXISTS fleet_specs (
    ship_symbol TEXT PRIMARY KEY,
    frame_symbol TEXT,
    frame_name TEXT,
    frame_condition REAL,
    frame_integrity REAL,
    frame_module_slots INTEGER,
    frame_mounting_points INTEGER,
    reactor_symbol TEXT,
    reactor_name TEXT,
    reactor_power_output REAL,
    engine_symbol TEXT,
    engine_name TEXT,
    engine_speed REAL,
    crew_current INTEGER,
    crew_required INTEGER,
    crew_capacity INTEGER,
    crew_rotation TEXT,
    crew_morale REAL,
    quality INTEGER
);

-- -----------------------------
-- Fleet Modules (nested list)
-- -----------------------------
CREATE TABLE IF NOT EXISTS fleet_modules (
    ship_symbol TEXT,
    module_symbol TEXT,
    module_name TEXT,
    module_class TEXT,
    module_type TEXT,
    PRIMARY KEY (ship_symbol, module_symbol),
    FOREIGN KEY (ship_symbol) REFERENCES fleet_specs(ship_symbol)
);

-- -----------------------------
-- Fleet Mounts (nested list)
-- -----------------------------
CREATE TABLE IF NOT EXISTS fleet_mounts (
    ship_symbol TEXT,
    mount_symbol TEXT,
    mount_name TEXT,
    mount_class TEXT,
    mount_type TEXT,
    PRIMARY KEY (ship_symbol, mount_symbol),
    FOREIGN KEY (ship_symbol) REFERENCES fleet_specs(ship_symbol)
);

-- -----------------------------
-- Fleet Cargo (nested object/list)
-- -----------------------------
CREATE TABLE IF NOT EXISTS fleet_cargo (
    ship_symbol TEXT,
    units INTEGER,
    capacity INTEGER,
    PRIMARY KEY (ship_symbol),
    FOREIGN KEY (ship_symbol) REFERENCES fleet_specs(ship_symbol)
);