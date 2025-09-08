#!/usr/bin/env bash
# bootstrap_db_pkg.sh
# Creates the new DB package (session/models/repositories) and the inspector script.
set -euo pipefail

# --- 0) Ensure folders ---------------------------------------------------------
mkdir -p db
touch db/__init__.py

# --- 1) db/session.py ----------------------------------------------------------
cat > db/session.py <<'PY'
# db/session.py
from __future__ import annotations
from sqlmodel import create_engine, SQLModel

DB_URL = "sqlite:///spacetraders.db"
ENGINE = create_engine(DB_URL, echo=False)

def init_db() -> None:
    # Import models so SQLModel knows about them before create_all
    from db import models  # noqa: F401
    SQLModel.metadata.create_all(ENGINE)
PY

# --- 2) db/models.py -----------------------------------------------------------
cat > db/models.py <<'PY'
# db/models.py
from __future__ import annotations
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column, DateTime

def utcnow() -> datetime:
    # store timezone-aware UTC
    return datetime.now(timezone.utc)

class ShipsSpecsORM(SQLModel, table=True):
    __tablename__ = "ships_specs"
    symbol: str = Field(primary_key=True)
    role: Optional[str] = None
    frame_name: Optional[str] = None
    frame_module_slots: Optional[int] = None
    frame_mounting_points: Optional[int] = None
    engine_name: Optional[str] = None
    speed: Optional[int] = None
    mounts_csv: Optional[str] = None
    modules_csv: Optional[str] = None
    capacity: Optional[int] = None
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=utcnow)
    )

class ShipsActivityORM(SQLModel, table=True):
    __tablename__ = "ships_activity"
    symbol: str = Field(primary_key=True)
    status: Optional[str] = None
    flight_mode: Optional[str] = None
    cooldown_remaining_seconds: Optional[int] = None
    cooldown_expiration: Optional[datetime] = None
    cargo_units: Optional[int] = None
    cargo_capacity: Optional[int] = None
    fuel_current: Optional[int] = None
    fuel_capacity: Optional[int] = None
    condition: Optional[float] = None
    current_waypoint: Optional[str] = None
    destination_waypoint: Optional[str] = None
    fuel_level: Optional[float] = None
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=utcnow)
    )
PY

# --- 3) db/repositories.py -----------------------------------------------------
cat > db/repositories.py <<'PY'
# db/repositories.py
from __future__ import annotations
from typing import Iterable
from datetime import datetime, timezone
from sqlmodel import Session
from db.session import ENGINE
from db.models import ShipsSpecsORM, ShipsActivityORM
from domain.ships_specs import ShipsSpecs
from domain.ships_activity import ShipsActivity

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

def upsert_specs_many(items: Iterable[ShipsSpecs]) -> None:
    with Session(ENGINE) as session:
        now = _utcnow()
        for s in items:
            mounts_csv = ",".join(s.mounts) if s.mounts else None
            modules_csv = ",".join(s.modules) if s.modules else None
            row = session.get(ShipsSpecsORM, s.symbol)
            if row:
                row.role = s.role
                row.frame_name = s.frame_name
                row.frame_module_slots = s.frame_module_slots
                row.frame_mounting_points = s.frame_mounting_points
                row.engine_name = s.engine_name
                row.speed = s.speed
                row.mounts_csv = mounts_csv
                row.modules_csv = modules_csv
                row.capacity = s.capacity
                row.updated_at = now
            else:
                session.add(ShipsSpecsORM(
                    symbol=s.symbol,
                    role=s.role,
                    frame_name=s.frame_name,
                    frame_module_slots=s.frame_module_slots,
                    frame_mounting_points=s.frame_mounting_points,
                    engine_name=s.engine_name,
                    speed=s.speed,
                    mounts_csv=mounts_csv,
                    modules_csv=modules_csv,
                    capacity=s.capacity,
                    updated_at=now,
                ))
        session.commit()

def upsert_activity_many(items: Iterable[ShipsActivity]) -> None:
    with Session(ENGINE) as session:
        now = _utcnow()
        for a in items:
            row = session.get(ShipsActivityORM, a.symbol)
            if row:
                row.status = a.status
                row.flight_mode = a.flight_mode
                row.cooldown_remaining_seconds = a.cooldown_remaining_seconds
                row.cooldown_expiration = a.cooldown_expiration
                row.cargo_units = a.cargo_units
                row.cargo_capacity = a.cargo_capacity
                row.fuel_current = a.fuel_current
                row.fuel_capacity = a.fuel_capacity
                row.condition = a.condition
                row.current_waypoint = a.current_waypoint
                row.destination_waypoint = a.destination_waypoint
                row.fuel_level = a.fuel_level
                row.updated_at = now
            else:
                session.add(ShipsActivityORM(
                    symbol=a.symbol,
                    status=a.status,
                    flight_mode=a.flight_mode,
                    cooldown_remaining_seconds=a.cooldown_remaining_seconds,
                    cooldown_expiration=a.cooldown_expiration,
                    cargo_units=a.cargo_units,
                    cargo_capacity=a.cargo_capacity,
                    fuel_current=a.fuel_current,
                    fuel_capacity=a.fuel_capacity,
                    condition=a.condition,
                    current_waypoint=a.current_waypoint,
                    destination_waypoint=a.destination_waypoint,
                    fuel_level=a.fuel_level,
                    updated_at=now,
                ))
        session.commit()

