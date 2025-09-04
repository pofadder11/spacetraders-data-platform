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

    """
    # hacky test. remove and integrate client side if this works
    async def update_ship_status(conn, ship_symbol: str, new_status: str):
        conn.execute(
            "UPDATE fleet_nav SET status = ? WHERE ship_symbol = ?",
            (new_status, ship_symbol)
        )
    conn.commit()"""

    async def prepare_ship_for_navigation(self, ship_symbol: str):
        print("[debug]: Start Nav Prep")
        """Dock, refuel, and orbit ship before navigation."""
        self.etl.fleet()

        self.cur.execute(
            """
        SELECT 
            fn.status,
            fs.fuel_current,
            fs.fuel_capacity
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

        print("[DEBUG]: db call for status etc.", status)

        if status == "IN_TRANSIT":
            self.cur.execute(
                """
            SELECT arrival_time
            FROM journeys_log
            WHERE ship_symbol = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """,
                (ship_symbol,),
            )
            arrival_time = self.cur.fetchone()[0]
            print("DEBUG: Raw arrival :", arrival_time)
            arrival_dt = datetime.fromisoformat(arrival_time.replace("Z", "+00:00"))
            print("DEBUG: arrival :", arrival_dt)
            now = datetime.now(timezone.utc)
            wait_sec = max(0, (arrival_dt - now).total_seconds())
            print("DEBUG: wait_sec :", wait_sec)
            print(f"[INFO] {ship_symbol} en route, sleeping {wait_sec:.0f}s...")
            await asyncio.sleep(wait_sec + 1)

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
        print("INFO: Nav prep done, preparing to fly!")

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

        await self.prepare_ship_for_navigation(ship_symbol)
        self.etl.journey(ship_symbol, waypoint_symbol)
        # parse arrival time
        self.cur.execute(
            """
            SELECT arrival_time
            FROM journeys_log
            ORDER BY timestamp DESC
            LIMIT 1
            """
        )
        arrival = self.cur.fetchone()[0]

        # Wait until arrival
        arrival_dt = datetime.fromisoformat(arrival.replace("Z", "+00:00"))
        print("DEBUG: arrival :", arrival_dt)
        now = datetime.now(timezone.utc)
        wait_sec = max(0, (arrival_dt - now).total_seconds())
        print("DEBUG: wait_sec :", wait_sec)
        print(f"[INFO] {ship_symbol} en route, sleeping {wait_sec:.0f}s...")
        await asyncio.sleep(wait_sec + 5)

    async def probe_markets(self, ship_symbol: str, market_waypoint: str):
        """
        Navigate to market waypoint if needed, then get marketplace data
        """
        # --- Get current waypoint ---
        print("[INFO]: starting probe_markets")
        await self.nav(ship_symbol, market_waypoint)
        print("[INFO]: probe_markets arrived, docking")
        self.client.dock_ship(ship_symbol)
        print("[INFO]: probe_markets docked, starting ETL")
        self.etl.market_prices(market_waypoint)
        print("[INFO]: probe_markets complete")
        self.etl.fleet()

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

    async def mine_sell_repeat(self, ship_symbol: str, mine_site: str):
        # 1. Mine until cargo is full
        print("[DEBUG]: ")
        await self.mine_until_full(ship_symbol, mine_site)

        # 2. Find the best market
        self.cur.execute(
            """
            SELECT tg.waypoint_symbol,
                GROUP_CONCAT(tg.trade_symbol) AS sellable_goods,
                SUM(fci.units * tg.sell_price) AS total_value
            FROM tradegoods_log tg
            JOIN fleet_cargo_inventory fci
            ON tg.trade_symbol = fci.symbol
            WHERE fci.ship_symbol = ?
            AND tg.sell_price IS NOT NULL
            GROUP BY tg.waypoint_symbol
            ORDER BY total_value DESC
            LIMIT 1;
            """,
            (ship_symbol,),
        )
        row = self.cur.fetchone()
        if not row:
            print(f"[WARNING] No markets found for ship {ship_symbol}")
            return

        market, goods_str, _ = row
        goods = goods_str.split(",")

        # 3. Navigate to that market
        await self.nav(ship_symbol, market)

        # 4. Sell all relevant goods
        for g in goods:
            self.client.sell_cargo(ship_symbol, g)

        # 5. Repeat cycle
        await self.mine_sell_repeat(ship_symbol, mine_site)
