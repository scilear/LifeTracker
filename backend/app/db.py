from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


def create_sqlite_engine(database_url: str):
    # For file-based SQLite, `check_same_thread=False` allows use across threads.
    connect_args = {"check_same_thread": False}

    # For in-memory SQLite, StaticPool is required to keep the DB alive across sessions.
    if database_url.endswith(":memory:"):
        return create_engine(
            database_url,
            connect_args=connect_args,
            poolclass=StaticPool,
            future=True,
        )

    return create_engine(database_url, connect_args=connect_args, future=True)


def create_sessionmaker(engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session_factory(SessionLocal: sessionmaker[Session]):
    def _get_session() -> Generator[Session, None, None]:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    return _get_session
