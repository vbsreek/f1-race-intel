from datetime import datetime, timezone

from f1_race_intel.data.openf1.schemas import OpenF1Driver, OpenF1Lap, OpenF1Session, OpenF1Stint
from f1_race_intel.models import Driver, Lap, Session as RaceSession, Stint


def build_race_session(
    *,
    session_key: int,
    meeting_key: int,
    session_type: str = "Race",
    session_name: str = "Race",
    year: int = 2023,
    circuit_short_name: str | None = None,
    country_name: str | None = None,
) -> RaceSession:
    return RaceSession(
        session_key=session_key,
        meeting_key=meeting_key,
        session_type=session_type,
        session_name=session_name,
        date_start=datetime(year, 9, 17, 12, 0, tzinfo=timezone.utc),
        circuit_short_name=circuit_short_name,
        country_name=country_name,
        year=year,
        is_cancelled=False,
    )


def build_openf1_session(session: RaceSession) -> OpenF1Session:
    return OpenF1Session(
        session_key=session.session_key,
        meeting_key=session.meeting_key,
        session_type=session.session_type,
        session_name=session.session_name,
        date_start=session.date_start,
        date_end=session.date_end,
        circuit_key=session.circuit_key,
        circuit_short_name=session.circuit_short_name,
        country_code=session.country_code,
        country_name=session.country_name,
        location=session.location,
        year=session.year,
        is_cancelled=session.is_cancelled,
    )


def build_openf1_driver(session_key: int, driver_number: int, **kwargs) -> OpenF1Driver:
    return OpenF1Driver(session_key=session_key, driver_number=driver_number, **kwargs)


def build_openf1_stint(session_key: int, driver_number: int, stint_number: int, **kwargs) -> OpenF1Stint:
    return OpenF1Stint(
        session_key=session_key,
        driver_number=driver_number,
        stint_number=stint_number,
        **kwargs,
    )


def build_openf1_lap(session_key: int, driver_number: int, lap_number: int, **kwargs) -> OpenF1Lap:
    return OpenF1Lap(
        session_key=session_key,
        driver_number=driver_number,
        lap_number=lap_number,
        **kwargs,
    )


def seed_stint_dataset(db_session, session_key: int, meeting_key: int) -> RaceSession:
    race = build_race_session(
        session_key=session_key,
        meeting_key=meeting_key,
        circuit_short_name="Singapore",
        country_name="Singapore",
    )
    db_session.add(race)
    db_session.add(
        Driver(
            session_key=session_key,
            driver_number=16,
            full_name="Charles LECLERC",
            name_acronym="LEC",
            team_name="Ferrari",
        )
    )
    db_session.add(
        Stint(
            session_key=session_key,
            driver_number=16,
            stint_number=1,
            compound="SOFT",
            lap_start=1,
            lap_end=3,
            tyre_age_at_start=3,
        )
    )
    for lap_number, duration in [(1, 95.1), (2, 93.4), (3, 92.8)]:
        db_session.add(
            Lap(
                session_key=session_key,
                driver_number=16,
                lap_number=lap_number,
                lap_duration=duration,
            )
        )
    db_session.commit()
    return race
