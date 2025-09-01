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
print("me :",me)
pretty(me.data.headquarters)


#contracts_list = contracts.get_contracts()
#print("contracts_list :",contracts_list)

systems_list = systems.get_systems()
systems_coords = [(s.symbol, s.x, s.y) for s in systems_list.data]
pretty(systems_coords)

#shipyard_list = systems.get_shipyard()
#print("shipyard_list :",shipyard_list)

