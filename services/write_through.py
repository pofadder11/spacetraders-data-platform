# services/write_through.py
from __future__ import annotations

from typing import Any, Callable, Dict, Tuple

from sqlalchemy.orm import Session

from services.client_service import OpenAPIService

# Handler signature: Session, result (.data), args, kwargs, api_name, method_name
Handler = Callable[[Session, Any, Tuple[Any, ...], Dict[str, Any], str, str], None]


from services.normalizer import upsert_fleet_nav as _upsert_nav
from services.normalizer import upsert_market_trade_goods as _upsert_market
from services.normalizer import upsert_market_trade_goods_current as _upsert_market_current
from services.normalizer import upsert_fleet_nav_from_nav as _upsert_nav_from_nav
from services.normalizer import (
    upsert_ship_current_from_nav_fuel as _upsert_ship_current_from_nav_fuel,
    upsert_ship_current_from_nav as _upsert_ship_current_from_nav,
    upsert_ships_current as _upsert_ships_current,
    upsert_system_row as _upsert_system_row,
    upsert_waypoints_from_list as _upsert_waypoints_from_list,
    upsert_fleet_nav_from_ship as _upsert_fleet_nav_from_ship,
    update_ship_current_cargo_units as _update_ship_current_cargo_units,
    upsert_ship_cargo_current as _upsert_ship_cargo_current,
    insert_extraction_yield as _insert_extraction_yield,
)

# Write-through relies on your dedicated normalizer


