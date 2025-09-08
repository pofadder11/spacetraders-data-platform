# db/auto_repo_sqlite.py
from __future__ import annotations
import sqlite3
import json
from dataclasses import dataclass
from datetime import datetime, date, time, timezone
from typing import Any, Iterable, Type, get_args, get_origin

# ---- Python -> SQLite column type mapping (coarse) ---------------------------
_SQLITE_TYPE = {
    int: "INTEGER",
    float: "REAL",
    bool: "INTEGER",
    str: "TEXT",
    bytes: "BLOB",
    datetime: "TEXT",  # stored as ISO-8601 strings
    date: "TEXT",
    time: "TEXT",
}

def _py_to_sqlite(ann: Any) -> str:
    """
    Map a typing annotation to an SQLite column type.
    - Optional[T] / Union[T, None] -> T
    - List/Dict/... -> TEXT (JSON-encoded)
    """
    origin = get_origin(ann)
    if origin is None:
        return _SQLITE_TYPE.get(ann, "TEXT")

    # Handle Optional[T] / Union[T, None]
    if origin is type(None):
        return "TEXT"

    # typing.Union / PEP604 union (T | None)
    try:
        from typing import Union  # noqa
        if origin is Union:
            args = [a for a in get_args(ann) if a is not type(None)]
            base = args[0] if args else str
            return _SQLITE_TYPE.get(base, "TEXT")
    except Exception:
        pass

    # Lists, Dicts, Tuples etc -> store as JSON string
    return "TEXT"

def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _to_sql_value(v: Any) -> Any:
    """
    Coerce Python values into something sqlite3 can bind.
    - primitives: keep as-is
    - datetime/date/time: isoformat string
    - list/tuple/set/dict: json.dumps
    - bytes: keep as-is
    - everything else: str()
    """
    if v is None:
        return None
    if isinstance(v, (int, float, str, bool, bytes)):
        return v
    if isinstance(v, (datetime, date, time)):
        return v.isoformat()
    if isinstance(v, (list, tuple, set, dict)):
        try:
            return json.dumps(v)
        except TypeError:
            def _safe(o):
                try:
                    json.dumps(o)
                    return o
                except TypeError:
                    return str(o)
            if isinstance(v, dict):
                return json.dumps({k: _safe(x) for k, x in v.items()})
            else:
                return json.dumps([_safe(x) for x in v])
    return str(v)

@dataclass
class TableSpec:
    table: str
    pk: str = "symbol"
    add_updated_at: bool = True  # maintain an updated_at column

def ensure_table_for_domain(conn: sqlite3.Connection, model_cls: Type[Any], spec: TableSpec) -> None:
    """
    Create/extend a table with columns for all model fields (snake_case),
    plus updated_at (TEXT) if requested. Existing columns are preserved.
    """
    cur = conn.cursor()

    # Current columns
    cur.execute(f"PRAGMA table_info({spec.table})")
    existing = {row[1] for row in cur.fetchall()}  # column name at index 1

    annotations = getattr(model_cls, "__annotations__", {})
    cols_to_add = []

    for name, ann in annotations.items():
        if name in existing:
            continue
        coltype = _py_to_sqlite(ann)
        coldef = f"{name} {coltype}"
        if name == spec.pk and not existing:
            coldef += " PRIMARY KEY"
        cols_to_add.append(coldef)

    # updated_at
    if spec.add_updated_at and "updated_at" not in existing:
        cols_to_add.append("updated_at TEXT")

    if not existing:
        # Create fresh table
        if spec.pk not in annotations:
            raise ValueError(f"Primary key '{spec.pk}' not found in model fields.")
        ddl = ", ".join(cols_to_add)
        cur.execute(f"CREATE TABLE IF NOT EXISTS {spec.table} ({ddl})")
    else:
        # Add missing columns
        for coldef in cols_to_add:
            cur.execute(f"ALTER TABLE {spec.table} ADD COLUMN {coldef}")

    conn.commit()

def upsert_many(conn: sqlite3.Connection, spec: TableSpec, models: Iterable[Any]) -> None:
    """
    Upsert any number of Pydantic domain model instances into the table,
    serializing non-primitive fields automatically.
    IMPORTANT: Columns are derived from the model class annotations (DRY),
    not from the first instance's dump (which may omit None fields).
    """
    models = list(models)
    if not models:
        return

    model_cls = type(models[0])

    # Ensure table exists with all annotated columns
    ensure_table_for_domain(conn, model_cls, spec)

    # Build the full column list from annotations
    ann_cols = list(getattr(model_cls, "__annotations__", {}).keys())
    cols = ann_cols.copy()
    if spec.add_updated_at and "updated_at" not in cols:
        cols.append("updated_at")

    placeholders = ", ".join(["?"] * len(cols))
    colnames = ", ".join(cols)
    sql = f"INSERT OR REPLACE INTO {spec.table} ({colnames}) VALUES ({placeholders})"

    cur = conn.cursor()
    for m in models:
        data = m.model_dump(mode="python")  # may omit None, so use .get below
        if spec.add_updated_at:
            data["updated_at"] = _utcnow_iso()
        vals = [_to_sql_value(data.get(c)) for c in cols]
        cur.execute(sql, vals)

    conn.commit()
