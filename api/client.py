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
    # Example API endpoints
    # -----------------------------
    def get_my_user(self) -> Dict[str, Any]:
        return self._request("GET", "my/account")

    def list_ships(self) -> Dict[str, Any]:
        return self._request("GET", "my/ships")

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


# Initialize the client
client = SpaceTradersClient()

# Call an API method
ships = client.list_ships()

# Inspect results
print(ships)
