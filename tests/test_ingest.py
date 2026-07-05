import pytest

from f1_race_intel.data.repositories.race_data import RaceDataRepository
from f1_race_intel.data.services import IngestService
from tests.conftest import MEETING_KEY, SESSION_KEY
from tests.factories import (
    build_openf1_driver,
    build_openf1_lap,
    build_openf1_session,
    build_openf1_stint,
    build_race_session,
)


class FakeOpenF1Client:
    def __init__(self, session_key: int = SESSION_KEY, meeting_key: int = MEETING_KEY) -> None:
        self._session = build_race_session(session_key=session_key, meeting_key=meeting_key)
        self._openf1_session = build_openf1_session(self._session)

    async def get_session(self, session_key: int):
        if session_key != self._session.session_key:
            return None
        return self._openf1_session

    async def get_drivers(self, session_key: int):
        if session_key != self._session.session_key:
            return []
        return [
            build_openf1_driver(
                session_key,
                16,
                full_name="Charles LECLERC",
                name_acronym="LEC",
                team_name="Ferrari",
            )
        ]

    async def get_stints(self, session_key: int):
        if session_key != self._session.session_key:
            return []
        return [
            build_openf1_stint(
                session_key,
                16,
                1,
                compound="SOFT",
                lap_start=1,
                lap_end=3,
                tyre_age_at_start=3,
            )
        ]

    async def get_laps(self, session_key: int):
        if session_key != self._session.session_key:
            return []
        return [
            build_openf1_lap(session_key, 16, lap_number, lap_duration=duration)
            for lap_number, duration in [(1, 95.1), (2, 93.4), (3, 92.8)]
        ]

    async def list_sessions(self, *, year=None, session_type=None):
        if year is not None and self._session.year != year:
            return []
        if session_type is not None and self._session.session_type != session_type:
            return []
        return [self._openf1_session]


@pytest.mark.asyncio
async def test_ingest_service_persists_openf1_payload(db_session) -> None:
    service = IngestService(RaceDataRepository(db_session), FakeOpenF1Client())
    counts = await service.ingest_session(SESSION_KEY)

    assert counts.drivers == 1
    assert counts.stints == 1
    assert counts.laps == 3

    repo = RaceDataRepository(db_session)
    session = repo.get_session(SESSION_KEY)
    assert session is not None
    assert session.meeting_key == MEETING_KEY
    assert len(repo.get_drivers(SESSION_KEY)) == 1
    assert len(repo.get_stints(SESSION_KEY)) == 1
    assert len(repo.get_laps(SESSION_KEY)) == 3
