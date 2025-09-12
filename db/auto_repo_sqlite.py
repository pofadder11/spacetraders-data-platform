# db/auto_repo_sqlite.py
from __future__ import annotations
import sqlite3
import json
from dataclasses import dataclass
from datetime import datetime, date, time, timezone
from typing import Dict, Any, Iterable, Optional, Type, get_args, get_origin

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
    - List/Dict/Tuple/Set/... -> TEXT (JSON-encoded)
    """
    origin = get_origin(ann)
    if origin is None:
        return _SQLITE_TYPE.get(ann, "TEXT")

    # Optional[T] / Union[T, None]
    try:
        from typing import Union  # noqa
        if origin is Union:
            args = [a for a in get_args(ann) if a is not type(None)]
            base = args[0] if args else str
            return _SQLITE_TYPE.get(base, "TEXT")
    except Exception:
        pass

    # Any parametrized/collection type -> TEXT (store JSON)
    return "TEXT"

def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _to_sql_value(v: Any) -> Any:
    """
    Coerce Python values into types sqlite3 can bind.
    - primitives: as-is
    - datetime/date/time: isoformat string
    - list/tuple/set/dict: json.dumps
    - bytes: as-is
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
            # stringify non-serializable members
            def _safe(o):
                try:
                    json.dumps(o)
                    return o
                except TypeError:
                    return str(o)
            if isinstance(v, dict):
                return json.dumps({k: _safe(x) for k, x in v.items()})
            return json.dumps([_safe(x) for x in v])
    return str(v)

@dataclass
class TableSpec:
    table: str
    pk: Union[str, Tuple[str, ...]] = "symbol"  # NEW: allow composite PK
    add_updated_at: bool = True  # maintain an updated_at column

def ensure_table_for_domain(
    conn: sqlite3.Connection,
    model_cls: Type[Any],
    spec: TableSpec,
    *,
    extra_columns: Optional[Dict[str, Any]] = None,   # NEW: add columns not in the model (e.g., observed_at)
) -> None:
    """
    Create/extend a table with columns for all model fields (snake_case),
    plus updated_at (TEXT) if requested. Existing columns are preserved.

    - Supports composite primary keys via TableSpec.pk = (col1, col2, ...)
    - `extra_columns` lets you add fields not present on the model (e.g., observed_at for snapshots).
    """
    cur = conn.cursor()

    # Current columns
    cur.execute(f"PRAGMA table_info({spec.table})")
    existing = {row[1] for row in cur.fetchall()}  # column name at index 1

    # Merge model annotations + extra_columns
    annotations = dict(getattr(model_cls, "__annotations__", {}))
    if extra_columns:
        for k, v in extra_columns.items():
            annotations.setdefault(k, v)

    cols_to_add = []

    # Determine PK (single or composite)
    pk_cols: Tuple[str, ...]
    if isinstance(spec.pk, tuple):
        pk_cols = spec.pk
    else:
        pk_cols = (spec.pk,)

    # For new table, collect column defs (without inline PK unless single-pk and new table)
    for name, ann in annotations.items():
        if name in existing:
            continue
        coltype = _py_to_sqlite(ann)
        cols_to_add.append(f"{name} {coltype}")

    # updated_at (if requested)
    if spec.add_updated_at and "updated_at" not in existing:
        cols_to_add.append("updated_at TEXT")

    if not existing:
        # Create fresh table
        # Ensure all PK columns exist in annotations/extra
        for col in pk_cols:
            if col not in annotations and not (spec.add_updated_at and col == "updated_at"):
                raise ValueError(f"Primary key column '{col}' not found in model fields or extra_columns.")

        ddl_cols = ", ".join(cols_to_add)

        # Inline PK if single column and present; else composite PK table constraint
        if len(pk_cols) == 1 and pk_cols[0] in annotations:
            # add PRIMARY KEY inline by reconstructing that column’s def
            parts = []
            for name, ann in annotations.items():
                coldef = f"{name} {_py_to_sqlite(ann)}"
                if name == pk_cols[0]:
                    coldef += " PRIMARY KEY"
                parts.append(coldef)
            if spec.add_updated_at:
                parts.append("updated_at TEXT")
            ddl = ", ".join(parts)
        else:
            # use composite PK constraint
            ddl = ddl_cols + f", PRIMARY KEY({', '.join(pk_cols)})"

        cur.execute(f"CREATE TABLE IF NOT EXISTS {spec.table} ({ddl})")
    else:
        # Add missing columns
        for coldef in cols_to_add:
            cur.execute(f"ALTER TABLE {spec.table} ADD COLUMN {coldef}")

        # NOTE: cannot add/change primary key on an existing SQLite table without rebuild.

    conn.commit()

