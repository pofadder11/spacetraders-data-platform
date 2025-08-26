import sqlite3
import time
from datetime import datetime

from api.client import SpaceTradersClient
from api.db.init_db import init_db
from api.normalizer import normalize_fleet, normalize_shipyards, normalize_waypoints

# -----------------------------
# Setup client & DB
# -----------------------------
client = SpaceTradersClient()
conn = init_db("spacetraders.db")
cur = conn.cursor()

# -----------------------------
# ETL: Refresh tables
# -----------------------------
system_symbol = client.system_symbol

# Waypoints
waypoints_json = client.list_waypoints(system_symbol)
normalize_waypoints(conn, waypoints_json["data"])

# Shipyards
shipyards_json = client.list_shipyards(system_symbol)
shipyards_rows = normalize_shipyards(shipyards_json)

# Fleet
fleet_json = client.list_ships()
normalize_fleet(conn, fleet_json["data"])

# -----------------------------
# Select fastest ship (any status, any fuel)
# -----------------------------
cur.execute(
    """
    SELECT fs.ship_symbol, fs.engine_speed
    FROM fleet_specs fs
    ORDER BY fs.engine_speed DESC
    LIMIT 1
"""
)
row = cur.fetchone()
if not row:
    raise RuntimeError("No ships found in fleet_specs")

ship_symbol = row[0]
print(f"[INFO] Selected ship {ship_symbol} with highest speed {row[1]}")


# -----------------------------
# Prepare ship for navigation
# -----------------------------
def prepare_ship_for_navigation(client: SpaceTradersClient, ship_symbol: str) -> None:
    """
    Ensure a ship is ready for navigation:
    - If not IN_ORBIT, orbit it.
    - If fuel_current < fuel_capacity, refuel it.
    """
    conn = sqlite3.connect("spacetraders.db")
    cur = conn.cursor()
    cur.execute(
        """
        SELECT fn.status, fn.fuel_current, fn.fuel_capacity
        FROM fleet_nav fn
        WHERE fn.ship_symbol = ?
    """,
        (ship_symbol,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise RuntimeError(f"No fleet_nav entry found for ship {ship_symbol}")

    status, fuel_current, fuel_capacity = row

    # Orbit if necessary
    if status != "IN_ORBIT":
        print(f"[INFO] Ship {ship_symbol} is {status}, sending to orbit...")
        resp = client.orbit_ship(ship_symbol)
        print(f"[INFO] Orbit response: {resp}")

    # Refuel if necessary
    if fuel_current < fuel_capacity:
        print(
            f"[INFO] Ship {ship_symbol} fuel {fuel_current}/{fuel_capacity}, refueling..."
        )
        resp = client.refuel_ship(ship_symbol)
        print(f"[INFO] Refuel response: {resp}")


prepare_ship_for_navigation(client, ship_symbol)

# -----------------------------
# Fetch shipyards to navigate
# -----------------------------
cur.execute("SELECT waypoint_symbol FROM shipyards LIMIT 3")
shipyard_waypoints = [r[0] for r in cur.fetchall()]

# -----------------------------
# Navigate sequentially
# -----------------------------
for waypoint in shipyard_waypoints:
    print(f"[INFO] Navigating {ship_symbol} to {waypoint}")
    nav_resp = client.navigate_ship(ship_symbol, waypoint)

    # -----------------------------
    # Calculate travel time from route timestamps
    # -----------------------------
    route_info = nav_resp["data"]["nav"]["route"]
    print("Route info: ", route_info["departureTime"])
    departure_ts = route_info["departureTime"]
    arrival_ts = route_info["arrival"]
    # Parse strings into datetime objects
    departure_dt = datetime.fromisoformat(departure_ts.replace("Z", "+00:00"))
    arrival_dt = datetime.fromisoformat(arrival_ts.replace("Z", "+00:00"))
    # Compute travel seconds
    travel_seconds = (arrival_dt - departure_dt).total_seconds()
    print(f"[INFO] Travel time: {travel_seconds} seconds")

    # -----------------------------
    # Wait until arrival
    # -----------------------------
    print(f"[INFO] Waiting for ship to arrive at {waypoint}...")
    time.sleep(travel_seconds + 1)  # small buffer to ensure arrival

    # -----------------------------
    # Refresh shipyard_ships for this waypoint
    # -----------------------------
    cur.execute(
        "SELECT shipyard_symbol FROM shipyards WHERE waypoint_symbol = ?", (waypoint,)
    )
shipyard_row = cur.fetchone()
if shipyard_row:
    full_shipyard_symbol = shipyard_row[0]

    # Extract last two segments after first dash
    parts = full_shipyard_symbol.split("-", 1)
    api_shipyard_symbol = parts[1] if len(parts) > 1 else full_shipyard_symbol

    ships_json = client.list_shipyard_ships(api_shipyard_symbol)

    # Assuming you have a normalize_shipyard_ships function
    normalize_shipyards(conn, ships_json)
    print(
        f"[INFO] Refreshed shipyard_ships for {full_shipyard_symbol} (API symbol: {api_shipyard_symbol})"
    )

conn.close()
print("[INFO] Startup orchestration complete.")
