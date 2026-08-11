# Peer-review rubric checklist

| Grading criterion | Evidence in this repository |
|---|---|
| Unit tests for the API | `tests/test_api.py` |
| Unit tests for the model | `tests/test_model.py` |
| Unit tests for logging | `tests/test_logging.py` |
| Run all unit tests with a single script; tests pass | `python run_tests.py` |
| Performance monitoring | `src/monitor.py`, `/monitor` API endpoint |
| Isolate read/write tests from production | All model/log/monitor tests use pytest `tmp_path`; production directories are not written by tests |
| API supports a specific country and all countries combined | `/predict?country=singapore&months=3` and `/predict?country=all&months=3` |
| Data ingestion exists as a function or script | `src/ingest.py` (`load_monthly_revenue`, `ingest_csv`) |
| Multiple models compared | Linear Regression, Random Forest, Gradient Boosting in `src/train.py` |
| EDA investigation uses visualizations | `src/eda.py`, `EDA.md`, generated PNG figures |
| Working Docker image definition | `Dockerfile` and `docker-compose.yml` |
| Visualization compares model with baseline | `artifacts/figures/model_vs_baseline.png` |

## Quick reviewer commands

```bash
pip install -r requirements.txt
python run_tests.py
python -m src.train --data data/monthly_revenue.csv --model-dir artifacts/models --metrics-dir artifacts/metrics
python -m src.eda --data data/monthly_revenue.csv --metrics-dir artifacts/metrics --figure-dir artifacts/figures
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

API examples:

```bash
curl "http://localhost:8000/predict?country=singapore&months=3"
curl "http://localhost:8000/predict?country=all&months=3"
curl "http://localhost:8000/monitor"
```


Pre-packaging validation: see `VALIDATION_REPORT.md` (**7 tests passed**).
