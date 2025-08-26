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

CREATE TABLE IF NOT EXISTS shipyard_ships (
    shipyard_symbol TEXT,
    ship_type TEXT,
    cost INTEGER,
    other_details TEXT,
    PRIMARY KEY (shipyard_symbol, ship_type),
    FOREIGN KEY (shipyard_symbol) REFERENCES shipyards(shipyard_symbol)
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
