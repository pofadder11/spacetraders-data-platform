from typing import Any, Dict, Optional

import requests

import config


class SpaceTradersClient:
    """Minimal client for SpaceTraders API."""

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

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Generic request handler."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Log / raise as needed
            raise RuntimeError(f"API request failed: {e}") from e

    # Example: get my user/account info
    def get_my_user(self) -> Dict[str, Any]:
        return self._request("GET", "my/account")

    # Example: list ships
    def list_ships(self) -> Dict[str, Any]:
        return self._request("GET", "my/ships")
