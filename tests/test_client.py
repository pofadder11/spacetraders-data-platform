"""# run_startup.py

import sqlite3

import pandas as pd

from api.client import SpaceTradersClient
from api.db.pipeline import SpaceTradersDataManager

client = SpaceTradersClient()
# -----------------------------
# Setup
# -----------------------------


# -----------------------------
conn = sqlite3.connect("spacetraders.db")
cur = conn.cursor()
etl = SpaceTradersDataManager(client, conn)

client.supply_chain()


import sqlite3

from api.client import SpaceTradersClient
from api.db.pipeline import SpaceTradersDataManager

client = SpaceTradersClient()
conn = sqlite3.connect("spacetraders.db")

cargo = pd.read_sql_query(
    "SELECT symbol, units from fleet_cargo_inventory WHERE ship_symbol IS 'FLAT_SHIP-1'",
    conn,
)

# etl = SpaceTradersDataManager(client, conn)
# etl.fleet()

for row in cargo.itertuples(index=False):
    client.jettison("FLAT_SHIP-6", row.symbol, row.units)

# etl.journey("FLAT_SHIP-1", "X1-AP86-B6")
# etl.fleet()
"""

"""
client.refuel_ship("FLAT_SHIP-1")
client.orbit_ship("FLAT_SHIP-1")

# from config import DB_PATH
"""

# negotiate = client.negotiate_contract("JANKNESS-1")
# print("Negotiable contracts:", negotiate)
# accept_contract = client.accept_contract(client.list_contracts()["data"]["id"])
# conn = sqlite3.connect("spacetraders.db")
# normalize_contracts(conn, contracts)
# contract_id = contracts['data'][0]['id']
# print("First contract ID:", contract_id)
# print("Contracts:", contracts)

# client.accept_contract("cmesgtjlkgjzjuo6yu3cjefqh")

# shipyards = client.list_shipyards()
# print("Shipyards:", shipyards)

# waypoints = client.list_waypoints(client.system_symbol)
# print("Waypoints:", waypoints)
"""
etl.fleet()
client.dock_ship("FLAT_SHIP-1")
etl.fleet()

client.refuel_ship("FLAT_SHIP-1")
client.orbit_ship("FLAT_SHIP-1")
etl.fleet()
etl.journey("FLAT_SHIP-1", "X1-AP86-B7")
etl.fleet()
"""
# client.get_market("X1-AP86-B7")

# client.dock_ship("FLAT_SHIP-1")
# client.negotiate_contract("FLAT_SHIP-1")
# print("Ships:", client.list_ships())
# normalize_fleet(sqlite3.connect("spacetraders.db"), client.list_ships())


"""
# client.dock_ship("JANKNESS-1")
print("Dock: ", client.dock_ship("JANKNESS-1"))
print("Refuel: ", client.refuel_ship("JANKNESS-1"))
print("Orbit: ", client.orbit_ship("JANKNESS-1"))
nav_wayp = client.navigate_ship("JANKNESS-1", "X1-GN67-A2")
print("Navigation result:", nav_wayp)
"""
"""
# print("Shipyard ships", client.list_shipyard_ships("X1-GN67-A2"))
# print("Shipyards :", client.list_shipyards())
# conn = sqlite3.connect("spacetraders.db")

# normalize_fleet(conn, client.list_ships())
# normalize_shipyards(conn, client.list_shipyards())
# normalize_waypoints(conn, client.list_waypoints(client.system_symbol))
# normalize_shipyard_ships(conn, client.list_shipyard_ships("X1-NM89-C44"))


# print("Ships:", client.list_ships())
"""
