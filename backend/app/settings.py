from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_allow_origins: list[str]


def get_settings() -> Settings:
    database_url = os.getenv("LIFETRACKER_DATABASE_URL", "sqlite:///./lifetracker.db")
    cors = os.getenv("LIFETRACKER_CORS_ALLOW_ORIGINS", "http://localhost:5173")
    cors_allow_origins = [o.strip() for o in cors.split(",") if o.strip()]
    return Settings(database_url=database_url, cors_allow_origins=cors_allow_origins)
