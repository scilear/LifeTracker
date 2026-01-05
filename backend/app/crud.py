from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Habit, HabitRecord
from .schemas import HabitCreate, HabitUpdate, RecordCreate


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def create_habit(db: Session, payload: HabitCreate) -> Habit:
    habit = Habit(
        name=payload.name,
        description=payload.description,
        tags_json=json.dumps(payload.tags),
        schedule_type=payload.schedule_type,
        time_of_day=payload.time_of_day,
        days_of_week_json=json.dumps(payload.days_of_week) if payload.days_of_week is not None else None,
        day_of_month=payload.day_of_month,
        is_active=payload.is_active,
        created_at=_utcnow(),
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


def list_habits(db: Session) -> list[Habit]:
    return list(db.scalars(select(Habit).order_by(Habit.id)))


def get_habit(db: Session, habit_id: int) -> Habit | None:
    return db.get(Habit, habit_id)


def update_habit(db: Session, habit: Habit, payload: HabitUpdate) -> Habit:
    data = payload.model_dump(exclude_unset=True)

    if "tags" in data and data["tags"] is not None:
        habit.tags_json = json.dumps(data.pop("tags"))

    if "days_of_week" in data:
        dow = data.pop("days_of_week")
        habit.days_of_week_json = json.dumps(dow) if dow is not None else None

    for k, v in data.items():
        setattr(habit, k, v)

    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


def delete_habit(db: Session, habit: Habit) -> None:
    db.delete(habit)
    db.commit()


def list_records(db: Session, habit_id: int) -> list[HabitRecord]:
    stmt = select(HabitRecord).where(HabitRecord.habit_id == habit_id).order_by(HabitRecord.due_at.desc())
    return list(db.scalars(stmt))


def upsert_record(db: Session, habit: Habit, payload: RecordCreate) -> HabitRecord:
    stmt = select(HabitRecord).where(
        HabitRecord.habit_id == habit.id,
        HabitRecord.due_at == payload.due_at,
    )
    existing = db.scalars(stmt).first()

    if existing is None:
        rec = HabitRecord(
            habit_id=habit.id,
            due_at=payload.due_at,
            recorded_at=_utcnow(),
            status=payload.status,
            reason=payload.reason,
            comment=payload.comment,
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec

    existing.recorded_at = _utcnow()
    existing.status = payload.status
    existing.reason = payload.reason
    existing.comment = payload.comment

    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing
