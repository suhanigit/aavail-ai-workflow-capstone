import numpy as np
import pandas as pd

FEATURES = ["trend", "month_sin", "month_cos", "lag_1", "lag_12", "rolling_3"]

def make_features(ts):
    ts = ts.sort_values("date").copy()
    ts["trend"] = np.arange(len(ts), dtype=float)
    month = ts["date"].dt.month.astype(float)
    ts["month_sin"] = np.sin(2 * np.pi * month / 12.0)
    ts["month_cos"] = np.cos(2 * np.pi * month / 12.0)
    ts["lag_1"] = ts["revenue"].shift(1)
    ts["lag_12"] = ts["revenue"].shift(12)
    ts["rolling_3"] = ts["revenue"].shift(1).rolling(3).mean()
    return ts.dropna().reset_index(drop=True)

def next_feature_row(history_dates, history_revenue):
    next_date = (pd.Timestamp(history_dates[-1]) + pd.offsets.MonthBegin(1)).normalize()
    month = float(next_date.month)
    trend = float(len(history_revenue))
    lag_1 = float(history_revenue[-1])
    lag_12 = float(history_revenue[-12]) if len(history_revenue) >= 12 else float(np.mean(history_revenue))
    rolling_3 = float(np.mean(history_revenue[-3:]))
    row = {
        "trend": trend,
        "month_sin": float(np.sin(2*np.pi*month/12.0)),
        "month_cos": float(np.cos(2*np.pi*month/12.0)),
        "lag_1": lag_1,
        "lag_12": lag_12,
        "rolling_3": rolling_3,
    }
    return next_date, row
