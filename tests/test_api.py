# tests/test_api.py
# import pytest

from api.client import SpaceTradersClient


def test_get_ships_returns_list():
    client = SpaceTradersClient()
    ships = client.get_ships()

    # Test that it returns a list
    assert isinstance(ships, list)
    # Test that first item has expected keys
    assert "symbol" in ships[0]
    assert "type" in ships[0]
    assert "location" in ships[0]
