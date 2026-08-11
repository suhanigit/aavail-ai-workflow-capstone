import json
from src.predict import forecast

def test_models_are_compared_and_saved(trained_paths):
    _, model_dir, metrics_dir = trained_paths
    metrics = json.loads((metrics_dir / "singapore.json").read_text())
    assert set(metrics["candidate_mae"]) == {
        "linear_regression", "random_forest", "gradient_boosting"
    }
    assert (model_dir / "singapore.joblib").exists()
    assert metrics["best_mae"] > 0
    assert metrics["baseline_mae"] > 0

def test_country_and_all_forecasts(trained_paths):
    _, model_dir, _ = trained_paths
    sg = forecast("singapore", 3, model_dir)
    all_market = forecast("all", 3, model_dir)
    assert len(sg) == 3
    assert len(all_market) == 3
    assert all(p["predicted_revenue"] > 0 for p in sg)
    assert all(p["predicted_revenue"] > 0 for p in all_market)
