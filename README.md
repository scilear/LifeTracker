# LifeTracker

A lightweight, browser-based habit/action tracker with due prompts, reasons for misses, and optional comments.

## What’s included

- Vue 3 + Vue Router frontend (polls for due habits and can show browser notifications).
- FastAPI + SQLAlchemy backend with a SQLite database.
- Pytest suite (TDD-focused) covering schedules, due detection, and core API flows.

## Quick start (dev)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend will create a local SQLite DB at `backend/lifetracker.db` by default.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (typically `http://localhost:5173`).

## Browser notifications

Notifications require explicit user permission.
Use **Settings → Enable notifications**, then keep the app open to receive due prompts.

## Running tests

```bash
cd backend
pytest
```
