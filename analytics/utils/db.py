import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parents[1] / "spacetraders.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def query_df(sql: str, params: tuple = ()) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql(sql, conn, params=params)
