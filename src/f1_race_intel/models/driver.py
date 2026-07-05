from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from f1_race_intel.models.base import Base


class Driver(Base):
    __tablename__ = "drivers"
    __table_args__ = (UniqueConstraint("session_key", "driver_number", name="uq_driver_session"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_key: Mapped[int] = mapped_column(ForeignKey("sessions.session_key", ondelete="CASCADE"), index=True)
    driver_number: Mapped[int] = mapped_column(Integer)
    broadcast_name: Mapped[str | None] = mapped_column(String(64))
    full_name: Mapped[str | None] = mapped_column(String(128))
    name_acronym: Mapped[str | None] = mapped_column(String(8))
    team_name: Mapped[str | None] = mapped_column(String(64))
    team_colour: Mapped[str | None] = mapped_column(String(16))
    first_name: Mapped[str | None] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    country_code: Mapped[str | None] = mapped_column(String(8))

    session: Mapped["Session"] = relationship(back_populates="drivers")


from f1_race_intel.models.session import Session  # noqa: E402
