from f1_race_intel.analytics.stints import stint_analytics


from tests.conftest import SESSION_KEY


def test_stint_analytics_computes_lap_stats(db_session, sample_session) -> None:
    results = stint_analytics(db_session, SESSION_KEY)
    assert len(results) == 1
    row = results[0]
    assert row.driver_name == "Charles LECLERC"
    assert row.lap_count == 3
    assert row.best_lap_time == 92.8
    assert row.avg_lap_time == 93.767
