# EDA summary

The project includes a reproducible exploratory analysis of monthly revenue by country.

Run:

```bash
make train
make eda
```

Generated visualizations:

- `artifacts/figures/eda_revenue_by_country.png`
- `artifacts/figures/model_vs_baseline.png`

The first chart checks market-level trends, seasonality, and scale differences.
The second chart compares each selected forecasting model with a seasonal-naive baseline using validation MAE.
