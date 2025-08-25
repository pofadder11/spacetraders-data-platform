import sqlite3
from typing import Any, Dict, List


def init_db(db_path: str = "spacetraders.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

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
