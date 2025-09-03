"""Convenience API namespaces for the SpaceTraders client.

This module exposes grouped accessors for the generated OpenAPI client.  The
``svc`` object provides the raw client, while the top-level variables like
``systems`` and ``fleet`` are *data-proxy* shortcuts that automatically return
``.data`` from responses.  In addition, the ``etl`` namespace wraps those
proxies with write-through handlers so that calling, for example,
``etl.fleet.get_my_ships()`` will normalize and persist the response to the
database.
"""

from __future__ import annotations

from services.client_service import OpenAPIService
from services.write_through import WriteThrough, default_handlers
from services.state_sync import state_handlers
from session import SessionLocal
from typing import Any


class APIProxy:
    """Proxy that delegates attribute lookups across all API groups.

    This allows calling endpoints directly, e.g. ``api.get_my_agent()``
    instead of ``api.agents.get_my_agent()``.
    """

    def __init__(self, service: OpenAPIService) -> None:
        self._service = service

    def __getattr__(self, name: str) -> Any:  # pragma: no cover - simple delegation
        d = self._service.d
        # Allow access to group namespaces directly (api.systems, api.agents, ...)
        if hasattr(d, name):
            return getattr(d, name)
        # Search each API group for the requested attribute
        for group in vars(d).values():
            if hasattr(group, name):
                return getattr(group, name)
        raise AttributeError(f"{name!r} not found in any API group")

# Instantiate the client service once; it lazily loads .env in its ctor
svc = OpenAPIService()

# Unified data-proxy accessor across API groups (e.g., api.get_my_agent())
api = APIProxy(svc)

# Write-through wrapper (returns .data and persists via handlers)
_handlers = default_handlers()
_handlers.update(state_handlers())
etl = WriteThrough(svc, SessionLocal, handlers=_handlers)

# Raw (non-data-proxy) access to the generated APIs
raw = svc.apis
