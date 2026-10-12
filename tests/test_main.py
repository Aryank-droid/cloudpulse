from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["application"] == "CloudPulse"


def test_csv_analysis():
    response = client.post(
        "/analyze",
        files={
            "file": (
                "scores.csv",
                b"score\n10\n20\n30\n",
                "text/csv",
            )
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "rows": 3,
        "average_score": 20.0,
        "highest_score": 30,
        "lowest_score": 10,
    }
