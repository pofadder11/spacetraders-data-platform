from sqlalchemy import String, Integer, ForeignKey
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