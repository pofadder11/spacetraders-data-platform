from api.client import SpaceTradersClient

# Initialize the client

client = SpaceTradersClient()

# contracts = client.list_contracts()
# print("Contracts:", contracts)

shipyards = client.list_shipyards()
print("Shipyards:", shipyards)

# waypoints = client.list_waypoints(client.system_symbol)
# print("Waypoints:", waypoints)

# ships= client.list_ships()
# print("Ships:", ships)
