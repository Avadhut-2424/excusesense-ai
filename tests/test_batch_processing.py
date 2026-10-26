import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_batch_analyze_endpoint():
    payload = {
        "applications": [
            "I have a high fever and doctor advised two days of bed rest.",
            "My fish ate my car keys so I cannot function properly.",
            "I feel completely overwhelmed emotionally and need a wellness day."
        ]
    }
    res = client.post("/api/v1/batch", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_processed"] == 3
    assert len(data["results"]) == 3

    preds = [r["prediction"] for r in data["results"]]
    assert "Genuine" in preds
    assert "Suspicious" in preds
    assert "Emotional" in preds

def test_batch_analyze_empty_payload():
    res = client.post("/api/v1/batch", json={"applications": []})
    assert res.status_code == 422 or res.status_code == 400
