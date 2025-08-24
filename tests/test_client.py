import os
from unittest.mock import patch

import pytest

from api.client import SpaceTradersClient

# Ensure a token exists so config.py doesn’t raise
os.environ["SPACETRADERS_TOKEN"] = "fake-token"

# Sample mock response data
MOCK_USER_DATA = {"user": {"username": "test_user"}}
MOCK_SHIPS_DATA = {"ships": [{"symbol": "SHIP_1", "type": "Fighter"}]}


@pytest.fixture
def client():
    return SpaceTradersClient(db_path=None)  # in-memory cache for tests


def test_get_my_user_cached(client):
    with patch.object(
        client, "_request", return_value=MOCK_USER_DATA
    ) as mock_request:
        # First call: triggers _request
        user1 = client.get_my_user()
        assert user1 == MOCK_USER_DATA
        mock_request.assert_called_once_with("GET", "my/account")

        # Second call: cache should return same result
        # without new _request call
        user2 = client.get_my_user()
        assert user2 == MOCK_USER_DATA
        # Still only one _request call because caching is enabled
        mock_request.assert_called_once()


def test_list_ships_cached(client):
    with patch.object(
        client, "_request", return_value=MOCK_SHIPS_DATA
    ) as mock_request:
        ships1 = client.list_ships()
        assert ships1 == MOCK_SHIPS_DATA
        mock_request.assert_called_once_with("GET", "my/ships")

        ships2 = client.list_ships()
        assert ships2 == MOCK_SHIPS_DATA
        mock_request.assert_called_once()


def test_transfer_cargo_calls_request(client):
    with patch.object(
        client, "_request", return_value={"success": True}
    ) as mock_request:
        result = client.transfer_cargo(
            ship_id="SHIP_1",
            cargo_type="ORE",
            quantity=10,
            target_ship="SHIP_2",
        )
        assert result == {"success": True}
        mock_request.assert_called_once_with(
            "POST",
            "my/ships/SHIP_1/transfer",
            json={
                "cargo_type": "ORE",
                "quantity": 10,
                "target_ship": "SHIP_2",
            },
        )
