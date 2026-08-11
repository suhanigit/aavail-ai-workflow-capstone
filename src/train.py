from pathlib import Path
import argparse
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from .features import make_features, FEATURES
from .ingest import load_monthly_revenue

def _candidate_models():
    return {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=160, min_samples_leaf=2, random_state=42
        ),
        "gradient_boosting": GradientBoostingRegressor(random_state=42),
    }

def _series_for_country(df, country):
    if country == "all":
        ts = df.groupby("date", as_index=False)["revenue"].sum()
    else:
        ts = df[df["country"] == country][["date", "revenue"]].copy()
    return ts.sort_values("date").reset_index(drop=True)

def train_one(df, country, model_dir, metrics_dir, validation_months=8):
    ts = _series_for_country(df, country)
    feat = make_features(ts)
    if len(feat) <= validation_months + 6:
        raise ValueError("Not enough history to train and validate")

    train = feat.iloc[:-validation_months]
    valid = feat.iloc[-validation_months:]
    X_train, y_train = train[FEATURES], train["revenue"]
    X_valid, y_valid = valid[FEATURES], valid["revenue"]

    baseline_pred = valid["lag_12"].to_numpy()
    baseline_mae = float(mean_absolute_error(y_valid, baseline_pred))

    candidates = {}
    fitted = {}
    for name, model in _candidate_models().items():
        model.fit(X_train, y_train)
        pred = model.predict(X_valid)
        mae = float(mean_absolute_error(y_valid, pred))
        candidates[name] = mae
        fitted[name] = model

    best_name = min(candidates, key=candidates.get)
    best_model = fitted[best_name]

    model_dir = Path(model_dir)
    metrics_dir = Path(metrics_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)

    bundle = {
        "country": country,
        "model_name": best_name,
        "model": best_model,
        "features": FEATURES,
        "history_dates": [d.strftime("%Y-%m-%d") for d in ts["date"]],
        "history_revenue": [float(v) for v in ts["revenue"]],
    }
    joblib.dump(bundle, model_dir / f"{country}.joblib")

    metrics = {
        "country": country,
        "validation_months": validation_months,
        "baseline_mae": baseline_mae,
        "candidate_mae": candidates,
        "best_model": best_name,
        "best_mae": float(candidates[best_name]),
        "improvement_vs_baseline_pct": float(
            100.0 * (baseline_mae - candidates[best_name]) / baseline_mae
        ) if baseline_mae else 0.0,
    }
    (metrics_dir / f"{country}.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    return metrics

def train_all(data_path, model_dir, metrics_dir):
    df = load_monthly_revenue(data_path)
    countries = sorted(df["country"].unique().tolist())
    results = {}
    for country in countries + ["all"]:
        results[country] = train_one(df, country, model_dir, metrics_dir)
    return results

def main():
    parser = argparse.ArgumentParser(description="Train and compare AAVAIL revenue models.")
    parser.add_argument("--data", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--metrics-dir", required=True)
    args = parser.parse_args()
    results = train_all(args.data, args.model_dir, args.metrics_dir)
    for country, metrics in results.items():
        print(
            f"{country}: best={metrics['best_model']} "
            f"MAE={metrics['best_mae']:.2f}, baseline={metrics['baseline_mae']:.2f}"
        )

if __name__ == "__main__":
    main()
