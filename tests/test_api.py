import os
from fastapi.testclient import TestClient
from src.api import app

def test_api_health_and_predictions(trained_paths, tmp_path, monkeypatch):
    _, model_dir, metrics_dir = trained_paths
    monkeypatch.setenv("AAVAIL_MODEL_DIR", str(model_dir))
    monkeypatch.setenv("AAVAIL_METRICS_DIR", str(metrics_dir))
    monkeypatch.setenv("AAVAIL_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("AAVAIL_MONITOR_DIR", str(tmp_path / "monitor"))

    client = TestClient(app)

    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

    r = client.get("/predict", params={"country": "singapore", "months": 2})
    assert r.status_code == 200
    assert r.json()["country"] == "singapore"
    assert len(r.json()["predictions"]) == 2

    r = client.get("/predict", params={"country": "all", "months": 2})
    assert r.status_code == 200
    assert r.json()["country"] == "all"
    assert len(r.json()["predictions"]) == 2

def test_api_monitor_endpoint(trained_paths, tmp_path, monkeypatch):
    _, model_dir, metrics_dir = trained_paths
    monkeypatch.setenv("AAVAIL_MODEL_DIR", str(model_dir))
    monkeypatch.setenv("AAVAIL_METRICS_DIR", str(metrics_dir))
    monkeypatch.setenv("AAVAIL_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("AAVAIL_MONITOR_DIR", str(tmp_path / "monitor"))

    client = TestClient(app)
    r = client.get("/monitor")
    assert r.status_code == 200
    assert r.json()["models"]
