from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from config.settings import settings
from models import Base  # reuse existing ORM models
from sqlalchemy import text


engine = create_async_engine(settings.database_url, echo=False, future=True)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)


async def init_db_async() -> None:
    await check_db_connection_async()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def check_db_connection_async() -> None:
    """Try connecting to the database and raise a helpful error if unreachable."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        msg = (
            "Could not connect to PostgreSQL.\n"
            f"DATABASE_URL={settings.database_url}\n"
            "Checklist:\n"
            "- Is PostgreSQL running and listening on the host/port?\n"
            "- Are user/password correct and allowed in pg_hba.conf?\n"
            "- Can you connect with psql using the same credentials?\n"
            "- If using Docker: did you publish the port and use the right host?\n"
        )
        raise RuntimeError(msg) from e
