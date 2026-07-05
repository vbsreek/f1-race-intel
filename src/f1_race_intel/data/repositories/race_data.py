from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from f1_race_intel.models import Driver, Lap, Session as RaceSession, Stint


class RaceDataRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_sessions(
        self,
        *,
        year: int | None = None,
        session_type: str | None = None,
        limit: int = 50,
    ) -> list[RaceSession]:
        query = select(RaceSession).order_by(RaceSession.date_start.desc().nullslast())
        if year is not None:
            query = query.where(RaceSession.year == year)
        if session_type is not None:
            query = query.where(RaceSession.session_type == session_type)
        return list(self._db.scalars(query.limit(limit)).all())

    def get_session(self, session_key: int) -> RaceSession | None:
        return self._db.get(RaceSession, session_key)

    def get_drivers(self, session_key: int) -> list[Driver]:
        return list(
            self._db.scalars(
                select(Driver)
                .where(Driver.session_key == session_key)
                .order_by(Driver.driver_number)
            ).all()
        )

    def get_stints(self, session_key: int) -> list[Stint]:
        return list(
            self._db.scalars(
                select(Stint)
                .where(Stint.session_key == session_key)
                .order_by(Stint.driver_number, Stint.stint_number)
            ).all()
        )

    def get_laps(self, session_key: int) -> list[Lap]:
        return list(
            self._db.scalars(
                select(Lap)
                .where(Lap.session_key == session_key)
                .order_by(Lap.driver_number, Lap.lap_number)
            ).all()
        )

    def replace_session_data(
        self,
        session: RaceSession,
        drivers: list[Driver],
        stints: list[Stint],
        laps: list[Lap],
    ) -> None:
        session_key = session.session_key
        self._db.merge(session)
        self._db.flush()

        self._db.execute(delete(Driver).where(Driver.session_key == session_key))
        self._db.execute(delete(Stint).where(Stint.session_key == session_key))
        self._db.execute(delete(Lap).where(Lap.session_key == session_key))

        self._db.add_all(drivers)
        self._db.add_all(stints)
        self._db.add_all(laps)
        self._db.commit()

    def ping(self) -> bool:
        from sqlalchemy import text

        self._db.execute(text("SELECT 1"))
        return True
