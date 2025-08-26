import json
from typing import Any, Dict, Optional

import requests

import api.config as config


class SpaceTradersClient:
    """Minimal SpaceTraders API client (no caching, only global system_symbol)."""

    def __init__(self, token: Optional[str] = None):
        self.base_url = config.API_BASE_URL
        self.token = token or config.API_TOKEN
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        )

        # Global system symbol for convenience
        self.system_symbol: Optional[str] = None
        self._init_system_symbol()

    def _init_system_symbol(self):
        """Initialize systemSymbol from agent headquarters (first two parts)."""
        agent = self.get_my_agent()
        hq = agent["data"]["headquarters"]
        self.headquarters = hq  # keep full HQ symbol as well
        self.system_symbol = "-".join(hq.split("-")[:2])

    # -----------------------------
    # Generic request handler
    # -----------------------------
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        # Debug: show request info
        print("[DEBUG] Making request:")
        print(f"  Method: {method}")
        print(f"  URL: {self.base_url}/{endpoint.lstrip('/')}")
        print(f"  kwargs: {json.dumps(kwargs, indent=2, default=str)}")

        # Ensure empty JSON body for POST/PUT/PATCH if not provided
        headers = kwargs.get("headers", self.session.headers)
        if method.upper() in {"POST", "PUT", "PATCH"}:
            has_json_header = headers and "application/json" in headers.get(
                "Content-Type", ""
            )
            if has_json_header and "json" not in kwargs and "data" not in kwargs:
                kwargs["json"] = {}
                print("[DEBUG] Injected empty JSON body {}")

        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = self.session.request(method, url, timeout=10, **kwargs)
            print(f"[DEBUG] Response status: {response.status_code}")
            print(f"[DEBUG] Raw response text: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[DEBUG] RequestException: {e}")
            raise RuntimeError(f"API request failed: {e}") from e
        except ValueError:
            return {"raw_response": response.text}

    # -----------------------------
    # API endpoints
    # -----------------------------
    def get_my_user(self) -> Dict[str, Any]:
        return self._request("GET", "my/account")

    def get_my_agent(self) -> Dict[str, Any]:
        return self._request("GET", "my/agent")

    def list_ships(self) -> Dict[str, Any]:
        return self._request("GET", "my/ships")

    def list_waypoints(self, system_symbol: Optional[str] = None) -> Dict[str, Any]:
        """List waypoints for a system."""
        system_symbol = system_symbol or self.system_symbol
        if not system_symbol:
            raise ValueError("System symbol not set. Call get_my_agent first.")
        return self._request("GET", f"systems/{system_symbol}/waypoints")

    def list_contracts(self) -> Dict[str, Any]:
        return self._request("GET", "my/contracts")

    def accept_contract(self, contract_id: str) -> Dict[str, Any]:
        return self._request("POST", f"my/contracts/{contract_id}/accept")

    def list_shipyards(self, system_symbol: Optional[str] = None) -> Dict[str, Any]:
        system_symbol = system_symbol or self.system_symbol
        return self._request(
            "GET", f"systems/{system_symbol}/waypoints?traits=SHIPYARD"
        )

    def list_shipyard_ships(
        self, system_symbol: str, waypoint_symbol: str
    ) -> Dict[str, Any]:
        endpoint = f"systems/{system_symbol}/waypoints/{waypoint_symbol}/shipyard"
        return self._request("GET", endpoint)

    def purchase_ship(self, ship_type: str, waypoint_symbol: str) -> Dict[str, Any]:
        return self._request(
            "POST",
            "my/ships",
            json={"shipType": ship_type, "waypointSymbol": waypoint_symbol},
        )

    def navigate_ship(self, ship_symbol: str, waypoint_symbol: str) -> Dict[str, Any]:
        return self._request(
            "POST",
            f"my/ships/{ship_symbol}/navigate",
            json={"waypointSymbol": waypoint_symbol},
        )

    def dock_ship(self, ship_symbol: str) -> Dict[str, Any]:
        return self._request("POST", f"my/ships/{ship_symbol}/dock")

    def orbit_ship(self, ship_symbol: str) -> Dict[str, Any]:
        return self._request("POST", f"my/ships/{ship_symbol}/orbit")

    def refuel_ship(self, ship_symbol: str) -> Dict[str, Any]:
        return self._request("POST", f"my/ships/{ship_symbol}/refuel")

    def negotiate_contract(self, ship_symbol: str) -> Dict[str, Any]:
        return self._request("POST", f"my/ships/{ship_symbol}/negotiate/contract")
