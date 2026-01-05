from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router
from .db import create_sessionmaker, create_sqlite_engine
from .models import Base
from .settings import get_settings

settings = get_settings()
engine = create_sqlite_engine(settings.database_url)
SessionLocal = create_sessionmaker(engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_app() -> FastAPI:
    app = FastAPI(title="LifeTracker API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/health")
    def health():
        return {"ok": True}

    return app


app = create_app()
