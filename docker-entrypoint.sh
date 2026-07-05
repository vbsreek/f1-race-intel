#!/bin/sh
set -e
alembic upgrade head
exec uvicorn f1_race_intel.main:app --host 0.0.0.0 --port 8000 --app-dir src
