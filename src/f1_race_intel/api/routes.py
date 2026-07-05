from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from f1_race_intel.api.deps import (
    get_analytics_service,
    get_ingest_service,
    get_openf1_client,
    get_race_data_repo,
    get_session_service,
)
from f1_race_intel.api.schemas import (
    DriverOut,
    HealthOut,
    IngestResult,
    SessionOut,
    StintAnalyticsOut,
    StintOut,
)
from f1_race_intel.data import OpenF1Client, RaceDataRepository
from f1_race_intel.data.services import AnalyticsService, IngestService, SessionNotFoundError, SessionService

router = APIRouter()


@router.get("/health", response_model=HealthOut)
async def health(repo: Annotated[RaceDataRepository, Depends(get_race_data_repo)]) -> HealthOut:
    try:
        repo.ping()
        db_status = "ok"
    except Exception:
        db_status = "unavailable"
    return HealthOut(status="ok", database=db_status)


@router.get("/openf1/sessions", response_model=list[SessionOut])
async def list_openf1_sessions(
    openf1: Annotated[OpenF1Client, Depends(get_openf1_client)],
    year: int | None = None,
    session_type: str | None = None,
) -> list[SessionOut]:
    """Live sessions from OpenF1 (not persisted)."""
    try:
        sessions = await openf1.list_sessions(year=year, session_type=session_type)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenF1 request failed: {exc}") from exc
    return [SessionOut.model_validate(session.model_dump()) for session in sessions]


@router.get("/sessions", response_model=list[SessionOut])
def list_sessions(
    service: Annotated[SessionService, Depends(get_session_service)],
    year: int | None = None,
    session_type: str | None = None,
    limit: int = Query(default=50, le=200),
) -> list[SessionOut]:
    return service.list_sessions(year=year, session_type=session_type, limit=limit)


@router.get("/sessions/{session_key}", response_model=SessionOut)
def get_session(
    session_key: int,
    service: Annotated[SessionService, Depends(get_session_service)],
) -> SessionOut:
    try:
        return service.get_session(session_key)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/sessions/{session_key}/drivers", response_model=list[DriverOut])
def list_drivers(
    session_key: int,
    service: Annotated[SessionService, Depends(get_session_service)],
) -> list[DriverOut]:
    try:
        return service.get_drivers(session_key)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/sessions/{session_key}/stints", response_model=list[StintOut])
def list_stints(
    session_key: int,
    service: Annotated[SessionService, Depends(get_session_service)],
) -> list[StintOut]:
    try:
        return service.get_stints(session_key)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/sessions/{session_key}/analytics/stints", response_model=list[StintAnalyticsOut])
def get_stint_analytics(
    session_key: int,
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
) -> list[StintAnalyticsOut]:
    try:
        return service.stint_summary(session_key)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/ingest/sessions/{session_key}", response_model=IngestResult)
async def ingest_one_session(
    session_key: int,
    service: Annotated[IngestService, Depends(get_ingest_service)],
    include_laps: bool = True,
) -> IngestResult:
    try:
        counts = await service.ingest_session(session_key, include_laps=include_laps)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Ingest failed: {exc}") from exc
    return IngestResult(
        session_key=counts.session_key,
        drivers=counts.drivers,
        stints=counts.stints,
        laps=counts.laps,
    )


@router.post("/ingest/sync", response_model=list[IngestResult])
async def sync_sessions(
    service: Annotated[IngestService, Depends(get_ingest_service)],
    year: int | None = None,
    session_type: str | None = None,
    limit: int = Query(default=5, le=20),
    include_laps: bool = True,
) -> list[IngestResult]:
    """Fetch session list from OpenF1 and ingest the most recent ones."""
    try:
        results = await service.sync_sessions(
            year=year,
            session_type=session_type,
            limit=limit,
            include_laps=include_laps,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Ingest sync failed: {exc}") from exc
    return [
        IngestResult(
            session_key=row.session_key,
            drivers=row.drivers,
            stints=row.stints,
            laps=row.laps,
        )
        for row in results
    ]
