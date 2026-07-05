from dataclasses import dataclass
from datetime import datetime, timezone

from f1_race_intel.data.openf1.client import OpenF1Client
from f1_race_intel.data.openf1.mappers import driver_to_orm, lap_to_orm, session_to_orm, stint_to_orm
from f1_race_intel.data.repositories.race_data import RaceDataRepository


@dataclass(frozen=True)
class IngestCounts:
    session_key: int
    drivers: int
    stints: int
    laps: int


class IngestService:
    def __init__(self, repo: RaceDataRepository, openf1: OpenF1Client) -> None:
        self._repo = repo
        self._openf1 = openf1

    async def ingest_session(self, session_key: int, *, include_laps: bool = True) -> IngestCounts:
        session_data = await self._openf1.get_session(session_key)
        if session_data is None:
            raise ValueError(f"Session {session_key} not found in OpenF1")

        drivers = [driver_to_orm(row) for row in await self._openf1.get_drivers(session_key)]
        stints = [stint_to_orm(row) for row in await self._openf1.get_stints(session_key)]
        laps = []
        if include_laps:
            laps = [lap_to_orm(row) for row in await self._openf1.get_laps(session_key)]

        self._repo.replace_session_data(session_to_orm(session_data), drivers, stints, laps)

        return IngestCounts(
            session_key=session_key,
            drivers=len(drivers),
            stints=len(stints),
            laps=len(laps),
        )

    async def sync_sessions(
        self,
        *,
        year: int | None = None,
        session_type: str | None = None,
        limit: int = 5,
        include_laps: bool = True,
    ) -> list[IngestCounts]:
        season = year if year is not None else datetime.now(timezone.utc).year
        remote_sessions = await self._openf1.list_sessions(year=season, session_type=session_type)
        remote_sessions.sort(key=lambda session: session.date_start or datetime.min.replace(tzinfo=timezone.utc), reverse=True)

        results: list[IngestCounts] = []
        for session in remote_sessions[:limit]:
            try:
                results.append(await self.ingest_session(session.session_key, include_laps=include_laps))
            except ValueError:
                continue
        return results
