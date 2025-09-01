import sqlite3

from api.db.create_log_tables import create_log_tables


def init_db(db_path: str = "spacetraders.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Load schema from external file
    with open("api/db/schema.sql", "r") as f:
        cur.executescript(f.read())

    # Create log tables (idempotent)
    create_log_tables(conn)
    conn.commit()
    return conn
