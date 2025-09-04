from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class System(Base):
    __tablename__ = "systems"

    symbol: Mapped[str] = mapped_column(String(50), primary_key=True)
    type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    x: Mapped[int] = mapped_column(Integer)
    y: Mapped[int] = mapped_column(Integer)

    waypoints: Mapped[list["Waypoint"]] = relationship(
        "Waypoint",
        back_populates="system",
        cascade="all, delete-orphan")

class Waypoint(Base):
    __tablename__ = "waypoints"

    symbol: Mapped[str] = mapped_column(String(100), primary_key=True)
    system_symbol: Mapped[str] = mapped_column(
        ForeignKey("systems.symbol", ondelete="CASCADE"),
        index=True,
    )
    type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    x: Mapped[int] = mapped_column(Integer)
    y: Mapped[int] = mapped_column(Integer)

    system = relationship("System", back_populates="waypoints")

class FleetNav(Base):
    __tablename__ = "fleet_nav"

    ship_symbol: Mapped[str] = mapped_column(String(100), primary_key=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    flight_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Current location from nav
    system_symbol: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    waypoint_symbol: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    # Route details (if in transit)
    route_departure_system: Mapped[str | None] = mapped_column(String(50), nullable=True)
    route_departure_waypoint: Mapped[str | None] = mapped_column(String(100), nullable=True)
    route_destination_system: Mapped[str | None] = mapped_column(String(50), nullable=True)
    route_destination_waypoint: Mapped[str | None] = mapped_column(String(100), nullable=True)
    route_departure_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    route_arrival_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class MarketTradeGoodSnapshot(Base):
    __tablename__ = "market_trade_goods"

    # Composite primary key: waypoint + trade symbol + observed_at
    waypoint_symbol: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    trade_symbol: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True, index=True)

    # MarketTradeGood fields
    type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    trade_volume: Mapped[int | None] = mapped_column(Integer, nullable=True)
    supply: Mapped[str | None] = mapped_column(String(20), nullable=True)
    activity: Mapped[str | None] = mapped_column(String(20), nullable=True)
    purchase_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sell_price: Mapped[int | None] = mapped_column(Integer, nullable=True)


class MarketTradeGoodCurrent(Base):
    __tablename__ = "market_trade_goods_current"

    waypoint_symbol: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    trade_symbol: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)

    # latest observed timestamp used to determine freshness
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    trade_volume: Mapped[int | None] = mapped_column(Integer, nullable=True)
    supply: Mapped[str | None] = mapped_column(String(20), nullable=True)
    activity: Mapped[str | None] = mapped_column(String(20), nullable=True)
    purchase_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sell_price: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ShipCurrent(Base):
    __tablename__ = "ships_current"

    ship_symbol: Mapped[str] = mapped_column(String(100), primary_key=True)

    role: Mapped[str | None] = mapped_column(String(50), nullable=True)

    nav_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    flight_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    system_symbol: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    waypoint_symbol: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    fuel_current: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fuel_capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cargo_units: Mapped[int | None] = mapped_column(Integer, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ExtractionYield(Base):
    __tablename__ = "extraction_yield"

    # log each yield event
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, default=datetime.utcnow)

    ship_symbol: Mapped[str] = mapped_column(String(100), index=True)
    waypoint_symbol: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    trade_symbol: Mapped[str] = mapped_column(String(100), index=True)
    units: Mapped[int] = mapped_column(Integer)

    # cooldown context at the time of extraction/siphon
    cooldown_total_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cooldown_remaining_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cooldown_expiration: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ShipCargoCurrent(Base):
    __tablename__ = "ship_cargo_current"

    # current inventory per ship and trade symbol
    ship_symbol: Mapped[str] = mapped_column(String(100), primary_key=True)
    trade_symbol: Mapped[str] = mapped_column(String(100), primary_key=True)

    units: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("ship_symbol", "trade_symbol", name="uq_ship_cargo_current_pk"),
    )