def default_handlers() -> Dict[str, Handler]:
    """
    Registry keys use either snake alias ('fleet') or class name ('FleetApi'),
    plus method name, e.g. 'fleet.get_my_ships'.
    """
    def handle_get_my_ships(session: Session, data: Any, *ctx) -> None:
        _upsert_nav(session, data)
        _upsert_ships_current(session, data)

    def handle_get_market(session: Session, market: Any, *ctx) -> None:
        _upsert_market(session, market)
        _upsert_market_current(session, market)

    def handle_navigate_ship(session: Session, navdata: Any, args, kwargs, api_name, method_name) -> None:
        # args[0] expected to be ship_symbol per FleetApi signature
        ship_symbol = args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol")
        nav = getattr(navdata, "nav", None)
        fuel = getattr(navdata, "fuel", None)
        if ship_symbol and nav is not None:
            _upsert_nav_from_nav(session, ship_symbol, nav)
            _upsert_ship_current_from_nav_fuel(session, ship_symbol, nav=nav, fuel=fuel)

    def handle_get_ship_nav(session: Session, nav: Any, args, kwargs, api_name, method_name) -> None:
        ship_symbol = args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol")
        if ship_symbol and nav is not None:
            _upsert_nav_from_nav(session, ship_symbol, nav)
            _upsert_ship_current_from_nav(session, ship_symbol, nav)

    def handle_refuel_ship(session: Session, data: Any, args, kwargs, api_name, method_name) -> None:
        ship_symbol = args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol")
        fuel = getattr(data, "fuel", None)
        if ship_symbol and fuel is not None:
            _upsert_ship_current_from_nav_fuel(session, ship_symbol, nav=None, fuel=fuel)

    def handle_purchase_ship(session: Session, data: Any, args, kwargs, api_name, method_name) -> None:
        ship = getattr(data, "ship", None)
        if ship is not None:
            _upsert_ships_current(session, [ship])
            _upsert_fleet_nav_from_ship(session, ship)

    def handle_extract_resources(session: Session, data: Any, args, kwargs, api_name, method_name) -> None:
        ship_symbol = args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol")
        extraction = getattr(data, "extraction", None)
        cooldown = getattr(data, "cooldown", None)
        cargo = getattr(data, "cargo", None)
        if extraction is not None:
            ex_yield = getattr(extraction, "var_yield", None)
            if ex_yield is not None:
                _insert_extraction_yield(
                    session,
                    ship_symbol,
                    getattr(ex_yield, "symbol", None),
                    getattr(ex_yield, "units", None) or 0,
                    cooldown,
                )
        if cargo is not None:
            _update_ship_current_cargo_units(session, ship_symbol, getattr(cargo, "units", None))
            _upsert_ship_cargo_current(session, ship_symbol, cargo)

    def handle_siphon_resources(session: Session, data: Any, args, kwargs, api_name, method_name) -> None:
        ship_symbol = args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol")
        siphon = getattr(data, "siphon", None)
        cooldown = getattr(data, "cooldown", None)
        cargo = getattr(data, "cargo", None)
        if siphon is not None:
            sy = getattr(siphon, "var_yield", None)
            if sy is not None:
                _insert_extraction_yield(
                    session,
                    ship_symbol,
                    getattr(sy, "symbol", None),
                    getattr(sy, "units", None) or 0,
                    cooldown,
                )
        if cargo is not None:
            _update_ship_current_cargo_units(session, ship_symbol, getattr(cargo, "units", None))
            _upsert_ship_cargo_current(session, ship_symbol, cargo)

    def handle_get_system(session: Session, system: Any, *ctx) -> None:
        if system is not None:
            _upsert_system_row(session, system)

    def handle_get_system_waypoints(session: Session, waypoints: Any, *ctx) -> None:
        if waypoints:
            _upsert_waypoints_from_list(session, waypoints)

    return {
        "fleet.get_my_ships": handle_get_my_ships,
        "FleetApi.get_my_ships": handle_get_my_ships,
        # market fetch -> snapshot + current
        "systems.get_market": handle_get_market,
        "SystemsApi.get_market": handle_get_market,
        # navigate -> update FleetNav row
        "fleet.navigate_ship": handle_navigate_ship,
        "FleetApi.navigate_ship": handle_navigate_ship,
        # patch nav behaves like navigate (returns nav + fuel)
        "fleet.patch_ship_nav": handle_navigate_ship,
        "FleetApi.patch_ship_nav": handle_navigate_ship,
        # get nav returns ShipNav only
        "fleet.get_ship_nav": handle_get_ship_nav,
        "FleetApi.get_ship_nav": handle_get_ship_nav,
        # docking/orbit return nav only
        "fleet.dock_ship": lambda session, data, args, kwargs, *_: (
            _upsert_nav_from_nav(session, args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol"), getattr(data, "nav", None)),
            _upsert_ship_current_from_nav(session, args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol"), getattr(data, "nav", None))
        ),
        "FleetApi.dock_ship": lambda session, data, args, kwargs, *_: (
            _upsert_nav_from_nav(session, args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol"), getattr(data, "nav", None)),
            _upsert_ship_current_from_nav(session, args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol"), getattr(data, "nav", None))
        ),
        "fleet.orbit_ship": lambda session, data, args, kwargs, *_: (
            _upsert_nav_from_nav(session, args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol"), getattr(data, "nav", None)),
            _upsert_ship_current_from_nav(session, args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol"), getattr(data, "nav", None))
        ),
        "FleetApi.orbit_ship": lambda session, data, args, kwargs, *_: (
            _upsert_nav_from_nav(session, args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol"), getattr(data, "nav", None)),
            _upsert_ship_current_from_nav(session, args[0] if args else kwargs.get("ship_symbol") or kwargs.get("shipSymbol"), getattr(data, "nav", None))
        ),
        # refuel updates fuel state
        "fleet.refuel_ship": handle_refuel_ship,
        "FleetApi.refuel_ship": handle_refuel_ship,
        # purchase ship -> update ships_current and fleet_nav
        "fleet.purchase_ship": handle_purchase_ship,
        "FleetApi.purchase_ship": handle_purchase_ship,
        # systems and waypoints persistence
        "systems.get_system": handle_get_system,
        "SystemsApi.get_system": handle_get_system,
        "systems.get_system_waypoints": handle_get_system_waypoints,
        "SystemsApi.get_system_waypoints": handle_get_system_waypoints,
        # resource gathering
        "fleet.extract_resources": handle_extract_resources,
        "FleetApi.extract_resources": handle_extract_resources,
        "fleet.siphon_resources": handle_siphon_resources,
        "FleetApi.siphon_resources": handle_siphon_resources,
    }


class _ApiDataProxyWT:
    """
    Per-API proxy. Any method call returns `.data` (via the service's data-proxy),
    then applies a write-through handler if registered.
    """
    def __init__(
        self,
        api_obj: Any,
        api_name: str,
        session_factory: Callable[[], Session],
        handlers: Dict[str, Handler],
    ) -> None:
        self._api_obj = api_obj
        self._api_name = api_name
        self._session_factory = session_factory
        self._handlers = handlers

    def __getattr__(self, method_name: str):
        target = getattr(self._api_obj, method_name)  # already returns `.data`

        def wrapped(*args, **kwargs):
            result = target(*args, **kwargs)  # this is the inner `.data`
            # Lookup handler by alias or class-name key
            key1 = f"{self._api_name}.{method_name}"
            key2 = None
            # Best-effort: if user accessed CamelCase (e.g., 'FleetApi'), support that too
            if self._api_name and self._api_name[0].islower():
                # try to map 'fleet' -> 'FleetApi' style
                cap = f"{self._api_name[0].upper()}{self._api_name[1:]}Api"
                key2 = f"{cap}.{method_name}"

            handler = self._handlers.get(key1) or (self._handlers.get(key2) if key2 else None)
            if handler:
                with self._session_factory() as session:
                    handler(session, result, args, kwargs, self._api_name, method_name)
            return result

        return wrapped


class WriteThrough:
    """
    Middleware wrapper for OpenAPIService's data-proxy.
    Usage:
        wt = WriteThrough(svc, SessionLocal, handlers=default_handlers())
        ships = wt.fleet.get_my_ships()  # returns data and writes through to DB
    """
    def __init__(
        self,
        svc: OpenAPIService,
        session_factory: Callable[[], Session],
        handlers: Dict[str, Handler] | None = None,
    ) -> None:
        self._svc = svc
        self._session_factory = session_factory
        self._handlers = handlers or {}

    def register(self, key: str, handler: Handler) -> None:
        self._handlers[key] = handler

    def __getattr__(self, api_name: str) -> _ApiDataProxyWT:
        # Delegate API lookup to the service's data-proxy namespace
        api_obj = getattr(self._svc.d, api_name)
        return _ApiDataProxyWT(api_obj, api_name, self._session_factory, self._handlers)
