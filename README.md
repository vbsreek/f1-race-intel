# F1 Race Intelligence Platform

End-to-end F1 analytics: ingest session timing and telemetry, model stint performance, serve APIs and dashboards.

**Stack:** Python, PostgreSQL, Docker, FastAPI, OpenF1

## Quick start

```bash
# Local with Postgres (recommended)
docker compose up --build

# Or API + Postgres manually
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
docker compose up db -d
uvicorn f1_race_intel.main:app --reload --app-dir src
```

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

## Ingest data

Pull a session from OpenF1 into Postgres:

```bash
# CLI — pass any OpenF1 session_key
f1-ingest <session_key>

# Or via API
curl -X POST http://localhost:8000/api/v1/ingest/sessions/<session_key>
curl -X POST "http://localhost:8000/api/v1/ingest/sync?year=2024&session_type=Race&limit=3"
```

## API overview

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/openf1/sessions` | Live OpenF1 session list (proxy) |
| `GET /api/v1/sessions` | Persisted sessions from Postgres |
| `GET /api/v1/sessions/{key}/drivers` | Drivers for a session |
| `GET /api/v1/sessions/{key}/stints` | Stint data |
| `GET /api/v1/sessions/{key}/analytics/stints` | Stint pace summary (avg/best lap) |
| `POST /api/v1/ingest/sessions/{key}` | Ingest one session |
| `POST /api/v1/ingest/sync` | Bulk ingest recent sessions |

## Project layout

```
src/f1_race_intel/
  api/         REST routes and schemas
  data/        OpenF1 client, repositories, and services
    openf1/    Typed API schemas, client, and ORM mappers
    repositories/
    services/
  analytics/   Stint pace calculations (via data layer)
  models/      SQLAlchemy ORM models
alembic/       Database migrations
tests/
```

## Migrations

Migrations run automatically when starting via Docker Compose. To run manually:

```bash
alembic upgrade head
```

## Next milestones

1. Telemetry (car_data) ingest and sector traces
2. Strategy comparison dashboard
3. Notebook examples for race analysis
