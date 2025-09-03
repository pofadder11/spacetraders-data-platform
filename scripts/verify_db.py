from __future__ import annotations

from sqlalchemy import select

from session import init_db, SessionLocal
from models import FleetNav, ShipCurrent, MarketTradeGoodCurrent


def main() -> None:
    init_db()
    with SessionLocal() as s:
        print("-- FleetNav sample --")
        rows = s.execute(select(FleetNav).limit(5)).scalars().all()
        for r in rows:
            print(r.ship_symbol, r.status, r.system_symbol, "->", r.route_destination_waypoint, r.route_arrival_time)

        print("\n-- ShipsCurrent sample --")
        rows = s.execute(select(ShipCurrent).limit(5)).scalars().all()
        for r in rows:
            print(r.ship_symbol, r.nav_status, r.fuel_current, "/", r.fuel_capacity, "at", r.system_symbol, r.waypoint_symbol)

        print("\n-- MarketTradeGoodCurrent sample --")
        rows = s.execute(select(MarketTradeGoodCurrent).limit(5)).scalars().all()
        for r in rows:
            print(r.waypoint_symbol, r.trade_symbol, r.sell_price, "obs:", r.observed_at)


if __name__ == "__main__":
    main()

