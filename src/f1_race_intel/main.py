from contextlib import asynccontextmanager

from fastapi import FastAPI

from f1_race_intel.api.routes import router
from f1_race_intel.config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(
    title="F1 Race Intelligence",
    description="Session timing, telemetry ingest, and stint analytics APIs.",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "service": "f1-race-intel",
        "docs": "/docs",
        "health": "/api/v1/health",
        "openf1": settings.openf1_base_url,
    }
