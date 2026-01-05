from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router
from .db import create_sessionmaker, create_sqlite_engine, get_session_factory
from .models import Base
from .settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    engine = create_sqlite_engine(settings.database_url)
    SessionLocal = create_sessionmaker(engine)

    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="LifeTracker API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"] ,
        allow_headers=["*"],
    )

    get_session = get_session_factory(SessionLocal)

    # Dependency override point for tests.
    app.dependency_overrides[Depends] = None  # no-op; explicit overrides are set in tests

    # Bind Session dependency: using `Depends()` in routes expects this exact callable.
    app.dependency_overrides[SessionDependency] = get_session  # type: ignore[name-defined]

    app.include_router(router)

    @app.get("/health")
    def health():
        return {"ok": True}

    return app


# A tiny trick to keep routes simple: they use `db: Session = Depends()`.
# We override this dependency by referencing this symbol.

def SessionDependency():  # pragma: no cover
    raise RuntimeError("Session dependency not configured")


app = create_app()
