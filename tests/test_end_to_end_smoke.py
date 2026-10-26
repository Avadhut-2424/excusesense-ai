import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_pipeline_smoke():
    """
    Smoke test running complete lifecycle:
    1. Health check
    2. Single inference with attribution
    3. Retrieval in history
    4. Stats verification
    5. Clean up
    """
    # 1. Health
    h = client.get("/health")
    assert h.status_code == 200

    # 2. Analyze
    sample_text = "Severe fever requiring emergency clinic visit and doctor consultation."
    res = client.post("/api/v1/analyze", json={"text": sample_text})
    assert res.status_code == 201
    record = res.json()
    record_id = record["id"]
    assert record["prediction"] == "Genuine"
    assert len(record["attributions"]) > 0

    # 3. History
    hist = client.get("/api/v1/history?limit=10")
    assert hist.status_code == 200
    ids = [item["id"] for item in hist.json()]
    assert record_id in ids

    # 4. Stats
    st = client.get("/api/v1/stats")
    assert st.status_code == 200
    assert st.json()["total"] > 0

    # 5. Delete
    d = client.delete(f"/api/v1/history/{record_id}")
    assert d.status_code == 200
