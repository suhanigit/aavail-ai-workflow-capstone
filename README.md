# AAVAIL Revenue Forecasting - AI Workflow Capstone

A complete, containerized business solution for forecasting AAVAIL monthly revenue by market.  
The project follows an end-to-end AI workflow: **ingestion -> EDA -> model comparison -> deployment API -> logging -> monitoring -> unit testing -> Docker**.

## Business goal

AAVAIL needs a repeatable revenue forecasting service that can return forecasts for a **specific country** or for **all markets combined**. The solution compares multiple models against a seasonal-naive baseline, exposes the selected models through a FastAPI service, logs prediction requests, and provides a simple performance-monitoring mechanism.

## Project structure

```text
.
├── data/monthly_revenue.csv
├── src/
│   ├── ingest.py
│   ├── features.py
│   ├── train.py
│   ├── predict.py
│   ├── api.py
│   ├── logging_utils.py
│   ├── monitor.py
│   └── eda.py
├── tests/
│   ├── test_api.py
│   ├── test_model.py
│   ├── test_logging.py
│   ├── test_monitoring.py
│   └── test_ingest.py
├── artifacts/
│   ├── models/
│   ├── metrics/
│   └── figures/
├── run_tests.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── EDA.md
└── RUBRIC_CHECKLIST.md
```

## Quick start

```bash
python -m pip install -r requirements.txt
make train
make eda
python run_tests.py
make run
```

Open the API documentation at `http://localhost:8000/docs`.

## API examples

Specific country:

```bash
curl "http://localhost:8000/predict?country=singapore&months=3"
```

All markets combined:

```bash
curl "http://localhost:8000/predict?country=all&months=3"
```

Monitoring:

```bash
curl "http://localhost:8000/monitor"
```

## Model comparison

For every country and the aggregate market, the training pipeline evaluates:

1. Linear Regression
2. Random Forest Regression
3. Gradient Boosting Regression

Validation MAE is compared with a **seasonal-naive baseline** (revenue from the same month one year earlier). The best validation model is serialized to `artifacts/models/`, and the detailed metrics are written to `artifacts/metrics/`.

Run:

```bash
make train
make eda
```

The baseline comparison visualization is saved as:

`artifacts/figures/model_vs_baseline.png`

## Unit tests

All tests run with one script:

```bash
python run_tests.py
```

The tests cover:

- API behavior, including country-specific and all-market forecasts
- model training, comparison, persistence, and prediction
- structured logging
- data ingestion
- model performance monitoring

### Test isolation

Unit tests use pytest temporary directories (`tmp_path`) for models, metrics, logs, and monitoring output. They do **not** overwrite the production model or log directories.

## Monitoring

`src/monitor.py` compares each model's validation MAE with its baseline MAE. It assigns a `healthy`, `warning`, or `degraded` state and can append monitoring snapshots to `runtime/monitoring/performance.jsonl`.

The API exposes the same mechanism:

```bash
GET /monitor
```

## Docker

Build and run the complete solution:

```bash
docker build -t aavail-capstone .
docker run --rm -p 8000:8000 aavail-capstone
```

or:

```bash
docker compose up --build
```

The Docker image trains the models during build and starts the FastAPI service on port 8000.

## Data note

`data/monthly_revenue.csv` is a compact, deterministic demonstration dataset included so the peer reviewer can run the entire solution immediately without external credentials or downloads. The ingestion module accepts any CSV with the same `date,country,revenue` schema, so the workflow can be connected to the course/raw production data without changing the model or API interface.

## Peer review

See [`RUBRIC_CHECKLIST.md`](RUBRIC_CHECKLIST.md) for a one-to-one mapping from every grading criterion to the implementation evidence.
