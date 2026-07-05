from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from f1_race_intel.models.base import Base


class Session(Base):
    __tablename__ = "sessions"

    session_key: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_key: Mapped[int] = mapped_column(Integer, index=True)
    session_type: Mapped[str] = mapped_column(String(64))
    session_name: Mapped[str] = mapped_column(String(128))
    date_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    date_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    circuit_key: Mapped[int | None] = mapped_column(Integer)
    circuit_short_name: Mapped[str | None] = mapped_column(String(64))
    country_code: Mapped[str | None] = mapped_column(String(8))
    country_name: Mapped[str | None] = mapped_column(String(64))
    location: Mapped[str | None] = mapped_column(String(128))
    year: Mapped[int] = mapped_column(Integer, index=True)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    drivers: Mapped[list["Driver"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    stints: Mapped[list["Stint"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    laps: Mapped[list["Lap"]] = relationship(back_populates="session", cascade="all, delete-orphan")


from f1_race_intel.models.driver import Driver  # noqa: E402
from f1_race_intel.models.lap import Lap  # noqa: E402
from f1_race_intel.models.stint import Stint  # noqa: E402
