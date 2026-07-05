"""Alembic migrations for F1 Race Intelligence."""

import sqlalchemy as sa
from alembic import op

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sessions",
        sa.Column("session_key", sa.Integer(), nullable=False),
        sa.Column("meeting_key", sa.Integer(), nullable=False),
        sa.Column("session_type", sa.String(length=64), nullable=False),
        sa.Column("session_name", sa.String(length=128), nullable=False),
        sa.Column("date_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("date_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("circuit_key", sa.Integer(), nullable=True),
        sa.Column("circuit_short_name", sa.String(length=64), nullable=True),
        sa.Column("country_code", sa.String(length=8), nullable=True),
        sa.Column("country_name", sa.String(length=64), nullable=True),
        sa.Column("location", sa.String(length=128), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("is_cancelled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("session_key"),
    )
    op.create_index("ix_sessions_meeting_key", "sessions", ["meeting_key"])
    op.create_index("ix_sessions_year", "sessions", ["year"])

    op.create_table(
        "drivers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_key", sa.Integer(), nullable=False),
        sa.Column("driver_number", sa.Integer(), nullable=False),
        sa.Column("broadcast_name", sa.String(length=64), nullable=True),
        sa.Column("full_name", sa.String(length=128), nullable=True),
        sa.Column("name_acronym", sa.String(length=8), nullable=True),
        sa.Column("team_name", sa.String(length=64), nullable=True),
        sa.Column("team_colour", sa.String(length=16), nullable=True),
        sa.Column("first_name", sa.String(length=64), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=True),
        sa.Column("country_code", sa.String(length=8), nullable=True),
        sa.ForeignKeyConstraint(["session_key"], ["sessions.session_key"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_key", "driver_number", name="uq_driver_session"),
    )
    op.create_index("ix_drivers_session_key", "drivers", ["session_key"])

    op.create_table(
        "stints",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_key", sa.Integer(), nullable=False),
        sa.Column("driver_number", sa.Integer(), nullable=False),
        sa.Column("stint_number", sa.Integer(), nullable=False),
        sa.Column("compound", sa.String(length=16), nullable=True),
        sa.Column("lap_start", sa.Integer(), nullable=True),
        sa.Column("lap_end", sa.Integer(), nullable=True),
        sa.Column("tyre_age_at_start", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["session_key"], ["sessions.session_key"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_key", "driver_number", "stint_number", name="uq_stint"),
    )
    op.create_index("ix_stints_session_key", "stints", ["session_key"])
    op.create_index("ix_stints_driver_number", "stints", ["driver_number"])

    op.create_table(
        "laps",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_key", sa.Integer(), nullable=False),
        sa.Column("driver_number", sa.Integer(), nullable=False),
        sa.Column("lap_number", sa.Integer(), nullable=False),
        sa.Column("lap_duration", sa.Float(), nullable=True),
        sa.Column("duration_sector_1", sa.Float(), nullable=True),
        sa.Column("duration_sector_2", sa.Float(), nullable=True),
        sa.Column("duration_sector_3", sa.Float(), nullable=True),
        sa.Column("is_pit_out_lap", sa.Boolean(), nullable=True),
        sa.Column("is_personal_best", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["session_key"], ["sessions.session_key"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_key", "driver_number", "lap_number", name="uq_lap"),
    )
    op.create_index("ix_laps_session_key", "laps", ["session_key"])
    op.create_index("ix_laps_driver_number", "laps", ["driver_number"])


def downgrade() -> None:
    op.drop_table("laps")
    op.drop_table("stints")
    op.drop_table("drivers")
    op.drop_table("sessions")
