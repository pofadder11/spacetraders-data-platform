# runner snippet
from rich import print as rprint
from rich.pretty import Pretty

from services.api_groups import systems, agents, fleet

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

me = agents.get_my_agent()  # directly returns the inner `.data`
hq = me.headquarters
pretty(hq)
system_symbol = "-".join(hq.split("-")[:2])

sys_obj = systems.get_system(system_symbol)           # returns data
wps = systems.get_system_waypoints(system_symbol)
     # returns list-like data

ships = fleet.get_my_ships()                          # returns data
pretty(ships)
print(ships)
pretty(wps)