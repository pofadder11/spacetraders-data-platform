def create_log_tables(conn, table_schemas: dict):
    """
    Creates log tables for each table in table_schemas.
    Each log table mirrors the schema + an extra 'timestamp' column.
    """
    cursor = conn.cursor()

    for table_name, columns in table_schemas.items():
        log_table = f"{table_name}_log"

        # Build column definitions, quoting names
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
