# test .json normalization and .db populating

from api.client import SpaceTradersClient
from api.db.init_db import init_db  # include normalize_shipyards
from api.normalizer import normalize_fleet, normalize_shipyards, normalize_waypoints

# -----------------------------
# Setup
# -----------------------------
client = SpaceTradersClient()
conn = init_db("spacetraders.db")

# -----------------------------
# Fetch waypoints for current system
# -----------------------------
system_symbol = client.system_symbol  # the global you already set up
waypoints_json = client.list_waypoints(system_symbol)

# -----------------------------
# Normalize into DB
# -----------------------------
normalize_waypoints(conn, waypoints_json["data"])

# -----------------------------
# Fetch shipyards for current system
# -----------------------------
shipyards_json = client.list_shipyards(system_symbol)

# -----------------------------
# Normalize shipyards
# -----------------------------
shipyards_rows = normalize_shipyards(shipyards_json)

# -----------------------------
# Fetch fleet
# -----------------------------
fleet_json = client.list_ships()

# -----------------------------
# Normalize fleet into DB
# -----------------------------
normalize_fleet(conn, fleet_json["data"])
