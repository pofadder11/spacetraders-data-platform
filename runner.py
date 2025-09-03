"""Example runner script focused on decision logic.

The goal of the runner is to orchestrate game play while delegating
persistence to :mod:`etl` and concrete API calls to :mod:`actions`.
It performs a very small set of decisions just to demonstrate the
pattern: fetch the agent's ships, update local state, and ensure each
ship is in orbit.

This file intentionally avoids embedding business rules beyond that
minimal example; real strategies should live in separate modules.
"""

from __future__ import annotations

from dotenv import load_dotenv

import actions
import etl
from services.client_service import OpenAPIService


load_dotenv()


def run() -> None:
    """Run a minimal decision loop.

    - Retrieve the player's ships using :func:`actions.list_ships`
    - Normalise and store each ship's state via :func:`etl.update_from_api`
    - If a ship is not already in orbit, call :func:`actions.orbit`
    """

    svc = OpenAPIService()
    ships = actions.list_ships(svc)
    for ship in ships:
        state = etl.update_from_api(ship)
        if state.nav_status != "IN_ORBIT":
            actions.orbit(svc, state.symbol)


if __name__ == "__main__":
    run()
