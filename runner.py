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


load_dotenv()


def run() -> None:
    """Run a minimal decision loop.

    - Retrieve the player's ships using :func:`services.actions.list_ships`
    - Normalise and store each ship's state via :func:`state.update_from_api`
    - If a ship is not already in orbit, call :func:`services.actions.orbit`
    """

    # Ensure database schema exists for write-through updates
    init_db()
    ships = act.list_ships()
    for ship in ships:
        s = state.update_from_api(ship)
        if s.nav_status != "IN_ORBIT":
            act.orbit(s.symbol)


if __name__ == "__main__":
    run()