def upsert_many(conn: sqlite3.Connection, spec: TableSpec, models: Iterable[Any]) -> None:
    """
    Upsert any number of Pydantic domain model instances into the table,
    serializing non-primitive fields automatically.

    IMPORTANT:
    - Columns are derived from the model class annotations (DRY),
      not from the first instance's dump (which may omit None fields).
    - Performs INSERT OR REPLACE (row-level last-write-wins) keyed by `spec.pk`.
    """
    models = list(models)
    if not models:
        return

    model_cls = type(models[0])

    # Ensure table exists with all annotated columns
    ensure_table_for_domain(conn, model_cls, spec)

    # Full column list from annotations (stable order)
    ann_cols = list(getattr(model_cls, "__annotations__", {}).keys())
    cols = ann_cols.copy()
    if spec.add_updated_at and "updated_at" not in cols:
        cols.append("updated_at")

    placeholders = ", ".join(["?"] * len(cols))
    colnames = ", ".join(cols)
    sql = f"INSERT OR REPLACE INTO {spec.table} ({colnames}) VALUES ({placeholders})"

    cur = conn.cursor()
    for m in models:
        data = m.model_dump(mode="python")  # may omit None; we .get(...)
        if spec.add_updated_at:
            data["updated_at"] = _utcnow_iso()
        vals = [_to_sql_value(data.get(c)) for c in cols]
        cur.execute(sql, vals)

    conn.commit()

def upsert_many_with_extra(
    conn: sqlite3.Connection,
    spec: TableSpec,
    models: Iterable[Any],
    *,
    extra_columns: Optional[Dict[str, Any]] = None,  # name -> python type (for table creation)
    extra_values: Optional[Dict[str, Any]] = None,   # name -> value (merged into every row)
) -> None:
    """
    Like upsert_many, but also:
      - ensures `extra_columns` exist on the table (types used for DDL),
      - merges `extra_values` into each row on write (e.g., observed_at timestamp).
    """
    models = list(models)
    if not models:
        return

    model_cls = type(models[0])

    # Ensure table exists with all annotated + extra columns
    ensure_table_for_domain(conn, model_cls, spec, extra_columns=extra_columns)

    # Build stable column list from merged annotations
    annotations = dict(getattr(model_cls, "__annotations__", {}))
    if extra_columns:
        # preserve insertion order: model columns first, then extras in provided order
        for k, v in extra_columns.items():
            if k not in annotations:
                annotations[k] = v

    cols = list(annotations.keys())
    if spec.add_updated_at and "updated_at" not in cols:
        cols.append("updated_at")

    placeholders = ", ".join(["?"] * len(cols))
    colnames = ", ".join(cols)
    sql = f"INSERT OR REPLACE INTO {spec.table} ({colnames}) VALUES ({placeholders})"

    cur = conn.cursor()
    for m in models:
        data = m.model_dump(mode="python")
        if extra_values:
            data.update(extra_values)
        if spec.add_updated_at:
            data["updated_at"] = _utcnow_iso()
        vals = [_to_sql_value(data.get(c)) for c in cols]
        cur.execute(sql, vals)

    conn.commit()

def snapshot_many(
    conn: sqlite3.Connection,
    base_table: str,
    model_cls: Type[Any],
    models: Iterable[Any],
    *,
    ts_col: str = "observed_at",
    pk_field: str = "id",
    observed_at: Optional[datetime] = None,
) -> None:
    """
    Append-only snapshots: writes rows into `{base_table}_snapshots` with composite
    PK of (pk_field, ts_col). Adds a timestamp column on the fly.

    Example:
      snapshot_many(conn, "market_goods", MarketGoodRow, rows["goods"])
    """
    when = observed_at or datetime.now(timezone.utc)
    spec = TableSpec(
        table=f"{base_table}_snapshots",
        pk=(pk_field, ts_col),            # composite PK => no overwrite across time
        add_updated_at=True,
    )
    upsert_many_with_extra(
        conn,
        spec,
        models,
        extra_columns={ts_col: datetime}, # ensure the column exists (TEXT in SQLite)
        extra_values={ts_col: when},      # set the same timestamp for this scrape
    )
