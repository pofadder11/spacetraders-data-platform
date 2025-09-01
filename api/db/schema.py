from pathlib import Path


def ensure_schema(conn, schema_path="api/db/schema.sql"):
    """Run schema.sql to ensure all tables exist."""
    with open(Path(schema_path), "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cur = conn.cursor()
    cur.executescript(schema_sql)  # executes multiple statements
    conn.commit()
    cur.close()
