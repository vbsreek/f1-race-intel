import argparse
import asyncio

from f1_race_intel.data import OpenF1Client, RaceDataRepository
from f1_race_intel.data.services import IngestService
from f1_race_intel.db import SessionLocal


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest F1 session data from OpenF1 into Postgres")
    parser.add_argument("session_key", type=int, help="OpenF1 session_key to ingest")
    parser.add_argument("--no-laps", action="store_true", help="Skip lap timing data")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        service = IngestService(RaceDataRepository(db), OpenF1Client())
        counts = asyncio.run(service.ingest_session(args.session_key, include_laps=not args.no_laps))
        print(
            f"Ingested session {counts.session_key}: "
            f"{counts.drivers} drivers, {counts.stints} stints, {counts.laps} laps"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
