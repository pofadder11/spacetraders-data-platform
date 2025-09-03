# services/write_through.py
from __future__ import annotations

from typing import Any, Callable, Dict

from sqlalchemy.orm import Session

from services.client_service import OpenAPIService

# Handler signature: gets a Session and the `.data` returned by the API call.
Handler = Callable[[Session, Any], None]


from services.normalizer import upsert_fleet_nav as _upsert_nav

# Write-through relies on your dedicated normalizer


def default_handlers() -> Dict[str, Handler]:
    """
    Registry keys use either snake alias ('fleet') or class name ('FleetApi'),
    plus method name, e.g. 'fleet.get_my_ships'.
    """
    def handle_get_my_ships(session: Session, data: Any) -> None:
        # `data` is already the `.data` payload (list[Ship]) from the data-proxy
        _upsert_nav(session, data)

    return {
        "fleet.get_my_ships": handle_get_my_ships,
        "FleetApi.get_my_ships": handle_get_my_ships,
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
                    handler(session, result)
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
