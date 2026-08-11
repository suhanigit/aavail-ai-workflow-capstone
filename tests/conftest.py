from pathlib import Path
import pytest

from src.train import train_all

@pytest.fixture(scope="session")
def project_root():
    return Path(__file__).resolve().parents[1]

@pytest.fixture()
def trained_paths(tmp_path, project_root):
    model_dir = tmp_path / "models"
    metrics_dir = tmp_path / "metrics"
    data_path = project_root / "data" / "monthly_revenue.csv"
    train_all(data_path, model_dir, metrics_dir)
    return data_path, model_dir, metrics_dir
