# runner.py
import asyncio
import sqlite3

from api.api_async import AsyncFleetOps
from api.client import SpaceTradersClient
from api.db.pipeline import SpaceTradersDataManager


async def main():
    client = SpaceTradersClient()
    conn = sqlite3.connect("spacetraders.db")
    etl = SpaceTradersDataManager(client, conn)
    ops = AsyncFleetOps(client, conn, etl)

    # Setup DB row factory
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get mining site
    cur.execute("SELECT symbol FROM waypoints WHERE type IS 'ENGINEERED_ASTEROID'")
    cur.fetchone()["symbol"]

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

    # Get ships with mining lasers
    cur.execute("SELECT ship_symbol FROM fleet_mounts WHERE name LIKE 'Mining Laser%'")
    ships = [r[0] for r in cur.fetchall()]
    print("Ships with lasers: ", ships)

    # Run miners concurrently
    tasks = []
    # for ship in ships:
    # print(f"[INFO] Sending {ship} to {mine_site} for mining...")
    # tasks.append(asyncio.create_task(ops.mine_until_full(ship, mine_site)))

    for market_waypoint in market_waypoints:
        tasks.append(asyncio.create_task(ops.probe_markets(satellite, market_waypoint)))

    await asyncio.gather(*tasks, return_exceptions=True)

    conn.close()
    print("[INFO] Mining session complete.")


if __name__ == "__main__":
    asyncio.run(main())
