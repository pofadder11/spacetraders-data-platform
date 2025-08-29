# run_startup.py
import sqlite3
import time

from api.client import SpaceTradersClient
from api.db.init_db import init_db
from api.db.pipeline import SpaceTradersDataManager

# -----------------------------
# Setup
# -----------------------------
conn = init_db("spacetraders.db")
client = SpaceTradersClient()
# -----------------------------
conn = sqlite3.connect("spacetraders.db")
cur = conn.cursor()
etl = SpaceTradersDataManager(client, conn)
# etl.store_fleet()
etl.store_contracts()
time.sleep(5)
etl.store_contracts()
time.sleep(5)
etl.store_contracts()
time.sleep(5)
etl.store_fleet()
time.sleep(5)
etl.store_fleet()
time.sleep(5)


# from config import DB_PATH

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

# print("Ships:", client.list_ships())
# normalize_fleet(sqlite3.connect("spacetraders.db"), client.list_ships())


# client.dock_ship("JANKNESS-1")
"""
print("Dock: ", client.dock_ship("JANKNESS-1"))
print("Refuel: ", client.refuel_ship("JANKNESS-1"))
print("Orbit: ", client.orbit_ship("JANKNESS-1"))
nav_wayp = client.navigate_ship("JANKNESS-1", "X1-GN67-A2")
print("Navigation result:", nav_wayp)
"""
# print("Shipyard ships", client.list_shipyard_ships("X1-GN67-A2"))
# print("Shipyards :", client.list_shipyards())
# conn = sqlite3.connect("spacetraders.db")

# normalize_fleet(conn, client.list_ships())
# normalize_shipyards(conn, client.list_shipyards())
# normalize_waypoints(conn, client.list_waypoints(client.system_symbol))
# normalize_shipyard_ships(conn, client.list_shipyard_ships("X1-NM89-C44"))


# print("Ships:", client.list_ships())
