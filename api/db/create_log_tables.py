import sqlite3


def create_log_tables(conn: sqlite3.Connection):
    """
    Creates log tables for all existing tables in the database.
    Each log table mirrors the table's columns + an extra 'timestamp' column.
    Skips tables that are already log tables.
    """
    cursor = conn.cursor()

    # Get all user tables (skip sqlite internal tables)
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    tables = [row[0] for row in cursor.fetchall()]

    for table_name in tables:
        # Skip tables that are already logs
        if table_name.endswith("_log"):
            continue

        log_table = f"{table_name}_log"

        # Get column names of the current table
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns = [row[1] for row in cursor.fetchall()]  # extract column names
        columns = [
            col for col in columns if col != "timestamp"
        ]  # remove timestamp if present

        # Build column definitions for log table, all as TEXT
        col_defs = ", ".join([f'"{col}" TEXT' for col in columns])
        sql = f"""
        CREATE TABLE IF NOT EXISTS "{log_table}" (
            {col_defs},
            "timestamp" TEXT
        )
        """
        cursor.execute(sql)
        print(f"[INFO] Created log table: {log_table}")

    conn.commit()
