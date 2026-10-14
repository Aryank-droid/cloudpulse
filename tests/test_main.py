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


def test_detect_anomalies():
    response = client.post(
        "/detect-anomalies",
        files={
            "file": (
                "scores.csv",
                b"score\n10\n11\n12\n13\n1000\n",
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    result = response.json()
    assert result["model"] == "IsolationForest"
    assert result["rows_analyzed"] == 5
    assert result["anomalies_detected"] >= 1
    assert any(
        item["score"] == 1000.0
        for item in result["anomalies"]
    )

