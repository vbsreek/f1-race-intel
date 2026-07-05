from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from f1_race_intel.models.base import Base


class Stint(Base):
    __tablename__ = "stints"
    __table_args__ = (
        UniqueConstraint("session_key", "driver_number", "stint_number", name="uq_stint"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_key: Mapped[int] = mapped_column(ForeignKey("sessions.session_key", ondelete="CASCADE"), index=True)
    driver_number: Mapped[int] = mapped_column(Integer, index=True)
    stint_number: Mapped[int] = mapped_column(Integer)
    compound: Mapped[str | None] = mapped_column(String(16))
    lap_start: Mapped[int | None] = mapped_column(Integer)
    lap_end: Mapped[int | None] = mapped_column(Integer)
    tyre_age_at_start: Mapped[int | None] = mapped_column(Integer)

    session: Mapped["Session"] = relationship(back_populates="stints")


from f1_race_intel.models.session import Session  # noqa: E402
