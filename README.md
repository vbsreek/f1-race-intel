# F1 Race Intelligence Platform

End-to-end F1 analytics: ingest session timing and telemetry, model stint performance, serve APIs and dashboards.

**Stack:** Python, PostgreSQL, Docker, FastAPI, OpenF1 / Ergast

## Quick start

```bash
# Local (API only — Postgres optional for now)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn f1_race_intel.main:app --reload --app-dir src

# With Postgres via Docker
docker compose up --build
```

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health
- Sessions (OpenF1 proxy): http://localhost:8000/api/v1/sessions?year=2024

## Project layout

```
src/f1_race_intel/
  api/       REST routes
  ingest/    ETL jobs (next milestone)
  models/    SQLAlchemy models (next milestone)
tests/
```

## Next milestones

1. SQLAlchemy models + Alembic migrations
2. OpenF1 ingest pipeline into Postgres
3. Stint/telemetry analytics endpoints
4. Dashboard or notebook layer
