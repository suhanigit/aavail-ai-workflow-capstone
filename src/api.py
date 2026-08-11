from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
import os

from .config import MODEL_DIR, METRICS_DIR, LOG_DIR, MONITOR_DIR
from .predict import forecast
from .monitor import monitor_models
from .logging_utils import get_logger, log_event

app = FastAPI(
    title="AAVAIL Revenue Forecast API",
    version="1.0.0",
    description="Forecast monthly AAVAIL revenue by country or for all countries combined.",
)

def _model_dir():
    return Path(os.getenv("AAVAIL_MODEL_DIR", MODEL_DIR))

def _metrics_dir():
    return Path(os.getenv("AAVAIL_METRICS_DIR", METRICS_DIR))

def _log_dir():
    return Path(os.getenv("AAVAIL_LOG_DIR", LOG_DIR))

def _monitor_dir():
    return Path(os.getenv("AAVAIL_MONITOR_DIR", MONITOR_DIR))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/predict")
def predict(
    country: str = Query("all", description="Country slug or 'all'"),
    months: int = Query(3, ge=1, le=24),
):
    country = country.lower().strip()
    try:
        predictions = forecast(country, months, _model_dir())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Unknown or untrained country: {country}")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    logger = get_logger("api", _log_dir())
    log_event(logger, "prediction", country=country, months=months)
    return {"country": country, "months": months, "predictions": predictions}

@app.get("/monitor")
def monitor():
    result = monitor_models(
        _metrics_dir(),
        _monitor_dir() / "performance.jsonl",
    )
    logger = get_logger("monitor", _log_dir())
    log_event(logger, "monitor_check", overall_status=result["overall_status"])
    return result
