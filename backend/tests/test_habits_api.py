from __future__ import annotations

from datetime import datetime, timezone


def test_habit_crud(client):
    payload = {
        "name": "Read",
        "description": "Read 10 pages",
        "tags": ["health", "mind"],
        "schedule_type": "daily",
        "time_of_day": "20:30",
        "is_active": True,
    }

    r = client.post("/api/habits", json=payload)
    assert r.status_code == 201
    habit = r.json()
    assert habit["id"] > 0
    assert habit["name"] == "Read"
    assert habit["tags"] == ["health", "mind"]

    r = client.get("/api/habits")
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.patch(f"/api/habits/{habit['id']}", json={"name": "Read (evening)", "tags": ["mind"]})
    assert r.status_code == 200
    updated = r.json()
    assert updated["name"] == "Read (evening)"
    assert updated["tags"] == ["mind"]

    r = client.delete(f"/api/habits/{habit['id']}")
    assert r.status_code == 204

    r = client.get("/api/habits")
    assert r.status_code == 200
    assert r.json() == []
