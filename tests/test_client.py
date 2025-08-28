import sqlite3

from api.client import SpaceTradersClient
from api.normalizer import normalize_fleet

# Initialize the client

client = SpaceTradersClient()

# negotiate = client.negotiate_contract("JANKNESS-1")
# print("Negotiable contracts:", negotiate)

# contracts = client.list_contracts()
# contract_id = contracts['data'][0]['id']
# print("First contract ID:", contract_id)
# print("Contracts:", contracts)

# client.accept_contract("cmesgtjlkgjzjuo6yu3cjefqh")

# shipyards = client.list_shipyards()
# print("Shipyards:", shipyards)

# waypoints = client.list_waypoints(client.system_symbol)
# print("Waypoints:", waypoints)

# print("Ships:", client.list_ships())


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
conn = sqlite3.connect("spacetraders.db")

normalize_fleet(conn, client.list_ships())
# normalize_shipyards(conn, client.list_shipyards())
# normalize_waypoints(conn, client.list_waypoints(client.system_symbol))
# normalize_shipyard_ships(conn, client.list_shipyard_ships("X1-NM89-C44"))


# print("Ships:", client.list_ships())
