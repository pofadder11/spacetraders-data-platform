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
    cargo_capacity INTEGER,
    cargo_units INTEGER,
    fuel_current INTEGER,
    fuel_capacity INTEGER,
    

    cooldown_remaining_seconds INTEGER
);

-- Technical / ship specs
CREATE TABLE IF NOT EXISTS fleet_specs (
    ship_symbol TEXT PRIMARY KEY,
    frame_symbol TEXT,
    frame_name TEXT,
    frame_condition REAL,
    frame_integrity REAL,
    frame_description TEXT,
    frame_moduleSlots INTEGER,
    frame_mountingPoints INTEGER,
    frame_fuelCapacity INTEGER,
    frame_requirements_power INTEGER,
    frame_requirements_crew INTEGER,
    frame_quality INTEGER,
    reactor_symbol TEXT,
    reactor_name TEXT,
    reactor_condition REAL,
    reactor_integrity REAL,
    reactor_description TEXT,
    reactor_powerOutput REAL,
    reactor_requirements_crew INTEGER,
    reactor_quality INTEGER,
    engine_symbol TEXT,
    engine_name TEXT,
    engine_condition REAL,
    engine_integrity REAL,
    engine_description TEXT,
    engine_speed REAL,
    engine_requirements_power INTEGER,
    engine_requirements_crew INTEGER,
    engine_quality INTEGER,
    registration_name TEXT,
    registration_factionSymbol TEXT,
    registration_role TEXT,
    crew_current INTEGER,
    crew_required INTEGER,
    crew_capacity INTEGER,
    crew_rotation TEXT,
    crew_morale REAL,
    cargo_capacity INTEGER,
    cargo_units INTEGER,
    fuel_current INTEGER,
    fuel_capacity INTEGER,
    cooldown_remainingSeconds INTEGER
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

-- -----------------------------
-- Contracts
-- -----------------------------
CREATE TABLE IF NOT EXISTS contracts (
    contract_id TEXT PRIMARY KEY,
    type TEXT,
    deadline TEXT,
    payment_on_accept INTEGER,
    payment_on_complete INTEGER,
    accepted INTEGER,
    fulfilled INTEGER,
    trade_symbol TEXT,
    destination_symbol TEXT,
    units_required INTEGER,
    units_fulfilled INTEGER
);

-- -----------------------------
-- Routes
-- -----------------------------
CREATE TABLE IF NOT EXISTS journeys (
    ship_symbol TEXT PRIMARY KEY,
    arrival_time TEXT,
    dest_x TEXT,
    dest_y TEXT,
    ori_x TEXT,
    ori_y TEXT,
);
