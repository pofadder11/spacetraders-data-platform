# api/api_async.py
import asyncio
import sqlite3
from datetime import datetime, timezone

from api.client import SpaceTradersClient
from api.db.pipeline import SpaceTradersDataManager

client = SpaceTradersClient()
conn = sqlite3.connect("spacetraders.db")
etl = SpaceTradersDataManager(client, conn)


class AsyncFleetOps:
    def __init__(self, client, conn, etl):
        self.client = client
        self.conn = conn
        self.cur = conn.cursor()
        self.etl = etl
        self.conn.row_factory = None  # set if you want sqlite.Row

    async def _sleep(self, seconds: float):
        """Async sleep wrapper."""
        await asyncio.sleep(seconds)

    async def prepare_ship_for_navigation(self, ship_symbol: str):
        """Dock, refuel, and orbit ship before navigation."""
        self.etl.fleet()
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

        # Refuel if not at capacity
        if fuel_current < fuel_capacity:
            if status != "DOCKED":
                print(f"[INFO] Docking {ship_symbol} (status: {status})")
                self.client.dock_ship(ship_symbol)
                await self._sleep(2)
            print(f"[INFO] Refueling {ship_symbol} ({fuel_current}/{fuel_capacity})")
            self.client.refuel_ship(ship_symbol)
            await self._sleep(2)
            self.etl.fleet()

        # Ensure in orbit
        if status != "IN_ORBIT":
            print(f"[INFO] Orbiting {ship_symbol} (status: {status})")
            self.client.orbit_ship(ship_symbol)
            await self._sleep(2)
            self.etl.fleet()

    async def nav(self, ship_symbol: str, waypoint_symbol: str):
        """Navigate ship unless already at target waypoint."""
        self.cur.execute(
            "SELECT waypointSymbol, status FROM fleet_nav WHERE ship_symbol = ?",
            (ship_symbol,),
        )
        row = self.cur.fetchone()
        if not row:
            print(f"[WARNING] No fleet_nav entry for {ship_symbol}, skipping")
            return

        current_wp, status = row
        print(
            f"[INFO] Current waypoint for {ship_symbol}: {current_wp} (status: {status})"
        )

        if current_wp == waypoint_symbol:
            print(
                f"[INFO] Ship {ship_symbol} already at {waypoint_symbol}, skipping navigation"
            )
            return

        print(f"[DEBUG] Navigating {ship_symbol} to {waypoint_symbol}")
        self.etl.fleet()
        await self.prepare_ship_for_navigation(ship_symbol)
        nav_resp = self.client.navigate_ship(ship_symbol, waypoint_symbol)
        self.etl.fleet()

        # Parse travel times
        route = nav_resp["data"]["nav"]["route"]
        dep_dt = datetime.fromisoformat(route["departureTime"].replace("Z", "+00:00"))
        arr_dt = datetime.fromisoformat(route["arrival"].replace("Z", "+00:00"))
        travel_seconds = (arr_dt - dep_dt).total_seconds()
        print(f"[INFO] Travel time: {travel_seconds:.1f} seconds")
        await self._sleep(travel_seconds + 1)

    async def mine_until_full(self, ship_symbol: str, mine_site: str):
        """
        Navigate ship to mine_site if needed, then repeatedly mine until cargo full,
        respecting cooldowns.
        """
        # --- Get current nav + cargo status ---

        # Refresh fleet data
        self.etl.fleet()

        self.cur.execute(
            """
            SELECT waypointSymbol, cargo_units, cargo_capacity
            FROM fleet_nav
            WHERE ship_symbol = ?
        """,
            (ship_symbol,),
        )
        nav_row = self.cur.fetchone()
        if not nav_row:
            print(f"[WARN] No nav record found for {ship_symbol}")
            return

        current_wp, cargo_units, cargo_capacity = nav_row

        # --- Navigate if not already at mining site ---
        if current_wp != mine_site:
            print(f"[INFO] {ship_symbol} navigating to {mine_site}...")
            self.client.navigate_ship(ship_symbol, mine_site)
            # Wait until arrival
            self.cur.execute(
                """
                SELECT route_arrival
                FROM fleet_nav
                WHERE ship_symbol = ?
            """,
                (ship_symbol,),
            )
            arrival = self.cur.fetchone()[0]
            arrival_dt = datetime.fromisoformat(arrival.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            wait_sec = max(0, (arrival_dt - now).total_seconds())
            print(f"[INFO] {ship_symbol} en route, sleeping {wait_sec:.0f}s...")
            await asyncio.sleep(wait_sec + 1)

        # --- Loop mining until full ---
        self.etl.fleet()
        while cargo_units < cargo_capacity:
            self.cur.execute(
                """
                SELECT cooldown_remainingSeconds
                FROM fleet_specs
                WHERE ship_symbol = ?
            """,
                (ship_symbol,),
            )
            cooldown_row = self.cur.fetchone()
            if cooldown_row and cooldown_row[0]:
                wait_sec = cooldown_row[0]
                if wait_sec > 0:
                    print(
                        f"[INFO] {ship_symbol} cooling down, sleeping {wait_sec:.0f}s..."
                    )
                    await asyncio.sleep(wait_sec + 1)

            # Perform mine attempt
            print(f"[ACTION] {ship_symbol} extracting resources...")
            mine_resp = self.client.extract(ship_symbol)
            wait_sec = mine_resp["data"]["cooldown"]["totalSeconds"]
            print("[INFO]: Waiting time from mining response: ", wait_sec)
            await asyncio.sleep(wait_sec + 1)
            wait_sec = 0

            # Update cargo from DB
            self.cur.execute(
                """
                SELECT cargo_units, cargo_capacity
                FROM fleet_nav
                WHERE ship_symbol = ?
            """,
                (ship_symbol,),
            )
            cargo_units, cargo_capacity = self.cur.fetchone()

            if cargo_units >= cargo_capacity:
                print(
                    f"[INFO] {ship_symbol} cargo full ({cargo_units}/{cargo_capacity})"
                )
                break
