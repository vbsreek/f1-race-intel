from f1_race_intel.data.repositories.race_data import RaceDataRepository
from f1_race_intel.models import Driver, Session as RaceSession, Stint


class SessionNotFoundError(LookupError):
    pass


class SessionService:
    def __init__(self, repo: RaceDataRepository) -> None:
        self._repo = repo

    def list_sessions(
        self,
        *,
        year: int | None = None,
        session_type: str | None = None,
        limit: int = 50,
    ) -> list[RaceSession]:
        return self._repo.list_sessions(year=year, session_type=session_type, limit=limit)

    def get_session(self, session_key: int) -> RaceSession:
        session = self._repo.get_session(session_key)
        if session is None:
            raise SessionNotFoundError(f"Session {session_key} not found")
        return session

    def get_drivers(self, session_key: int) -> list[Driver]:
        self.get_session(session_key)
        return self._repo.get_drivers(session_key)

    def get_stints(self, session_key: int) -> list[Stint]:
        self.get_session(session_key)
        return self._repo.get_stints(session_key)
