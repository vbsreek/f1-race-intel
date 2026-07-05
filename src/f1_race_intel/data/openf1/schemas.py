from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OpenF1Session(BaseModel):
    model_config = ConfigDict(extra="ignore")

    session_key: int
    meeting_key: int
    session_type: str
    session_name: str
    date_start: datetime | None = None
    date_end: datetime | None = None
    circuit_key: int | None = None
    circuit_short_name: str | None = None
    country_code: str | None = None
    country_name: str | None = None
    location: str | None = None
    year: int
    is_cancelled: bool = False


class OpenF1Driver(BaseModel):
    model_config = ConfigDict(extra="ignore")

    session_key: int
    driver_number: int
    broadcast_name: str | None = None
    full_name: str | None = None
    name_acronym: str | None = None
    team_name: str | None = None
    team_colour: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    country_code: str | None = None


class OpenF1Stint(BaseModel):
    model_config = ConfigDict(extra="ignore")

    session_key: int
    driver_number: int
    stint_number: int
    compound: str | None = None
    lap_start: int | None = None
    lap_end: int | None = None
    tyre_age_at_start: int | None = None


class OpenF1Lap(BaseModel):
    model_config = ConfigDict(extra="ignore")

    session_key: int
    driver_number: int
    lap_number: int
    lap_duration: float | None = None
    duration_sector_1: float | None = None
    duration_sector_2: float | None = None
    duration_sector_3: float | None = None
    is_pit_out_lap: bool | None = None
    is_personal_best: bool | None = None
