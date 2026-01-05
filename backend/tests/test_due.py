from __future__ import annotations

from datetime import datetime, timezone


def test_due_daily_and_recording(client):
    # Create a daily habit due at 10:00 UTC
    habit = client.post(
        "/api/habits",
        json={
            "name": "Water",
            "tags": [],
            "schedule_type": "daily",
            "time_of_day": "10:00",
            "is_active": True,
        },
    ).json()

    # Fetch due: should include today's 10:00 slot if within window.
    # Use a large window so it's deterministic.
    due = client.get("/api/due?window_minutes=10080").json()
    assert any(item["habit"]["id"] == habit["id"] for item in due)

    # Pick the earliest due occurrence for this habit.
    item = sorted([i for i in due if i["habit"]["id"] == habit["id"]], key=lambda x: x["due_at"])[0]
    due_at = item["due_at"]

    # Record it as done.
    rec = client.post(
        f"/api/habits/{habit['id']}/records",
        json={"due_at": due_at, "status": "done", "comment": "ok"},
    )
    assert rec.status_code == 201

    # Due list should no longer contain that exact due_at.
    due2 = client.get("/api/due?window_minutes=10080").json()
    assert not any(
        i["habit"]["id"] == habit["id"] and i["due_at"] == due_at
        for i in due2
    )


def test_weekly_schedule_filters_days(client):
    # Weekly on Monday only (0)
    habit = client.post(
        "/api/habits",
        json={
            "name": "Gym",
            "tags": ["sport"],
            "schedule_type": "weekly",
            "days_of_week": [0],
            "time_of_day": "07:00",
            "is_active": True,
        },
    ).json()

    due = client.get("/api/due?window_minutes=10080").json()
    items = [i for i in due if i["habit"]["id"] == habit["id"]]
    assert items, "Expected at least one due occurrence within 7 days"
