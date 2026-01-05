from __future__ import annotations

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import SessionDependency, create_app
from app.db import create_sessionmaker, create_sqlite_engine
from app.models import Base


@pytest.fixture()
def client():
    engine = create_sqlite_engine("sqlite+pysqlite:///:memory:")
    SessionLocal = create_sessionmaker(engine)
    Base.metadata.create_all(bind=engine)

    app = create_app()

    def _get_session():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[SessionDependency] = _get_session

    with TestClient(app) as c:
        yield c
