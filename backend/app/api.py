from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .crud import (
    create_habit,
    delete_habit,
    get_habit,
    list_habits,
    list_records,
    update_habit,
    upsert_record,
)
from .models import Habit
from .schemas import DueItem, HabitCreate, HabitOut, HabitUpdate, RecordCreate, RecordOut
from .services.due import compute_due
from .main import get_db

router = APIRouter(prefix="/api")


def _habit_to_out(h: Habit) -> HabitOut:
    return HabitOut(
        id=h.id,
        name=h.name,
        description=h.description,
        tags=json.loads(h.tags_json),
        schedule_type=h.schedule_type,
        time_of_day=h.time_of_day,
        days_of_week=json.loads(h.days_of_week_json) if h.days_of_week_json else None,
        day_of_month=h.day_of_month,
        is_active=h.is_active,
        created_at=h.created_at,
    )


@router.get("/habits", response_model=list[HabitOut])
def api_list_habits(db: Session = Depends(get_db)):
    return [_habit_to_out(h) for h in list_habits(db)]


@router.post("/habits", response_model=HabitOut, status_code=201)
def api_create_habit(payload: HabitCreate, db: Session = Depends(get_db)):
    habit = create_habit(db, payload)
    return _habit_to_out(habit)


@router.get("/habits/{habit_id}", response_model=HabitOut)
def api_get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = get_habit(db, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return _habit_to_out(habit)


@router.patch("/habits/{habit_id}", response_model=HabitOut)
def api_update_habit(habit_id: int, payload: HabitUpdate, db: Session = Depends(get_db)):
    habit = get_habit(db, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    habit = update_habit(db, habit, payload)
    return _habit_to_out(habit)


@router.delete("/habits/{habit_id}", status_code=204)
def api_delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = get_habit(db, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    delete_habit(db, habit)


@router.get("/habits/{habit_id}/records", response_model=list[RecordOut])
def api_list_records(habit_id: int, db: Session = Depends(get_db)):
    habit = get_habit(db, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    recs = list_records(db, habit_id)
    return [
        RecordOut(
            id=r.id,
            habit_id=r.habit_id,
            due_at=r.due_at,
            recorded_at=r.recorded_at,
            status=r.status,
            reason=r.reason,
            comment=r.comment,
        )
        for r in recs
    ]


@router.post("/habits/{habit_id}/records", response_model=RecordOut, status_code=201)
def api_upsert_record(habit_id: int, payload: RecordCreate, db: Session = Depends(get_db)):
    habit = get_habit(db, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    rec = upsert_record(db, habit, payload)
    return RecordOut(
        id=rec.id,
        habit_id=rec.habit_id,
        due_at=rec.due_at,
        recorded_at=rec.recorded_at,
        status=rec.status,
        reason=rec.reason,
        comment=rec.comment,
    )


@router.get("/due", response_model=list[DueItem])
def api_due(
    window_minutes: int = Query(default=60, ge=1, le=60 * 24 * 7),
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    due = compute_due(db, now=now, window_minutes=window_minutes)
    return [DueItem(habit=_habit_to_out(h), due_at=due_at, is_overdue=is_overdue) for h, due_at, is_overdue in due]
