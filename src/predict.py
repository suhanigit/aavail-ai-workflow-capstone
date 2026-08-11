from pathlib import Path
import joblib
import pandas as pd

from .features import next_feature_row, FEATURES

def load_bundle(country, model_dir):
    path = Path(model_dir) / f"{country}.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model not found for country={country}: {path}")
    return joblib.load(path)

def forecast(country, months, model_dir):
    if months < 1 or months > 24:
        raise ValueError("months must be between 1 and 24")

    bundle = load_bundle(country, model_dir)
    model = bundle["model"]
    history_dates = [pd.Timestamp(d) for d in bundle["history_dates"]]
    history_revenue = [float(v) for v in bundle["history_revenue"]]

    output = []
    for _ in range(months):
        next_date, row = next_feature_row(history_dates, history_revenue)
        X = pd.DataFrame([row], columns=FEATURES)
        pred = max(0.0, float(model.predict(X)[0]))
        output.append(
            {
                "date": next_date.strftime("%Y-%m"),
                "predicted_revenue": round(pred, 2),
            }
        )
        history_dates.append(next_date)
        history_revenue.append(pred)
    return output
