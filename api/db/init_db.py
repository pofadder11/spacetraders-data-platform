import sqlite3


def init_db(db_path: str = "spacetraders.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Load schema from external file
    with open("api/db/schema.sql", "r") as f:
        cur.executescript(f.read())

    conn.commit()
    return conn
