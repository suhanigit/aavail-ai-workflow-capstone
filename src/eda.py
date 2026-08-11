from pathlib import Path
import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt

from .ingest import load_monthly_revenue

def make_eda_figures(data_path, metrics_dir, figure_dir):
    df = load_monthly_revenue(data_path)
    figure_dir = Path(figure_dir)
    figure_dir.mkdir(parents=True, exist_ok=True)

    monthly = (
        df.groupby(["date", "country"], as_index=False)["revenue"].sum()
    )
    pivot = monthly.pivot(index="date", columns="country", values="revenue")
    ax = pivot.plot(figsize=(11, 6))
    ax.set_title("AAVAIL monthly revenue by country")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.grid(alpha=0.25)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(figure_dir / "eda_revenue_by_country.png", dpi=160)
    plt.close(fig)

    rows = []
    for path in Path(metrics_dir).glob("*.json"):
        m = json.loads(path.read_text(encoding="utf-8"))
        rows.append({
            "country": m["country"],
            "baseline_mae": m["baseline_mae"],
            "best_model_mae": m["best_mae"],
        })
    comp = pd.DataFrame(rows).sort_values("country")
    ax = comp.set_index("country")[["baseline_mae", "best_model_mae"]].plot(
        kind="bar", figsize=(11, 6)
    )
    ax.set_title("Best model versus seasonal-naive baseline")
    ax.set_ylabel("Validation MAE (lower is better)")
    ax.grid(axis="y", alpha=0.25)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(figure_dir / "model_vs_baseline.png", dpi=160)
    plt.close(fig)
    return [
        figure_dir / "eda_revenue_by_country.png",
        figure_dir / "model_vs_baseline.png",
    ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--metrics-dir", required=True)
    parser.add_argument("--figure-dir", required=True)
    args = parser.parse_args()
    for path in make_eda_figures(args.data, args.metrics_dir, args.figure_dir):
        print(path)

if __name__ == "__main__":
    main()
