from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ScheduleType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"  # One or more weekdays
    MONTHLY = "monthly"  # Day-of-month


class RecordStatus(str, Enum):
    DONE = "done"
    NOT_DONE = "not_done"


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Stored as JSON in text (client sends list[str])
    tags_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")

    schedule_type: Mapped[str] = mapped_column(String(20), nullable=False)
    time_of_day: Mapped[str] = mapped_column(String(5), nullable=False)  # HH:MM

    # Stored as JSON list[int] (0=Mon..6=Sun)
    days_of_week_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 1..31 for monthly schedules
    day_of_month: Mapped[int | None] = mapped_column(Integer, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    records: Mapped[list[HabitRecord]] = relationship(
        "HabitRecord",
        back_populates="habit",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class HabitRecord(Base):
    __tablename__ = "habit_records"
    __table_args__ = (UniqueConstraint("habit_id", "due_at", name="uq_habit_due"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)

    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    habit: Mapped[Habit] = relationship("Habit", back_populates="records")