def upsert_activity_one(item: ShipsActivity) -> None:
    upsert_activity_many([item])
PY

# --- 4) inspect_db.py ---------------------------------------------------------
cat > inspect_db.py <<'PY'
#!/usr/bin/env python3
# inspect_db.py
from __future__ import annotations
import sys
from typing import Optional, Any
from sqlmodel import SQLModel, Field, create_engine, Session, text

DB_URL = "sqlite:///spacetraders.db"
ENGINE = create_engine(DB_URL, echo=False)

class ShipsSpecsORM(SQLModel, table=True):
    __tablename__ = "ships_specs"
    symbol: str = Field(primary_key=True)
    role: Optional[str] = None
    frame_name: Optional[str] = None
    frame_module_slots: Optional[int] = None
    frame_mounting_points: Optional[int] = None
    engine_name: Optional[str] = None
    speed: Optional[int] = None
    mounts_csv: Optional[str] = None
    modules_csv: Optional[str] = None
    capacity: Optional[int] = None
    updated_at: Optional[str] = None  # SQLite renders datetimes as text

class ShipsActivityORM(SQLModel, table=True):
    __tablename__ = "ships_activity"
    symbol: str = Field(primary_key=True)
    status: Optional[str] = None
    flight_mode: Optional[str] = None
    cooldown_remaining_seconds: Optional[int] = None
    cooldown_expiration: Optional[str] = None
    cargo_units: Optional[int] = None
    cargo_capacity: Optional[int] = None
    fuel_current: Optional[int] = None
    fuel_capacity: Optional[int] = None
    condition: Optional[float] = None
    current_waypoint: Optional[str] = None
    destination_waypoint: Optional[str] = None
    fuel_level: Optional[float] = None
    updated_at: Optional[str] = None

def _print_table(title: str, rows: list[dict[str, Any]], cols: list[str]) -> None:
    print(f"\n=== {title} (rows={len(rows)}) ===")
    if not rows:
        print("(no rows)")
        return
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    header = " | ".join(c.ljust(widths[c]) for c in cols)
    sep = "-+-".join("-" * widths[c] for c in cols)
    print(header)
    print(sep)
    for r in rows:
        print(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))

def _recent(session: Session, table: str, limit: int, cols: list[str]) -> None:
    sql = text(f"SELECT * FROM {table} ORDER BY updated_at DESC LIMIT :lim")
    result = session.exec(sql.params(lim=limit)).all()
    rows = [{k: row[k] for k in row.keys()} for row in result]
    _print_table(table, rows, cols)

def main() -> None:
    try:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except Exception:
        limit = 10

    with Session(ENGINE) as session:
        _recent(session, "ships_activity", limit, cols=[
            "symbol","status","flight_mode","current_waypoint","destination_waypoint",
            "fuel_current","fuel_capacity","fuel_level","cargo_units","cargo_capacity",
            "cooldown_remaining_seconds","cooldown_expiration","condition","updated_at"
        ])
        _recent(session, "ships_specs", limit, cols=[
            "symbol","role","frame_name","engine_name","speed","capacity",
            "mounts_csv","modules_csv","updated_at"
        ])

if __name__ == "__main__":
    main()
PY
chmod +x inspect_db.py

# --- 5) (Optional) ensure deps in pyproject -----------------------------------
if [ -f "pyproject.toml" ]; then
  if ! grep -q 'sqlmodel' pyproject.toml; then
    echo "Updating pyproject.toml with sqlmodel dependency..."
    awk '
      BEGIN{added=0}
      {print}
      /^\[project\]/ { inproj=1 }
      inproj && /^dependencies\s*=\s*\[/ { deps=1 }
      deps && /\]/ && added==0 {
        sub(/\]/, ", \"sqlmodel\"]")
        added=1
      }
    ' pyproject.toml > pyproject.toml.tmp && mv pyproject.toml.tmp pyproject.toml || true
  fi
fi

echo "✔ DB package and inspector created."
echo "Install deps if needed:"
echo "  python -m pip install sqlmodel"
echo
echo "Run your updated runner, then inspect rows with:"
echo "  ./inspect_db.py 10"
