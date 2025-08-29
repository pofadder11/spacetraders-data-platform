import asyncio
import sqlite3
from datetime import datetime

from api.client import SpaceTradersClient
from api.db.pipeline import SpaceTradersDataManager


class AsyncFleetOps:
    def __init__(self, client: SpaceTradersClient, conn: sqlite3.Connection):
        self.client = client
        self.conn = conn
        self.cur = conn.cursor()
        self.etl = SpaceTradersDataManager(client, conn)

    async def prepare_ship_for_navigation(self, ship_symbol: str):
        self.etl.fleet()  # refresh fleet data
        self.cur.execute(
            """
            SELECT fn.status, fs.fuel_current, fs.fuel_capacity
            FROM fleet_nav fn
            JOIN fleet_specs fs ON fn.ship_symbol = fs.ship_symbol
            WHERE fn.ship_symbol = ?
            """,
            (ship_symbol,),
        )
        row = self.cur.fetchone()
        if not row:
            raise RuntimeError(f"No fleet_nav entry for ship {ship_symbol}")

        status, fuel_current, fuel_capacity = row

        # Dock + refuel if needed
        if fuel_current < fuel_capacity:
            if status != "DOCKED":
                print(f"[INFO] Docking {ship_symbol} (status: {status})")
                self.client.dock_ship(ship_symbol)
                await asyncio.sleep(2)
            print(f"[INFO] Refueling {ship_symbol} ({fuel_current}/{fuel_capacity})")
            self.client.refuel_ship(ship_symbol)
            await asyncio.sleep(2)
            self.etl.fleet()

        # Ensure orbiting before navigating
        if status != "IN_ORBIT":
            print(f"[INFO] Orbiting {ship_symbol} (status: {status})")
            self.client.orbit_ship(ship_symbol)
            await asyncio.sleep(2)
            self.etl.fleet()

    async def nav(self, ship_symbol: str, waypoint_symbol: str):
        self.cur.execute(
            "SELECT waypointSymbol, status FROM fleet_nav WHERE ship_symbol = ?",
            (ship_symbol,),
        )
        row = self.cur.fetchone()
        if not row:
            print(f"[WARNING] No fleet_nav entry for {ship_symbol}, skipping")
            return

        current_wp, status = row
        if current_wp == waypoint_symbol:
            print(f"[INFO] Ship {ship_symbol} already at {waypoint_symbol}, skipping")
            return

        print(f"[DEBUG] Navigating {ship_symbol} to {waypoint_symbol}")
        await self.prepare_ship_for_navigation(ship_symbol)
        nav_resp = self.client.navigate_ship(ship_symbol, waypoint_symbol)
        self.etl.fleet()

        # Parse route travel time
        route = nav_resp["data"]["nav"]["route"]
        dep_dt = datetime.fromisoformat(route["departureTime"].replace("Z", "+00:00"))
        arr_dt = datetime.fromisoformat(route["arrival"].replace("Z", "+00:00"))
        travel_seconds = (arr_dt - dep_dt).total_seconds()
        print(f"[INFO] Travel time: {travel_seconds:.1f} seconds")
        await asyncio.sleep(travel_seconds + 1)

    async def extract_resource(self, ship_symbol: str):
        print(f"[INFO] Extracting resources with {ship_symbol}")
        self.client.orbit_ship(ship_symbol)
        self.client.extract(ship_symbol)
        self.etl.fleet()
        await asyncio.sleep(2)

    async def mine_at_waypoint(self, ship_symbol: str, waypoint_symbol: str):
        """Full pipeline: navigate ship to waypoint, then mine."""
        await self.nav(ship_symbol, waypoint_symbol)
        await self.extract_resource(ship_symbol)
