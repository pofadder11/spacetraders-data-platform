"""Example runner script focused on decision logic.

The goal of the runner is to orchestrate game play while delegating
persistence to :mod:`state` and concrete API calls to :mod:`services.actions`.
It performs a very small set of decisions just to demonstrate the
pattern: fetch the agent's ships, update local state, and ensure each
ship is in orbit.

This file intentionally avoids embedding business rules beyond that
minimal example; real strategies should live in separate modules.
"""

from __future__ import annotations

from dotenv import load_dotenv

from services import actions as act
import state
from session import init_db

from rich import print as rprint
from rich.pretty import Pretty

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

list_ships = act.list_ships()
#rprint("List of ships: ", Pretty(list_ships))

#returns system_symbol, waypoint_symbol and route(=ShipNavRoute)
rprint("List of ships[0].nav: ", Pretty(list_ships[0].nav))

#returns
# destination: symbol, type, system_symbol, x, y
# origin: symbol, type, system_symbol, x, y
# departure time
# arrival
# good for DB route storage
rprint("List of ships[0].nav.route: ", Pretty(list_ships[0].nav.route))

"""
# returns cargo attributes: capacity, units and inventory[]
# good for transport and resource extraction logic calls
rprint("List of ships[0].cargo: ", Pretty(list_ships[0].cargo))

# returns fuel attributes: current, capacity and consumed
# good for route planning and fuel budgets
rprint("List of ships[0].fuel: ", Pretty(list_ships[0].fuel))

# returns fuel.consumed attributes: amount, timestamp (??not sure what the timestamp means,TODO: investigate fuel.consumption timestamp)
# good for route planning and fuel budgets
rprint("List of ships[0].fuel.consumed: ", Pretty(list_ships[0].fuel.consumed))

# returns ship_symbol, total_seconds, remaining_seconds and expiration
# good for quick access to async wait time for navigation logic if ship is IN_TRANSIT
rprint("List of ships[0].cooldown: ", Pretty(list_ships[0].cooldown))

# returns list of ShipMount, each with attributes: symbol, name, description, strength, deposits, requirements(=ShipRequirements(power, crew, slots))
# good for selecting outward-facing tools like probes, lasers and siphons
rprint("List of ships[0].mounts: ", Pretty(list_ships[0].mounts))

# returns list of ShipModules, each with attributes: symbol, name, description, strength, deposits, requirements(=ShipRequirements(power, crew, slots))
# good for selecting inward-facing tools like storage, processing etc.
rprint("List of ships[0].modules: ", Pretty(list_ships[0].modules))

# returns ShipFrame: symbol, name, condition, integrity, decsription, module_slots, mounting_points, fuel_capacity, requirements(=ShipRequirements(power, crew, slots)), quality
# good for DB display of fleet composition and capacities (modules, mounts, fuel etc.)
rprint("List of ships[0].frame: ", Pretty(list_ships[0].frame))

# returns list of ShipCrew: current, required, capacity, rotation, morale, wages)
rprint("List of ships[0].crew: ", Pretty(list_ships[0].crew))

"""

def run() -> None:
    """Run a minimal decision loop.

    - Retrieve the player's ships using :func:`services.actions.list_ships`
    - Normalise and store each ship's state via :func:`state.update_from_api`
    - If a ship is not already in orbit, call :func:`services.actions.orbit`
    """

    # Ensure database schema exists for write-through updates
    init_db()
    ships = act.list_ships()
    for s in ships:
        if getattr(getattr(ship, "nav", None), "status", None) != "IN_ORBIT":
            act.orbit(ship.symbol)


if __name__ == "__main__":
    run()
