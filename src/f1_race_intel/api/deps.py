from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from f1_race_intel.data import OpenF1Client, RaceDataRepository
from f1_race_intel.data.services import AnalyticsService, IngestService, SessionService
from f1_race_intel.db import get_db as _get_db

DbSession = Annotated[Session, Depends(_get_db)]


def get_race_data_repo(db: DbSession) -> RaceDataRepository:
    return RaceDataRepository(db)


def get_openf1_client() -> OpenF1Client:
    return OpenF1Client()


def get_session_service(repo: Annotated[RaceDataRepository, Depends(get_race_data_repo)]) -> SessionService:
    return SessionService(repo)


def get_analytics_service(repo: Annotated[RaceDataRepository, Depends(get_race_data_repo)]) -> AnalyticsService:
    return AnalyticsService(repo)


def get_ingest_service(
    repo: Annotated[RaceDataRepository, Depends(get_race_data_repo)],
    openf1: Annotated[OpenF1Client, Depends(get_openf1_client)],
) -> IngestService:
    return IngestService(repo, openf1)
