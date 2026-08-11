from src.monitor import monitor_models

def test_monitoring_mechanism(trained_paths, tmp_path):
    _, _, metrics_dir = trained_paths
    output = tmp_path / "monitor.jsonl"
    result = monitor_models(metrics_dir, output)
    assert result["models"]
    assert result["overall_status"] in {"healthy", "warning"}
    assert output.exists()
