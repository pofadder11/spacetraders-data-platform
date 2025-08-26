import sqlite3
from typing import Any, Dict, List


def init_db(db_path: str = "spacetraders.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Load schema from external .sql file
    with open("api/db/schema.sql", "r") as f:
        cur.executescript(f.read())

    conn.commit()
    return conn


def normalize_waypoints(conn: sqlite3.Connection, data: List[Dict[str, Any]]) -> None:
    cur = conn.cursor()

    for waypoint in data:
        symbol = waypoint["symbol"]
        system_symbol = waypoint["systemSymbol"]
        wtype = waypoint["type"]

        # Insert or replace waypoint
        cur.execute(
            """
            INSERT OR REPLACE INTO waypoints (symbol, system_symbol, type)
            VALUES (?, ?, ?)
            """,
            (symbol, system_symbol, wtype),
        )

        # Clear existing traits for this waypoint
        cur.execute("DELETE FROM traits WHERE waypoint_symbol = ?", (symbol,))

        # Insert traits
        for trait in waypoint.get("traits", []):
            cur.execute(
                """
                INSERT INTO traits (waypoint_symbol, trait_symbol)
                VALUES (?, ?)
                """,
                (symbol, trait["symbol"]),
            )

    conn.commit()


def normalize_shipyards(raw_json: dict) -> List[Dict[str, Any]]:
    """Extract shipyard data from raw API response."""
    rows = []
    for wp in raw_json["data"]:
        if any(tr["symbol"] == "SHIPYARD" for tr in wp.get("traits", [])):
            rows.append(
                {
                    "shipyard_symbol": wp["symbol"],
                    "waypoint_symbol": wp["symbol"],
                    "system_symbol": wp["systemSymbol"],
                    "is_under_construction": int(wp.get("isUnderConstruction", False)),
                    "faction_symbol": wp.get("faction", {}).get("symbol"),
                }
            )
    return rows


def normalize_fleet(conn: sqlite3.Connection, data: List[Dict[str, Any]]) -> None:
    cur = conn.cursor()

    for ship in data:
        symbol = ship["symbol"]
        ship.get("registration", {})
        nav = ship.get("nav", {})
        route = nav.get("route", {})
        route.get("origin", {})
        route.get("destination", {})
        crew = ship.get("crew", {})
        ship.get("frame", {})
        ship.get("reactor", {})
        ship.get("engine", {})
        fuel = ship.get("fuel", {})
        cooldown = ship.get("cooldown", {})
        cargo = ship.get("cargo", {})

        # Insert or replace fleet_nav record
        cur.execute(
            """
            INSERT OR REPLACE INTO fleet_nav (
                ship_symbol, name, faction_symbol, role,
                system_symbol, waypoint_symbol,
                route_origin_symbol, route_origin_type,
                route_destination_symbol, route_destination_type,
                status, flight_mode,
                fuel_current, fuel_capacity,
                cargo_capacity, cargo_units,
                cooldown_remaining_seconds
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol,
                ship.get("registration", {}).get("name"),
                ship.get("registration", {}).get("factionSymbol"),
                ship.get("registration", {}).get("role"),
                nav.get("systemSymbol"),
                nav.get("waypointSymbol"),
                nav.get("route", {}).get("origin", {}).get("symbol"),
                nav.get("route", {}).get("origin", {}).get("type"),
                nav.get("route", {}).get("destination", {}).get("symbol"),
                nav.get("route", {}).get("destination", {}).get("type"),
                nav.get("status"),
                nav.get("flightMode"),
                fuel.get("current"),
                fuel.get("capacity"),
                cargo.get("capacity"),
                cargo.get("units"),
                cooldown.get("remainingSeconds"),
            ),
        )

        # Insert or replace fleet_specs record
        cur.execute(
            """
            INSERT OR REPLACE INTO fleet_specs (
                ship_symbol,
                frame_symbol, frame_name, frame_condition, frame_integrity,
                frame_module_slots, frame_mounting_points,
                reactor_symbol, reactor_name, reactor_power_output,
                engine_symbol, engine_name, engine_speed,
                crew_current, crew_required, crew_capacity, crew_rotation, crew_morale,
                quality
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol,
                ship.get("frame", {}).get("symbol"),
                ship.get("frame", {}).get("name"),
                ship.get("frame", {}).get("condition"),
                ship.get("frame", {}).get("integrity"),
                ship.get("frame", {}).get("moduleSlots"),
                ship.get("frame", {}).get("mountingPoints"),
                ship.get("reactor", {}).get("symbol"),
                ship.get("reactor", {}).get("name"),
                ship.get("reactor", {}).get("powerOutput"),
                ship.get("engine", {}).get("symbol"),
                ship.get("engine", {}).get("name"),
                ship.get("engine", {}).get("speed"),
                crew.get("current"),
                crew.get("required"),
                crew.get("capacity"),
                crew.get("rotation"),
                crew.get("morale"),
                ship.get("registration", {}).get("quality"),
            ),
        )

    conn.commit()
    print("\n✅ Fleet normalization complete.\n")
