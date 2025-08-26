from api.client import SpaceTradersClient

# Initialize the client

client = SpaceTradersClient()

# negotiate = client.negotiate_contract("JANKNESS-1")
# print("Negotiable contracts:", negotiate)

contracts = client.list_contracts()
# contract_id = contracts['data'][0]['id']
# print("First contract ID:", contract_id)
# print("Contracts:", contracts)

client.accept_contract("cmesgtjlkgjzjuo6yu3cjefqh")

# shipyards = client.list_shipyards()
# print("Shipyards:", shipyards)

# waypoints = client.list_waypoints(client.system_symbol)
# print("Waypoints:", waypoints)

# ships= client.list_ships()
# print("Ships:", ships)

# client.dock_ship("JANKNESS-1")
