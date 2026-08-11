from pathlib import Path
from datetime import datetime, timezone
import argparse
import json

def monitor_models(metrics_dir, output_path=None):
    metrics_dir = Path(metrics_dir)
    records = []
    for path in sorted(metrics_dir.glob("*.json")):
        m = json.loads(path.read_text(encoding="utf-8"))
        ratio = m["best_mae"] / m["baseline_mae"] if m["baseline_mae"] else 0.0
        status = "healthy" if ratio <= 1.0 else ("warning" if ratio <= 1.15 else "degraded")
        records.append({
            "country": m["country"],
            "best_model": m["best_model"],
            "best_mae": m["best_mae"],
            "baseline_mae": m["baseline_mae"],
            "mae_to_baseline_ratio": ratio,
            "status": status,
        })

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_status": (
            "healthy" if records and all(r["status"] == "healthy" for r in records)
            else "warning"
        ),
        "models": records,
    }

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(summary) + "\n")
    return summary

def main():
    parser = argparse.ArgumentParser(description="Monitor model performance versus baseline.")
    parser.add_argument("--metrics-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = monitor_models(args.metrics_dir, args.output)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
