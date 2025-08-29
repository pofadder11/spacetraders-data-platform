import asyncio
import sqlite3

from api.api_async import AsyncFleetOps
from api.client import SpaceTradersClient

# Setup
client = SpaceTradersClient()
conn = sqlite3.connect("spacetraders.db")
conn.row_factory = sqlite3.Row
fleet_ops = AsyncFleetOps(client, conn)

# Find a mining site
cur = conn.cursor()
cur.execute("SELECT symbol FROM waypoints WHERE type IS 'ENGINEERED_ASTEROID'")
row = cur.fetchone()
if not row:
    raise RuntimeError("No ENGINEERED_ASTEROID waypoint found in DB")
mine_site = row["symbol"]

# Find ships with mining lasers
cur.execute("SELECT ship_symbol FROM fleet_mounts WHERE name LIKE 'Mining Laser%'")
rows = cur.fetchall()
mining_ships = [r[0] for r in rows] if rows else []


async def main():
    tasks = [fleet_ops.mine_at_waypoint(ship, mine_site) for ship in mining_ships]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
    conn.close()
    print("[INFO] Mining done.")
