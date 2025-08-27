# run_startup.py
import time
from datetime import datetime

from api.client import SpaceTradersClient
from api.db.init_db import init_db
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
conn = init_db("spacetraders.db")
cur = conn.cursor()

# -----------------------------
# ETL: Full refresh
# -----------------------------
system_symbol = client.system_symbol
normalize_waypoints(conn, client.list_waypoints(system_symbol))

shipyards_json = client.list_shipyards(system_symbol)
normalize_shipyards(conn, shipyards_json)

fleet_json = client.list_ships()
normalize_fleet(conn, fleet_json)


# -----------------------------
# Helper: Prepare ship for navigation
# -----------------------------
def prepare_ship_for_navigation(ship_symbol: str):
    cur.execute(
        """
        SELECT status, fuel_current, fuel_capacity
        FROM fleet_nav
        WHERE ship_symbol = ?
        """,
        (ship_symbol,),
    )
    row = cur.fetchone()
    if not row:
        raise RuntimeError(f"No fleet_nav entry for ship {ship_symbol}")

    status, fuel_current, fuel_capacity = row

    if status != "DOCKED":
        print(f"[INFO] Docking {ship_symbol} (status: {status})")
        client.dock_ship(ship_symbol)

    if fuel_current < fuel_capacity:
        print(f"[INFO] Refueling {ship_symbol} ({fuel_current}/{fuel_capacity})")
        client.refuel_ship(ship_symbol)

    if status != "IN_ORBIT":
        print(f"[INFO] Orbiting {ship_symbol} (status: {status})")
        client.orbit_ship(ship_symbol)


# -----------------------------
# Select fastest available ship
# -----------------------------
cur.execute(
    """
    SELECT fs.ship_symbol
    FROM fleet_specs fs
    JOIN fleet_nav fn ON fs.ship_symbol = fn.ship_symbol
    WHERE fn.status IN ('IN_ORBIT', 'DOCKED') AND fn.fuel_current > 0
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
# Fetch shipyard waypoints (limit 3)
# -----------------------------
cur.execute("SELECT waypoint_symbol, shipyard_symbol FROM shipyards LIMIT 3")
shipyard_rows = cur.fetchall()

for waypoint_symbol, full_shipyard_symbol in shipyard_rows:

    # -----------------------------
    # Skip navigation if already at this waypoint
    # -----------------------------
    cur.execute(
        "SELECT waypoint_symbol FROM fleet_nav WHERE ship_symbol = ?",
        (ship_symbol,),
    )
    current_wp = cur.fetchone()[0]
    if current_wp == waypoint_symbol:
        print(
            f"[INFO] Ship {ship_symbol} already at {waypoint_symbol}, skipping navigation"
        )
    else:
        print(f"[INFO] Navigating {ship_symbol} to {waypoint_symbol}")
        nav_resp = client.navigate_ship(ship_symbol, waypoint_symbol)

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
    api_shipyard_symbol = (
        full_shipyard_symbol.split("-", 1)[1]
        if "-" in full_shipyard_symbol
        else full_shipyard_symbol
    )
    ships_json = client.list_shipyard_ships(system_symbol, api_shipyard_symbol)
    normalize_shipyard_ships(conn, ships_json, full_shipyard_symbol)
    print(f"[INFO] Refreshed shipyard_ships for {full_shipyard_symbol}")

conn.close()
print("[INFO] Startup orchestration complete.")
