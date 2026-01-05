from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator


def _validate_hhmm(value: str) -> str:
    if not re.fullmatch(r"\d{2}:\d{2}", value):
        raise ValueError("time_of_day must be HH:MM")
    hh, mm = value.split(":")
    if not (0 <= int(hh) <= 23 and 0 <= int(mm) <= 59):
        raise ValueError("time_of_day must be a valid time")
    return value


class HabitBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    tags: list[str] = Field(default_factory=list)

    schedule_type: Literal["daily", "weekly", "monthly"]
    time_of_day: str

    days_of_week: list[int] | None = None
    day_of_month: int | None = None

    is_active: bool = True

    _validate_time = field_validator("time_of_day")(_validate_hhmm)

    @field_validator("days_of_week")
    @classmethod
    def _validate_days_of_week(cls, v):
        if v is None:
            return v
        if any(d < 0 or d > 6 for d in v):
            raise ValueError("days_of_week values must be between 0 and 6")
        # De-dup + stable
        return sorted(set(v))

    @field_validator("day_of_month")
    @classmethod
    def _validate_day_of_month(cls, v):
        if v is None:
            return v
        if v < 1 or v > 31:
            raise ValueError("day_of_month must be between 1 and 31")
        return v


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    tags: list[str] | None = None

    schedule_type: Literal["daily", "weekly", "monthly"] | None = None
    time_of_day: str | None = None

    days_of_week: list[int] | None = None
    day_of_month: int | None = None

    is_active: bool | None = None

    _validate_time = field_validator("time_of_day")(_validate_hhmm)


class HabitOut(HabitBase):
    id: int
    created_at: datetime


class RecordCreate(BaseModel):
    due_at: datetime
    status: Literal["done", "not_done"]
    reason: str | None = None
    comment: str | None = None


class RecordOut(BaseModel):
    id: int
    habit_id: int
    due_at: datetime
    recorded_at: datetime
    status: str
    reason: str | None
    comment: str | None


class DueItem(BaseModel):
    habit: HabitOut
    due_at: datetime
    is_overdue: bool
