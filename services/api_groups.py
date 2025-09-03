# services/api.py
from __future__ import annotations

from services.client_service import OpenAPIService

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

# If you also want raw (non-data-proxy) access:
raw = svc.apis

# Expose the full data-proxy namespace for convenience in helper functions
etl = svc.d
