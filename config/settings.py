from __future__ import annotations

import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    bearer_token: str
    database_url: str

    @staticmethod
    def load_env() -> "Settings":
        load_dotenv()
        token = os.getenv("BEARER_TOKEN")
        if not token:
            raise RuntimeError("Missing BEARER_TOKEN in environment")
        db_url = os.getenv("DATABASE_URL") or "postgresql+asyncpg://postgres:postgres@localhost:5432/spacetraders"
        return Settings(bearer_token=token, database_url=db_url)


settings = Settings.load_env()

