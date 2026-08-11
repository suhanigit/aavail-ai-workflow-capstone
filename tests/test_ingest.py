from src.ingest import load_monthly_revenue

def test_ingestion_function_validates_and_loads(project_root):
    df = load_monthly_revenue(project_root / "data" / "monthly_revenue.csv")
    assert {"date", "country", "revenue"} <= set(df.columns)
    assert df["revenue"].ge(0).all()
    assert df["country"].nunique() >= 2
