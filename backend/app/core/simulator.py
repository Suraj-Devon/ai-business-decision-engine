import pandas as pd


def simulate_marketing_scenarios(df: pd.DataFrame):
    """
    Simulate impact of changing marketing spend.
    Assumptions (explicit, conservative):
    - CAC remains constant short-term
    - Revenue response is proportional to customer change
    - Operating costs unchanged
    - Impact evaluated on latest month
    """

    latest = df.sort_values("month").iloc[-1]

    # Base metrics
    base_marketing = latest["marketing_spend"]
    base_revenue = latest["revenue"]
    base_customers = latest["new_customers"]
    cash_balance = latest["cash_balance"]
    operating_costs = latest["operating_costs"]

    scenarios = []

    changes = [-0.10, 0.0, 0.10, 0.20]

    # Guard: if no customers, we cannot simulate reliably
    if base_customers <= 0:
        return {
            "scenarios": [],
            "warnings": ["Cannot simulate scenarios with zero customers"]
        }

    cac = base_marketing / base_customers

    for change in changes:
        new_marketing = base_marketing * (1 + change)

        # Expected customers assuming CAC constant
        expected_customers = new_marketing / cac

        # Revenue scales with customers
        revenue_multiplier = expected_customers / base_customers
        expected_revenue = base_revenue * revenue_multiplier

        burn = operating_costs + new_marketing - expected_revenue

        if burn <= 0:
            runway = "infinite"
        else:
            runway = round(cash_balance / burn, 2)

        scenarios.append({
            "change_percent": int(change * 100),
            "expected_revenue": round(expected_revenue, 2),
            "expected_customers": int(expected_customers),
            "burn_rate": round(burn, 2),
            "runway_months": runway
        })

    return {
        "scenarios": scenarios,
        "warnings": []
    }
