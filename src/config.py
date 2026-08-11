from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(os.getenv("AAVAIL_DATA_PATH", PROJECT_ROOT / "data" / "monthly_revenue.csv"))
MODEL_DIR = Path(os.getenv("AAVAIL_MODEL_DIR", PROJECT_ROOT / "artifacts" / "models"))
METRICS_DIR = Path(os.getenv("AAVAIL_METRICS_DIR", PROJECT_ROOT / "artifacts" / "metrics"))
FIGURE_DIR = Path(os.getenv("AAVAIL_FIGURE_DIR", PROJECT_ROOT / "artifacts" / "figures"))
LOG_DIR = Path(os.getenv("AAVAIL_LOG_DIR", PROJECT_ROOT / "runtime" / "logs"))
MONITOR_DIR = Path(os.getenv("AAVAIL_MONITOR_DIR", PROJECT_ROOT / "runtime" / "monitoring"))

SUPPORTED_COUNTRIES = [
    "united_states",
    "singapore",
    "united_kingdom",
    "germany",
    "france",
]
