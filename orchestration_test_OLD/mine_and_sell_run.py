# runner.py
import asyncio
import random
import sqlite3

from api.api_async import AsyncFleetOps
from api.client import SpaceTradersClient
from api.db.pipeline import SpaceTradersDataManager


async def with_retries(coro_func, *args, retries=5, base_delay=2, **kwargs):
    for attempt in range(1, retries + 1):
        try:
            return await coro_func(*args, **kwargs)
        except Exception as e:
            if attempt == retries:
                print(
                    f"[ERROR] {coro_func.__name__} failed after {retries} retries: {e}"
                )
                raise
            delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
            print(
                f"[WARN] {coro_func.__name__} failed (attempt {attempt}), retrying in {delay:.1f}s..."
            )
            await asyncio.sleep(delay)


async def main():
    client = SpaceTradersClient()
    conn = sqlite3.connect("spacetraders.db")
    etl = SpaceTradersDataManager(client, conn)
    ops = AsyncFleetOps(client, conn, etl)
    """
    etl.waypoints()
    etl.shipyards()
    etl.fleet()
    etl.contracts()
    """

    # Setup DB row factory
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get mining site
    cur.execute("SELECT symbol FROM waypoints WHERE type IS 'ENGINEERED_ASTEROID'")
    mine_site = cur.fetchone()["symbol"]
    # Get ships with mining lasers
    cur.execute("SELECT ship_symbol FROM fleet_mounts WHERE name LIKE 'Mining Laser%'")
    ships = [r[0] for r in cur.fetchall()]
    print("Ships with lasers: ", ships)

    # get market waypoints

    cur.execute(
        "SELECT waypoint_symbol FROM traits WHERE trait_symbol IS 'MARKETPLACE'"
    )
    market_waypoints = [r[0] for r in cur.fetchall()]
    print("Market waypoints: ", market_waypoints)

    # get sattelite
    cur.execute("SELECT ship_symbol FROM fleet_specs WHERE frame_name is 'Probe'")
    satellite = cur.fetchone()["ship_symbol"]
    print("Sattelite :", satellite)

    # Run miners concurrently

    tasks = []
    for ship in ships:
        print(f"[INFO] Sending {ship} to {mine_site} for mining...")
        tasks.append(
            asyncio.create_task(with_retries(ops.mine_sell_repeat, ship, mine_site))
        )

    async def probe_all_markets(satellite, market_waypoints):
        for mw in market_waypoints:
            await with_retries(ops.probe_markets, satellite, mw)

    tasks.append(asyncio.create_task(probe_all_markets(satellite, market_waypoints)))

    await asyncio.gather(*tasks, return_exceptions=True)

    conn.close()
    print("[INFO] Session complete.")


if __name__ == "__main__":
    asyncio.run(main())
