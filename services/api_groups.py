from session import SessionLocal
from typing import Any
from services.client_service import OpenAPIService
from services.write_through import WriteThrough, default_handlers


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


# Create one shared service and a proxy for convenient access
svc = OpenAPIService()
api = APIProxy(svc)

# Raw (non-data-proxy) access is still available if needed
raw = svc.apis

# Write-through ETL helper
etl = WriteThrough(svc, SessionLocal, handlers=default_handlers())