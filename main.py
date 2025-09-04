import os
from rich import print as rprint
from rich.pretty import Pretty

from dotenv import load_dotenv

import openapi_client
from openapi_client.rest import ApiException

load_dotenv()

def pretty(obj):
    """
    Recursively pretty-print any object with color.
    Works with Pydantic/OpenAPI models, dicts, lists, etc.
    """
    # Convert Pydantic/OpenAPI model to dict if possible
    try:
        data = obj.dict(by_alias=True, exclude_none=True)
    except AttributeError:
        data = obj
    rprint(Pretty(data))

configuration = openapi_client.Configuration(access_token=os.getenv("BEARER_TOKEN"))
apicl = openapi_client.ApiClient(configuration)
agents = openapi_client.AgentsApi(apicl)
contracts = openapi_client.ContractsApi(apicl)
systems = openapi_client.SystemsApi(apicl)
fleet = openapi_client.FleetApi(apicl)


me = agents.get_my_agent()
#print("me :",me)
#pretty(me.data.headquarters)

my_system = '-'.join(me.data.headquarters.split('-')[:2])
print("My system :", my_system)

waypoints_list = systems.get_system_waypoints(my_system)
shipyards_list = systems.get_system_waypoints(my_system, traits ="SHIPYARD")
shipyards_waypoints = [(sl.symbol, sl.x, sl.y) for sl in shipyards_list.data]
print("Shipyard waypoints: ")
pretty(shipyards_waypoints)

my_ships = fleet.get_my_ships()
ship_types = [(st.symbol, st.frame.symbol, st.nav.status) for st in my_ships.data]
print("My ships: ")
pretty(ship_types)

#pretty([(w.symbol, w.traits) for w in waypoints_list.data])

marketplace_waypoints = [
    w.symbol
    for w in waypoints_list.data
    if any(t.name == "Marketplace" for t in w.traits)
]
"""
print("Waypoints with Marketplace trait: ")
pretty(marketplace_waypoints)

async def main():
    my_system = '-'.join(me.data.headquarters.split('-')[:2])
    
    # Get your ship symbols
    probe_ship = "PROBE-001"
    frigate_ship = "FRIGATE-001"
    
    await asyncio.gather(
        probe_gather_market_data(probe_ship, my_system),
        frigate_buy_mining_drones(frigate_ship, my_system)
    )

# Run the async loop
asyncio.run(main())
"""


