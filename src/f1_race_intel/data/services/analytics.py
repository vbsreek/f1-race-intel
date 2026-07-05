from f1_race_intel.api.schemas import StintAnalyticsOut
from f1_race_intel.data.repositories.race_data import RaceDataRepository
from f1_race_intel.data.services.sessions import SessionService
from f1_race_intel.models import Lap, Stint


class AnalyticsService:
    def __init__(self, repo: RaceDataRepository) -> None:
        self._repo = repo
        self._sessions = SessionService(repo)

    def stint_summary(self, session_key: int) -> list[StintAnalyticsOut]:
        self._sessions.get_session(session_key)

        drivers = {driver.driver_number: driver for driver in self._repo.get_drivers(session_key)}
        stints = self._repo.get_stints(session_key)
        laps = self._repo.get_laps(session_key)

        laps_by_driver: dict[int, list[Lap]] = {}
        for lap in laps:
            laps_by_driver.setdefault(lap.driver_number, []).append(lap)

        results: list[StintAnalyticsOut] = []
        for stint in stints:
            driver = drivers.get(stint.driver_number)
            stint_laps = _laps_for_stint(laps_by_driver.get(stint.driver_number, []), stint)
            valid_times = [lap.lap_duration for lap in stint_laps if lap.lap_duration is not None]

            results.append(
                StintAnalyticsOut(
                    driver_number=stint.driver_number,
                    driver_name=driver.full_name if driver else None,
                    team_name=driver.team_name if driver else None,
                    stint_number=stint.stint_number,
                    compound=stint.compound,
                    lap_start=stint.lap_start,
                    lap_end=stint.lap_end,
                    lap_count=len(stint_laps) if stint_laps else _lap_count_from_bounds(stint),
                    avg_lap_time=round(sum(valid_times) / len(valid_times), 3) if valid_times else None,
                    best_lap_time=round(min(valid_times), 3) if valid_times else None,
                    tyre_age_at_start=stint.tyre_age_at_start,
                )
            )

        return results


def _laps_for_stint(laps: list[Lap], stint: Stint) -> list[Lap]:
    if stint.lap_start is None or stint.lap_end is None:
        return []
    return [lap for lap in laps if stint.lap_start <= lap.lap_number <= stint.lap_end]


def _lap_count_from_bounds(stint: Stint) -> int | None:
    if stint.lap_start is None or stint.lap_end is None:
        return None
    return stint.lap_end - stint.lap_start + 1
