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
from session import SessionLocal

# Create one shared service. If you prefer lazy init, wrap this in a function.
svc = OpenAPIService()

# “Data-proxy” shortcuts: method calls return `.data` automatically.
systems = svc.d.systems
agents = svc.d.agents
fleet = svc.d.fleet
contracts = svc.d.contracts
factions = svc.d.factions
data_api = svc.d.data  # named 'data_api' to avoid name clash with 'data'
global_api = svc.d.global_api  # GlobalApi → global_api alias

# ETL write-through namespace: persisting normalized responses automatically.
etl = WriteThrough(svc, SessionLocal, handlers=default_handlers())

# If you also want raw (non-data-proxy) access:
raw = svc.apis
