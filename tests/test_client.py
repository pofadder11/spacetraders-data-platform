from api.client import SpaceTradersClient


def test_client_init():
    client = SpaceTradersClient(token="fake-token")
    assert client.token == "fake-token"


def test_list_ships_structure(monkeypatch):
    # Monkeypatch _request to avoid real API call
    client = SpaceTradersClient(token="fake-token")
    monkeypatch.setattr(
        client, "_request", lambda method, endpoint, **kw: {"ships": []}
    )

    resp = client.list_ships()
    assert "ships" in resp
