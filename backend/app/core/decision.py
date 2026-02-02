def decide_marketing_action(metrics: dict, scenarios: list):
    """
    Rule-based decision engine.
    AI will NEVER override this.
    """

    risks = []
    confidence = "MEDIUM"

    revenue_trend = metrics.get("revenue_trend")
    runway = metrics.get("runway_months")

    # Normalize runway for logic
    if runway == "infinite":
        runway_value = float("inf")
    else:
        runway_value = runway

    # Decision rules
    if runway_value < 3:
        decision = "DECREASE"
        risks.append("Runway below 3 months")
        confidence = "HIGH"

    elif 3 <= runway_value < 6:
        decision = "HOLD"
        risks.append("Runway between 3–6 months")
        confidence = "MEDIUM"

    else:
        if revenue_trend == "positive":
            decision = "INCREASE"
            confidence = "MEDIUM"
        else:
            decision = "HOLD"
            risks.append("Revenue trend not positive")

    # Scenario-based risk checks
    for s in scenarios:
        if s["change_percent"] > 0 and s["runway_months"] != "infinite":
            if s["runway_months"] < 3:
                risks.append(
                    f"+{s['change_percent']}% spend drops runway below 3 months"
                )

    return {
        "recommendation": decision,
        "confidence": confidence,
        "risks": list(set(risks))
    }
