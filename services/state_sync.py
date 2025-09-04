"""In-memory runner state sync handlers for WriteThrough.

These handlers update the lightweight `state` cache from API responses so the
runner has a fresh working view without DB reads.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from services.write_through import Handler
import state


def _ship_symbol_from(args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> str | None:
    return args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol")


def state_handlers() -> Dict[str, Handler]:
    def handle_get_my_ships(_session, ships, *_):
        if ships:
            state.update_from_ships(ships)

    def handle_navigate_or_patch(_session, data, args, kwargs, *_):
        ship_symbol = _ship_symbol_from(args, kwargs)
        if ship_symbol:
            nav = getattr(data, "nav", None)
            fuel = getattr(data, "fuel", None)
            state.update_from_nav(ship_symbol, nav, fuel)

    def handle_get_ship_nav(_session, nav, args, kwargs, *_):
        ship_symbol = _ship_symbol_from(args, kwargs)
        if ship_symbol:
            state.update_from_nav(ship_symbol, nav)

    def handle_orbit_or_dock(_session, data, args, kwargs, *_):
        ship_symbol = _ship_symbol_from(args, kwargs)
        if ship_symbol:
            nav = getattr(data, "nav", None)
            state.update_from_nav(ship_symbol, nav)

    def handle_refuel(_session, data, args, kwargs, *_):
        ship_symbol = _ship_symbol_from(args, kwargs)
        if ship_symbol:
            fuel = getattr(data, "fuel", None)
            state.update_from_nav(ship_symbol, None, fuel)

    return {
        # list ships
        "fleet.get_my_ships": handle_get_my_ships,
        "FleetApi.get_my_ships": handle_get_my_ships,
        # nav changes
        "fleet.navigate_ship": handle_navigate_or_patch,
        "FleetApi.navigate_ship": handle_navigate_or_patch,
        "fleet.patch_ship_nav": handle_navigate_or_patch,
        "FleetApi.patch_ship_nav": handle_navigate_or_patch,
        "fleet.get_ship_nav": handle_get_ship_nav,
        "FleetApi.get_ship_nav": handle_get_ship_nav,
        # orbit/dock
        "fleet.orbit_ship": handle_orbit_or_dock,
        "FleetApi.orbit_ship": handle_orbit_or_dock,
        "fleet.dock_ship": handle_orbit_or_dock,
        "FleetApi.dock_ship": handle_orbit_or_dock,
        # fuel changes
        "fleet.refuel_ship": handle_refuel,
        "FleetApi.refuel_ship": handle_refuel,
        # resource gathering updates cargo units
        "fleet.extract_resources": lambda _s, data, args, kwargs, *_: (
            state.update_from_cargo(_ship_symbol_from(args, kwargs), getattr(data, "cargo", None))
        ),
        "FleetApi.extract_resources": lambda _s, data, args, kwargs, *_: (
            state.update_from_cargo(_ship_symbol_from(args, kwargs), getattr(data, "cargo", None))
        ),
        "fleet.siphon_resources": lambda _s, data, args, kwargs, *_: (
            state.update_from_cargo(_ship_symbol_from(args, kwargs), getattr(data, "cargo", None))
        ),
        "FleetApi.siphon_resources": lambda _s, data, args, kwargs, *_: (
            state.update_from_cargo(_ship_symbol_from(args, kwargs), getattr(data, "cargo", None))
        ),
    }
