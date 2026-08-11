from pathlib import Path
import argparse
import pandas as pd

REQUIRED_COLUMNS = {"date", "country", "revenue"}

def load_monthly_revenue(path):
    path = Path(path)
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="raise")
    df["country"] = df["country"].astype(str).str.lower().str.strip()
    df["revenue"] = pd.to_numeric(df["revenue"], errors="raise")

    if df[["date", "country", "revenue"]].isna().any().any():
        raise ValueError("Nulls detected in required fields")
    if (df["revenue"] < 0).any():
        raise ValueError("Revenue cannot be negative")

    df = (
        df.groupby(["date", "country"], as_index=False)["revenue"]
          .sum()
          .sort_values(["country", "date"])
          .reset_index(drop=True)
    )
    return df

def ingest_csv(input_path, output_path):
    df = load_monthly_revenue(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Validate and ingest AAVAIL monthly revenue data.")
    parser.add_argument("--input", required=True, help="Input CSV with date,country,revenue")
    parser.add_argument("--output", required=True, help="Validated output CSV")
    args = parser.parse_args()
    out = ingest_csv(args.input, args.output)
    print(f"Ingested data -> {out}")

if __name__ == "__main__":
    main()
