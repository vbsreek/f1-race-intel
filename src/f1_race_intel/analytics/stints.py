from sqlalchemy.orm import Session

from f1_race_intel.api.schemas import StintAnalyticsOut
from f1_race_intel.data.repositories.race_data import RaceDataRepository
from f1_race_intel.data.services.analytics import AnalyticsService


def stint_analytics(db: Session, session_key: int) -> list[StintAnalyticsOut]:
    return AnalyticsService(RaceDataRepository(db)).stint_summary(session_key)
