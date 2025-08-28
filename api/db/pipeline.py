"""
This needs to be incorporated into data logging in order to reduce
code clutter and duplication in orchestration/run_startup.py
"""

import sqlite3

from api.client import SpaceTradersClient
from api.normalizer import normalize_contracts, normalize_fleet


class SpaceTradersDataManager:
    def __init__(self, client: SpaceTradersClient, conn: sqlite3.Connection):
        self.client = client
        self.conn = conn

    # -----------------------
    # Fleet
    # -----------------------
    def store_fleet(self):
        fleet_json = self.client.list_ships()
        normalize_fleet(self.conn, fleet_json)
        print("[INFO] Fleet data stored.")

    # -----------------------
    # Contracts
    # -----------------------
    def store_contracts(self):
        contracts_json = self.client.list_contracts()
        normalize_contracts(self.conn, contracts_json)
        print("[INFO] Contracts stored.")
