from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Habit, HabitRecord


def _parse_hhmm(value: str) -> time:
    hh, mm = value.split(":")
    return time(hour=int(hh), minute=int(mm), tzinfo=timezone.utc)


def _dates_between(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur = cur + timedelta(days=1)


def _matches_schedule(habit: Habit, d: date) -> bool:
    if habit.schedule_type == "daily":
        return True

    if habit.schedule_type == "weekly":
        if habit.days_of_week_json is None:
            return False
        days = json.loads(habit.days_of_week_json)
        # Python date.weekday(): Mon=0..Sun=6
        return d.weekday() in days

    if habit.schedule_type == "monthly":
        if habit.day_of_month is None:
            return False
        return d.day == habit.day_of_month

    return False


def _candidate_due_ats(habit: Habit, now: datetime, window_minutes: int) -> list[datetime]:
    start = (now - timedelta(days=1)).date()
    end = (now + timedelta(minutes=window_minutes) + timedelta(days=1)).date()

    t = _parse_hhmm(habit.time_of_day)
    out: list[datetime] = []

    for d in _dates_between(start, end):
        if not _matches_schedule(habit, d):
            continue
        due_at = datetime.combine(d, t)
        # keep as timezone-aware UTC
        out.append(due_at)

    return out


def compute_due(db: Session, now: datetime, window_minutes: int) -> list[tuple[Habit, datetime, bool]]:
    now = now.astimezone(timezone.utc)
    stmt = select(Habit).where(Habit.is_active.is_(True)).order_by(Habit.id)
    habits = list(db.scalars(stmt))

    # Pull relevant records once
    window_end = now + timedelta(minutes=window_minutes)
    record_stmt = select(HabitRecord).where(HabitRecord.due_at <= window_end)
    records = list(db.scalars(record_stmt))
    recorded = {(r.habit_id, r.due_at): r for r in records}

    due_items: list[tuple[Habit, datetime, bool]] = []

    for habit in habits:
        for due_at in _candidate_due_ats(habit, now, window_minutes):
            if due_at > window_end:
                continue
            if (habit.id, due_at) in recorded:
                continue

            is_overdue = due_at < now
            # Only surface items that are due/overdue now or within the requested window.
            if due_at <= window_end:
                due_items.append((habit, due_at, is_overdue))

    due_items.sort(key=lambda x: x[1])
    return due_items
