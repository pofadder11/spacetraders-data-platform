import sqlite3
from typing import Any, Dict, List


def init_db(db_path: str = "spacetraders.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # -----------------------------
    # Existing tables
    # -----------------------------
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS waypoints (
            symbol TEXT PRIMARY KEY,
            system_symbol TEXT NOT NULL,
            type TEXT NOT NULL
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS traits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waypoint_symbol TEXT NOT NULL,
            trait_symbol TEXT NOT NULL,
            FOREIGN KEY (waypoint_symbol) REFERENCES waypoints(symbol)
        );
        """
    )

    # -----------------------------
    # New tables for shipyards
    # -----------------------------
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS shipyards (
            shipyard_symbol TEXT PRIMARY KEY,
            waypoint_symbol TEXT NOT NULL,
            system_symbol TEXT NOT NULL,
            is_under_construction INTEGER DEFAULT 0,
            faction_symbol TEXT
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS shipyard_ships (
            shipyard_symbol TEXT,
            ship_type TEXT,
            cost INTEGER,
            other_details TEXT,
            PRIMARY KEY (shipyard_symbol, ship_type),
            FOREIGN KEY (shipyard_symbol) REFERENCES shipyards(shipyard_symbol)
        );
        """
    )

    conn.commit()
    return conn


def normalize_waypoints(
    conn: sqlite3.Connection, data: List[Dict[str, Any]]
) -> None:
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
                    "is_under_construction": int(
                        wp.get("isUnderConstruction", False)
                    ),
                    "faction_symbol": wp.get("faction", {}).get("symbol"),
                }
            )
    return rows
