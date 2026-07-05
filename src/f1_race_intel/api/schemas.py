from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_key: int
    meeting_key: int
    session_type: str
    session_name: str
    date_start: datetime | None
    date_end: datetime | None
    circuit_short_name: str | None
    country_name: str | None
    location: str | None
    year: int
    is_cancelled: bool


class DriverOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_number: int
    full_name: str | None
    name_acronym: str | None
    team_name: str | None
    country_code: str | None


class StintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_number: int
    stint_number: int
    compound: str | None
    lap_start: int | None
    lap_end: int | None
    tyre_age_at_start: int | None


class StintAnalyticsOut(BaseModel):
    driver_number: int
    driver_name: str | None
    team_name: str | None
    stint_number: int
    compound: str | None
    lap_start: int | None
    lap_end: int | None
    lap_count: int | None
    avg_lap_time: float | None
    best_lap_time: float | None
    tyre_age_at_start: int | None


class IngestResult(BaseModel):
    session_key: int
    drivers: int
    stints: int
    laps: int


class HealthOut(BaseModel):
    status: str
    database: str
