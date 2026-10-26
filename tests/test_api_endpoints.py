import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["model_accuracy"] > 0.9

def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"

def test_analyze_endpoint():
    payload = {"text": "I have a dental surgery scheduled this afternoon."}
    res = client.post("/api/v1/analyze", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "attributions" in data
    assert data["id"] > 0

def test_analyze_empty_text_fails():
    res = client.post("/api/v1/analyze", json={"text": "   "})
    assert res.status_code == 400

def test_history_endpoint():
    # Insert one record first
    client.post("/api/v1/analyze", json={"text": "Severe fever and doctor visit."})
    res = client.get("/api/v1/history?limit=10")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert len(items) > 0

def test_stats_endpoint():
    res = client.get("/api/v1/stats")
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "genuine" in data
    assert "suspicious" in data
    assert "emotional" in data
    assert "model_accuracy" in data
