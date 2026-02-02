import pandas as pd


def compute_metrics(df: pd.DataFrame):
    warnings = {}

    metrics = {}

    # Sort defensively
    df = df.sort_values("month")

    # --- Revenue Trend ---
    if len(df) < 2:
        metrics["revenue_trend"] = "insufficient_data"
    else:
        first = df.iloc[0]["revenue"]
        last = df.iloc[-1]["revenue"]

        if last > first:
            metrics["revenue_trend"] = "positive"
        elif last < first:
            metrics["revenue_trend"] = "negative"
        else:
            metrics["revenue_trend"] = "flat"

    # --- CAC ---
    total_customers = df["new_customers"].sum()
    total_marketing = df["marketing_spend"].sum()

    if total_customers == 0:
        metrics["cac"] = None
        warnings["cac"] = "No customers acquired — CAC undefined"
    else:
        metrics["cac"] = round(total_marketing / total_customers, 2)

    # --- Burn Rate (latest month) ---
    latest = df.iloc[-1]

    burn = (
        latest["operating_costs"]
        + latest["marketing_spend"]
        - latest["revenue"]
    )

    metrics["burn_rate"] = burn

    # --- Cash Runway ---
    last_3 = df.tail(3)

    burn_series = (
        last_3["operating_costs"]
        + last_3["marketing_spend"]
        - last_3["revenue"]
    )

    avg_burn = burn_series.mean()

    if avg_burn <= 0:
        metrics["runway_months"] = "infinite"
    else:
        metrics["runway_months"] = round(
            latest["cash_balance"] / avg_burn, 2
        )

    return {
        "metrics": metrics,
        "metric_warnings": warnings
    }
