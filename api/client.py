# api/client.py

class SpaceTradersClient:
    """
    Minimal stub of SpaceTraders API client.
    Used for testing CI and example usage.
    """

    def __init__(self, api_key: str = "TEST_KEY"):
        self.api_key = api_key

    def get_ships(self):
        """
        Return a fake list of ships (no real API call).
        """
        return [
            {"symbol": "SHIP-001", "type": "Fighter", "location": "OE-P1"},
            {"symbol": "SHIP-002", "type": "Miner", "location": "OE-P2"},
        ]
