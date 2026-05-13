from app.main import app


def test_health_endpoint():
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_dashboard_structure():
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    payload = response.json()

    assert "timeline" in payload
    assert "strategic" in payload
    assert "operational" in payload
    assert "simulation" in payload
    assert "integrated" in payload
    assert len(payload["timeline"]) >= 12
    assert payload["strategic"]["risk_level"] in {"Blue", "Yellow", "Orange", "Red"}
    assert payload["operational"]["risk_level"] in {"Blue", "Yellow", "Orange", "Red"}
