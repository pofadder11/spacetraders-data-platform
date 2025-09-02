import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base # important: imports models so Base knows all tables

def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///spacetraders.db")

engine = create_engine(get_database_url(), future=True, connect_args={"check_same_thread": False} if "sqlite" in get_database_url() else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db() -> None:
    Base.metadata.create_all(engine)