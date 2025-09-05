from __future__ import annotations

from typing import Any, Optional, List

from fastapi import FastAPI, Query
from pydantic import BaseModel

from db.async_session import SessionLocal, check_db_connection_async
from models import (
    ShipCurrent,
    FleetNav,
    MarketTradeGoodCurrent,
    ShipCargoCurrent,
    ShipyardOfferCurrent,
    System as DbSystem,
    Waypoint as DbWaypoint,
    MarketTradeGoodSnapshot as DbMktSnap,
    ExtractionYield as DbYield,
)
from sqlalchemy import select, func
from services import runner_status as rs


def create_app() -> FastAPI:
    app = FastAPI(title="Spacetraders Data API")

    @app.on_event("startup")
    async def _startup():
        await check_db_connection_async()

    class Item(BaseModel):
        data: Any

    @app.get("/status")
    async def status():
        loops = await rs.get_loops()
        return {"loops": loops}

    @app.get("/actions")
    async def actions(n: int = 100):
        return await rs.get_recent(n)

    @app.get("/fleet")
    async def fleet(limit: int = 200):
        async with SessionLocal() as s:
            rows = (await s.execute(select(ShipCurrent).limit(limit))).scalars().all()
            return [
                {
                    "ship_symbol": r.ship_symbol,
                    "role": r.role,
                    "nav_status": r.nav_status,
                    "flight_mode": r.flight_mode,
                    "system_symbol": r.system_symbol,
                    "waypoint_symbol": r.waypoint_symbol,
                    "fuel_current": r.fuel_current,
                    "fuel_capacity": r.fuel_capacity,
                    "cargo_units": r.cargo_units,
                    "updated_at": r.updated_at.isoformat() if r.updated_at else None,
                }
                for r in rows
            ]

    @app.get("/nav")
    async def nav(limit: int = 200):
        async with SessionLocal() as s:
            rows = (await s.execute(select(FleetNav).limit(limit))).scalars().all()
            return [
                {
                    "ship_symbol": r.ship_symbol,
                    "status": r.status,
                    "flight_mode": r.flight_mode,
                    "system_symbol": r.system_symbol,
                    "waypoint_symbol": r.waypoint_symbol,
                    "route_arrival_time": r.route_arrival_time.isoformat() if r.route_arrival_time else None,
                    "updated_at": r.updated_at.isoformat() if r.updated_at else None,
                }
                for r in rows
            ]

    @app.get("/markets/current")
    async def markets_current(
        waypoint: Optional[str] = None,
        trade_symbol: Optional[str] = None,
        limit: int = 500,
    ):
        async with SessionLocal() as s:
            stmt = select(MarketTradeGoodCurrent)
            if waypoint:
                stmt = stmt.where(MarketTradeGoodCurrent.waypoint_symbol == waypoint)
            if trade_symbol:
                stmt = stmt.where(MarketTradeGoodCurrent.trade_symbol == trade_symbol)
            rows = (await s.execute(stmt.limit(limit))).scalars().all()
            return [
                {
                    "waypoint_symbol": r.waypoint_symbol,
                    "trade_symbol": r.trade_symbol,
                    "observed_at": r.observed_at.isoformat() if r.observed_at else None,
                    "sell_price": r.sell_price,
                    "purchase_price": r.purchase_price,
                    "activity": r.activity,
                    "supply": r.supply,
                }
                for r in rows
            ]

    @app.get("/cargo/current")
    async def cargo_current(ship: Optional[str] = None, limit: int = 1000):
        async with SessionLocal() as s:
            stmt = select(ShipCargoCurrent)
            if ship:
                stmt = stmt.where(ShipCargoCurrent.ship_symbol == ship)
            rows = (await s.execute(stmt.limit(limit))).scalars().all()
            return [
                {
                    "ship_symbol": r.ship_symbol,
                    "trade_symbol": r.trade_symbol,
                    "units": r.units,
                    "updated_at": r.updated_at.isoformat() if r.updated_at else None,
                }
                for r in rows
            ]

    @app.get("/systems")
    async def systems(limit: int = 500):
        async with SessionLocal() as s:
            rows = (await s.execute(select(DbSystem).limit(limit))).scalars().all()
            return [
                {"symbol": r.symbol, "type": r.type, "x": r.x, "y": r.y}
                for r in rows
            ]

    @app.get("/waypoints")
    async def waypoints(system: Optional[str] = None, limit: int = 2000):
        async with SessionLocal() as s:
            stmt = select(DbWaypoint)
            if system:
                stmt = stmt.where(DbWaypoint.system_symbol == system)
            rows = (await s.execute(stmt.limit(limit))).scalars().all()
            return [
                {
                    "symbol": r.symbol,
                    "system_symbol": r.system_symbol,
                    "type": r.type,
                    "x": r.x,
                    "y": r.y,
                }
                for r in rows
            ]

    @app.get("/markets/snapshots")
    async def markets_snapshots(
        waypoint: Optional[str] = None,
        trade_symbol: Optional[str] = None,
        limit: int = 5000,
    ):
        async with SessionLocal() as s:
            stmt = select(DbMktSnap)
            if waypoint:
                stmt = stmt.where(DbMktSnap.waypoint_symbol == waypoint)
            if trade_symbol:
                stmt = stmt.where(DbMktSnap.trade_symbol == trade_symbol)
            rows = (await s.execute(stmt.limit(limit))).scalars().all()
            return [
                {
                    "waypoint_symbol": r.waypoint_symbol,
                    "trade_symbol": r.trade_symbol,
                    "observed_at": r.observed_at.isoformat() if r.observed_at else None,
                    "sell_price": r.sell_price,
                    "purchase_price": r.purchase_price,
                    "activity": r.activity,
                    "supply": r.supply,
                }
                for r in rows
            ]

    @app.get("/yields")
    async def yields(ship: Optional[str] = None, limit: int = 2000):
        async with SessionLocal() as s:
            stmt = select(DbYield)
            if ship:
                stmt = stmt.where(DbYield.ship_symbol == ship)
            rows = (await s.execute(stmt.limit(limit))).scalars().all()
            return [
                {
                    "observed_at": r.observed_at.isoformat() if r.observed_at else None,
                    "ship_symbol": r.ship_symbol,
                    "waypoint_symbol": r.waypoint_symbol,
                    "trade_symbol": r.trade_symbol,
                    "units": r.units,
                    "cooldown_total_seconds": r.cooldown_total_seconds,
                    "cooldown_remaining_seconds": r.cooldown_remaining_seconds,
                }
                for r in rows
            ]

    @app.get("/viz/ships_positions")
    async def viz_ships_positions():
        async with SessionLocal() as s:
            rows = (
                await s.execute(
                    select(
                        FleetNav.ship_symbol,
                        ShipCurrent.role,
                        FleetNav.status,
                        DbWaypoint.x,
                        DbWaypoint.y,
                    )
                    .join(DbWaypoint, DbWaypoint.symbol == FleetNav.waypoint_symbol)
                    .outerjoin(ShipCurrent, ShipCurrent.ship_symbol == FleetNav.ship_symbol)
                )
            ).all()
            return [
                {
                    "ship_symbol": sym,
                    "role": role,
                    "status": status,
                    "x": x,
                    "y": y,
                }
                for sym, role, status, x, y in rows
            ]

    @app.get("/viz/waypoints")
    async def viz_waypoints(system: Optional[str] = None, limit: int = 5000):
        async with SessionLocal() as s:
            stmt = select(DbWaypoint)
            if system:
                stmt = stmt.where(DbWaypoint.system_symbol == system)
            rows = (await s.execute(stmt.limit(limit))).scalars().all()
            return [
                {
                    "symbol": r.symbol,
                    "system_symbol": r.system_symbol,
                    "type": r.type,
                    "x": r.x,
                    "y": r.y,
                }
                for r in rows
            ]
    @app.get("/shipyards/current")
    async def shipyards_current(waypoint: Optional[str] = None, limit: int = 1000):
        async with SessionLocal() as s:
            stmt = select(ShipyardOfferCurrent)
            if waypoint:
                stmt = stmt.where(ShipyardOfferCurrent.waypoint_symbol == waypoint)
            rows = (await s.execute(stmt.limit(limit))).scalars().all()
            return [
                {
                    "waypoint_symbol": r.waypoint_symbol,
                    "ship_type": r.ship_type,
                    "name": r.name,
                    "purchase_price": r.purchase_price,
                    "observed_at": r.observed_at.isoformat() if r.observed_at else None,
                }
                for r in rows
            ]

    @app.get("/shipyards/status")
    async def shipyards_status():
        async with SessionLocal() as s:
            total_offers = (
                await s.execute(select(func.count()).select_from(ShipyardOfferCurrent))
            ).scalar() or 0
            by_wp = (
                await s.execute(
                    select(
                        ShipyardOfferCurrent.waypoint_symbol,
                        func.count().label("offers"),
                        func.max(ShipyardOfferCurrent.observed_at).label("observed_at"),
                    ).group_by(ShipyardOfferCurrent.waypoint_symbol)
                )
            ).all()
            yards = [
                {
                    "waypoint_symbol": wp,
                    "offers": offers,
                    "observed_at": obs.isoformat() if obs else None,
                }
                for wp, offers, obs in by_wp
            ]
            return {"total_offers": total_offers, "yards": yards}

    @app.get("/summary")
    async def summary():
        loops = await rs.get_loops()
        async with SessionLocal() as s:
            ships = (await s.execute(select(func.count()).select_from(ShipCurrent))).scalar() or 0
            navs = (await s.execute(select(func.count()).select_from(FleetNav))).scalar() or 0
            markets = (
                await s.execute(select(func.count()).select_from(MarketTradeGoodCurrent))
            ).scalar() or 0
            cargo = (await s.execute(select(func.count()).select_from(ShipCargoCurrent))).scalar() or 0
            yard_offers = (
                await s.execute(select(func.count()).select_from(ShipyardOfferCurrent))
            ).scalar() or 0
        return {
            "loops": loops,
            "counts": {
                "ships_current": ships,
                "fleet_nav": navs,
                "market_trade_goods_current": markets,
                "ship_cargo_current": cargo,
                "shipyard_offers_current": yard_offers,
            },
        }

    return app


async def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    import uvicorn
    import os

    app = create_app()
    # Run server in the SAME event loop to avoid cross-loop issues
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level=os.getenv("API_LOG_LEVEL", "warning"),
        access_log=False,
        loop="asyncio",
        lifespan="on",
    )
    server = uvicorn.Server(config)
    await server.serve()
