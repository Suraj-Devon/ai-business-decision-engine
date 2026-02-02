import pandas as pd
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "demo_monthly_data.csv"


def load_demo_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError("Demo data file not found")

    df = pd.read_csv(DATA_FILE)

    warnings = []

    # Basic validation
    required_columns = {
        "month",
        "revenue",
        "marketing_spend",
        "new_customers",
        "operating_costs",
        "cash_balance",
    }

    missing_cols = required_columns - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Check ordering
    if not df["month"].is_monotonic_increasing:
        warnings.append("Months are not in chronological order")

    # Check missing customers
    zero_customer_months = df[df["new_customers"] == 0]["month"].tolist()
    for m in zero_customer_months:
        warnings.append(f"No customers acquired in {m}")

    return {
        "company": "Demo B2B SaaS Startup",
        "currency": "USD",
        "period": "monthly",
        "data": df.to_dict(orient="records"),
        "data_warnings": warnings,
    }
