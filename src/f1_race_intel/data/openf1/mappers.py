from f1_race_intel.data.openf1.schemas import OpenF1Driver, OpenF1Lap, OpenF1Session, OpenF1Stint
from f1_race_intel.models import Driver, Lap, Session as RaceSession, Stint


def session_to_orm(data: OpenF1Session) -> RaceSession:
    return RaceSession(
        session_key=data.session_key,
        meeting_key=data.meeting_key,
        session_type=data.session_type,
        session_name=data.session_name,
        date_start=data.date_start,
        date_end=data.date_end,
        circuit_key=data.circuit_key,
        circuit_short_name=data.circuit_short_name,
        country_code=data.country_code,
        country_name=data.country_name,
        location=data.location,
        year=data.year,
        is_cancelled=data.is_cancelled,
    )


def driver_to_orm(data: OpenF1Driver) -> Driver:
    return Driver(
        session_key=data.session_key,
        driver_number=data.driver_number,
        broadcast_name=data.broadcast_name,
        full_name=data.full_name,
        name_acronym=data.name_acronym,
        team_name=data.team_name,
        team_colour=data.team_colour,
        first_name=data.first_name,
        last_name=data.last_name,
        country_code=data.country_code,
    )


def stint_to_orm(data: OpenF1Stint) -> Stint:
    return Stint(
        session_key=data.session_key,
        driver_number=data.driver_number,
        stint_number=data.stint_number,
        compound=data.compound,
        lap_start=data.lap_start,
        lap_end=data.lap_end,
        tyre_age_at_start=data.tyre_age_at_start,
    )


def lap_to_orm(data: OpenF1Lap) -> Lap:
    return Lap(
        session_key=data.session_key,
        driver_number=data.driver_number,
        lap_number=data.lap_number,
        lap_duration=data.lap_duration,
        duration_sector_1=data.duration_sector_1,
        duration_sector_2=data.duration_sector_2,
        duration_sector_3=data.duration_sector_3,
        is_pit_out_lap=data.is_pit_out_lap,
        is_personal_best=data.is_personal_best,
    )
