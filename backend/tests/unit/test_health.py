from fastapi.testclient import TestClient

from src.main import create_app


def test_health_endpoint_returns_status() -> None:
    """A should expose service health through the API."""

    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service_id": "00000000-0000-4000-8000-000000000001",
        "name": "utl-template",
        "healthy": True,
    }
