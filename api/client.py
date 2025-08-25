import json
import sqlite3
import time
from typing import Any, Dict, Optional

import requests

import api.config as config


class SpaceTradersClient:
    """Minimal client for SpaceTraders API with optional caching."""

    def __init__(
        self, token: Optional[str] = None, db_path: Optional[str] = "cache.db"
    ):
        self.base_url = config.API_BASE_URL
        self.token = token or config.API_TOKEN
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        )

        self.db_path = db_path
        self._cache_enabled = db_path is not None
        self._init_db() if self._cache_enabled else setattr(self, "_cache", {})

        # Fetch headquarters systemSymbol at initialization
        self.system_symbol: Optional[str] = None
        self._init_system_symbol()

    def _init_system_symbol(self):
        """Initialize systemSymbol from
        agent headquarters (first two parts)."""
        agent = self.get_my_agent()
        hq = agent["data"]["headquarters"]
        self.headquarters = hq  # keep full string as well
        self.system_symbol = "-".join(hq.split("-")[:2])

    # -----------------------------
    # Cache setup
    # -----------------------------
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS api_cache (
                key TEXT PRIMARY KEY,
                response TEXT,
                timestamp REAL
            )
        """
        )
        conn.commit()
        conn.close()

    # -----------------------------
    # Generic request handler
    # -----------------------------
    def _request(
        self, method: str, endpoint: str, use_cache: bool = True, **kwargs
    ) -> Dict[str, Any]:
        cache_key = f"{method}:{endpoint}:{json.dumps(kwargs, sort_keys=True)}"

        # Check cache first
        if use_cache:
            if self._cache_enabled:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute(
                    "SELECT response, timestamp FROM api_cache WHERE key = ?",
                    (cache_key,),
                )
                row = c.fetchone()
                conn.close()
                if row:
                    return json.loads(row[0])
            else:
                if cache_key in self._cache:
                    return self._cache[cache_key]

        # Make actual API request
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}") from e

        # Save to cache
        if use_cache:
            if self._cache_enabled:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute(
                    "REPLACE INTO "
                    "api_cache (key, response, timestamp) VALUES (?, ?, ?)",
                    (cache_key, json.dumps(data), time.time()),
                )
                conn.commit()
                conn.close()
            else:
                self._cache[cache_key] = data

        return data

    # -----------------------------
    # API endpoints
    # -----------------------------
    def get_my_user(self) -> Dict[str, Any]:
        return self._request("GET", "my/account")

    def get_my_agent(self) -> Dict[str, Any]:
        return self._request("GET", "my/agent")

    def list_ships(self) -> Dict[str, Any]:
        return self._request("GET", "my/ships")

    def list_waypoints(
        self, system_symbol: Optional[str] = None
    ) -> Dict[str, Any]:
        """List waypoints for a system.
        Defaults to the agent’s headquarters system."""
        system_symbol = system_symbol or self.system_symbol
        if not system_symbol:
            raise ValueError("System symbol not set. Call get_my_agent first.")
        return self._request("GET", f"systems/{system_symbol}/waypoints")

    # Example for future expansion
    def transfer_cargo(
        self, ship_id: str, cargo_type: str, quantity: int, target_ship: str
    ) -> Dict[str, Any]:
        payload = {
            "cargo_type": cargo_type,
            "quantity": quantity,
            "target_ship": target_ship,
        }
        return
        self._request("POST", f"my/ships/{ship_id}/transfer", json=payload)

    # -----------------------------
    # Contract Endpoints
    # -----------------------------
    def list_contracts(self) -> Dict[str, Any]:
        """List all available contracts for the user."""
        return self._request("GET", "my/contracts")

    def accept_contract(self, contract_id: str) -> Dict[str, Any]:
        """Accept a contract by its ID."""
        endpoint = f"my/contracts/{contract_id}/accept"
        return self._request("POST", endpoint)

    # -----------------------------
    # Shipyard / Ships Endpoints
    # -----------------------------
    def list_shipyards(
        self, system_symbol: Optional[str] = None
    ) -> Dict[str, Any]:
        """List shipyards for a system.
        Defaults to the agent’s headquarters system."""
        system_symbol = system_symbol or self.system_symbol
        if not system_symbol:
            raise ValueError("System symbol not set. Call get_my_agent first.")
        return self._request(
            "GET", f"systems/{system_symbol}/waypoints?traits=SHIPYARD"
        )

    def list_shipyard_ships(
        self, system_symbol: str, waypoint_symbol: str
    ) -> Dict[str, Any]:
        """List ships and services available
        at a specific shipyard waypoint."""
        endpoint = (
            f"systems/{system_symbol}/waypoints/{waypoint_symbol}/shipyard"
        )
        return self._request("GET", endpoint)

    def purchase_ship(
        self, ship_type: str, waypoint_symbol: str
    ) -> Dict[str, Any]:
        """Purchase a new ship at a given shipyard waypoint."""
        endpoint = "my/ships"
        payload = {"shipType": ship_type, "waypointSymbol": waypoint_symbol}
        return self._request("POST", endpoint, json=payload)
