# run_startup.py
import sqlite3
import time
from datetime import datetime

from api.client import SpaceTradersClient
from api.normalizer import (
    normalize_fleet,
    normalize_shipyard_ships,
    normalize_shipyards,
    normalize_waypoints,
)

# -----------------------------
# Setup
# -----------------------------
client = SpaceTradersClient()
conn = sqlite3.connect("spacetraders.db")
cur = conn.cursor()

# -----------------------------
# ETL: Full refresh
# -----------------------------
normalize_waypoints(conn, client.list_waypoints())
normalize_shipyards(conn, client.list_shipyards())
normalize_fleet(conn, client.list_ships())


# -----------------------------
# Helper: Prepare ship for navigation
# -----------------------------
def prepare_ship_for_navigation(ship_symbol: str):
    normalize_fleet(conn, client.list_ships())
    cur.execute(
        """
        SELECT fn.status, fs.fuel_current, fs.fuel_capacity
        FROM fleet_nav fn
        JOIN fleet_specs fs ON fn.ship_symbol = fs.ship_symbol
        WHERE fn.ship_symbol = ?
        """,
        (ship_symbol,),
    )
    row = cur.fetchone()
    if not row:
        raise RuntimeError(f"No fleet_nav entry for ship {ship_symbol}")

    status, fuel_current, fuel_capacity = row

    if fuel_current < fuel_capacity:
        if status != "DOCKED":
            print(f"[INFO] Docking {ship_symbol} (status: {status})")
            client.dock_ship(ship_symbol)
            time.sleep(2)  # wait for docking to complete
            print(f"[INFO] Refueling {ship_symbol} ({fuel_current}/{fuel_capacity})")
            client.refuel_ship(ship_symbol)

    if status != "IN_ORBIT":
        print(f"[INFO] Orbiting {ship_symbol} (status: {status})")
        client.orbit_ship(ship_symbol)


conn.row_factory = sqlite3.Row
cur = conn.cursor()
# -----------------------------
# Select fastest available ship
# -----------------------------
cur.execute(
    """
    SELECT fs.symbol
    FROM fleet_specs fs
    JOIN fleet_nav fn ON fs.ship_symbol = fn.ship_symbol
    WHERE fn.status IN ('IN_ORBIT', 'DOCKED') AND fs.fuel_current > 0
    ORDER BY fs.engine_speed DESC
    LIMIT 1
    """
)
row = cur.fetchone()
if not row:
    raise RuntimeError("No available ship found for navigation")
ship_symbol = row[0]

prepare_ship_for_navigation(ship_symbol)

# -----------------------------
# Fetch shipyard symbols (limit 3)
# -----------------------------
cur.execute("SELECT shipyard_symbol FROM shipyards LIMIT 3")
shipyard_symbols = [row["shipyard_symbol"] for row in cur.fetchall()]

for shipyard_symbol in shipyard_symbols:
    # -----------------------------
    # Fetch current waypoint and status for the ship
    # -----------------------------
    cur.execute(
        "SELECT waypointSymbol, status FROM fleet_nav WHERE ship_symbol = ?",
        (ship_symbol,),
    )
    row = cur.fetchone()
    if not row:
        print(f"[WARNING] No fleet_nav entry for {ship_symbol}, skipping")
        continue

    current_wp = row["waypointSymbol"]
    status = row["status"]
    print(
        f"[INFO] Current waypoint for {ship_symbol} is {current_wp} (status: {status})"
    )

    # -----------------------------
    # Skip navigation if already at this waypoint
    # -----------------------------
    if current_wp == shipyard_symbol:
        print(
            f"[INFO] Ship {ship_symbol} already at {shipyard_symbol}, skipping navigation"
        )
    else:
        # -----------------------------
        # Navigate ship
        # -----------------------------
        print(
            f"[DEBUG] Attempting to navigate {ship_symbol} from {current_wp} → {shipyard_symbol}"
        )
        nav_resp = client.navigate_ship(ship_symbol, shipyard_symbol)

        # Parse route timestamps
        route = nav_resp["data"]["nav"]["route"]
        dep_dt = datetime.fromisoformat(route["departureTime"].replace("Z", "+00:00"))
        arr_dt = datetime.fromisoformat(route["arrival"].replace("Z", "+00:00"))
        travel_seconds = (arr_dt - dep_dt).total_seconds()
        print(f"[INFO] Travel time: {travel_seconds:.1f} seconds")
        time.sleep(travel_seconds + 1)

        # -----------------------------
        # Refresh shipyard_ships for this waypoint
        # -----------------------------
        print(f"[INFO] Fetching shipyard_ships for {shipyard_symbol}")
        normalize_shipyard_ships(conn, client.list_shipyard_ships(shipyard_symbol))
        print(f"[INFO] Refreshed shipyard_ships for {shipyard_symbol}")

conn.close()
print("[INFO] Startup orchestration complete.")
