from sqlalchemy import Boolean, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from f1_race_intel.models.base import Base


class Lap(Base):
    __tablename__ = "laps"
    __table_args__ = (
        UniqueConstraint("session_key", "driver_number", "lap_number", name="uq_lap"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_key: Mapped[int] = mapped_column(ForeignKey("sessions.session_key", ondelete="CASCADE"), index=True)
    driver_number: Mapped[int] = mapped_column(Integer, index=True)
    lap_number: Mapped[int] = mapped_column(Integer)
    lap_duration: Mapped[float | None] = mapped_column(Float)
    duration_sector_1: Mapped[float | None] = mapped_column(Float)
    duration_sector_2: Mapped[float | None] = mapped_column(Float)
    duration_sector_3: Mapped[float | None] = mapped_column(Float)
    is_pit_out_lap: Mapped[bool | None] = mapped_column(Boolean)
    is_personal_best: Mapped[bool | None] = mapped_column(Boolean)

    session: Mapped["Session"] = relationship(back_populates="laps")


from f1_race_intel.models.session import Session  # noqa: E402
