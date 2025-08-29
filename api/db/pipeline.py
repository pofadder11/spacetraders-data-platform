import sqlite3

from api.client import SpaceTradersClient
from api.normalizer import Normalizer


class SpaceTradersDataManager:
    def __init__(self, client: SpaceTradersClient, conn: sqlite3.Connection):
        self.client = client
        self.conn = conn
        self.nmz = Normalizer(conn)

    def fleet(self):
        fleet_json = self.client.list_ships()
        self.nmz.normalize_fleet(fleet_json)
        print("[INFO] Fleet data stored.")

    def contracts(self):
        contracts_json = self.client.list_contracts()
        self.nmz.normalize_contracts(contracts_json)
        print("[INFO] Contracts stored.")

    def waypoints(self):
        waypoints_json = self.client.list_waypoints()
        self.nmz.normalize_waypoints(waypoints_json)
        print("[INFO] Waypoints stored.")

    def shipyards(self):
        shipyards_json = self.client.list_shipyards()
        self.nmz.normalize_shipyards(shipyards_json)
        print("[INFO] Shipyards stored.")

    def ship_markets(self, shipyard_symbol: str):
        shipyard_ships_json = self.client.list_shipyard_ships(shipyard_symbol)
        self.nmz.normalize_shipyard_ships(shipyard_ships_json)
        print("[INFO] Shipyard ships stored.")

    def journey(self, ship_symbol: str, waypoint_symbol: str):
        journeys_json = self.client.navigate_ship(ship_symbol, waypoint_symbol)
        self.nmz.normalize_journey(journeys_json, ship_symbol)
        print("[INFO] Ship journey stored.")
