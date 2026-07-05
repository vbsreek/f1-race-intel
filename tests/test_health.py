from tests.conftest import SESSION_KEY


def test_health(client) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"


def test_root(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "f1-race-intel"


def test_list_sessions_empty(client) -> None:
    response = client.get("/api/v1/sessions")
    assert response.status_code == 200
    assert response.json() == []


def test_get_session(client, sample_session) -> None:
    response = client.get(f"/api/v1/sessions/{SESSION_KEY}")
    assert response.status_code == 200
    body = response.json()
    assert body["session_key"] == SESSION_KEY
    assert body["circuit_short_name"] == "Singapore"


def test_stint_analytics(client, sample_session) -> None:
    response = client.get(f"/api/v1/sessions/{SESSION_KEY}/analytics/stints")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["driver_number"] == 16
    assert body[0]["compound"] == "SOFT"
    assert body[0]["lap_count"] == 3
    assert body[0]["best_lap_time"] == 92.8
    assert body[0]["avg_lap_time"] == 93.767
