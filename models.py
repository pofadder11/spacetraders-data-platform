from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
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
