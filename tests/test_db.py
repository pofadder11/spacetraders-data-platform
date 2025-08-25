# test .json normalization and .db populating

from api.client import SpaceTradersClient
from api.normalizer import init_db  # include normalize_shipyards
from api.normalizer import normalize_shipyards, normalize_waypoints

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
cur = conn.cursor()
for sy in shipyards_rows:
    cur.execute(
        """
        INSERT OR REPLACE INTO shipyards
        (shipyard_symbol, waypoint_symbol, system_symbol,
        is_under_construction, faction_symbol)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            sy["shipyard_symbol"],
            sy["waypoint_symbol"],
            sy["system_symbol"],
            sy["is_under_construction"],
            sy["faction_symbol"],
        ),
    )
conn.commit()
for sy in shipyards_rows:
    cur.execute(
        """
        INSERT OR REPLACE INTO traits (waypoint_symbol, trait_symbol)
        VALUES (?, ?)
        """,
        (sy["waypoint_symbol"], "SHIPYARD"),
    )
