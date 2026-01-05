from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.db import create_sessionmaker, create_sqlite_engine
from app.main import create_app, get_db
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

    app.dependency_overrides[get_db] = _get_session

    with TestClient(app) as c:
        yield c
