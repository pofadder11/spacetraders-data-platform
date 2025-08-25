# test .json normalization and .db populating

from api.client import SpaceTradersClient
from api.normalizer import init_db  # adjust import path as needed
from api.normalizer import normalize_waypoints

# Setup
client = SpaceTradersClient()
conn = init_db("spacetraders.db")

# Fetch waypoints for current system
system_symbol = client.system_symbol  # the global you already set up
waypoints_json = client.list_waypoints(system_symbol)

# Normalize into DB
normalize_waypoints(conn, waypoints_json["data"])
