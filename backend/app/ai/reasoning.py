def explain_decision(
    recommendation: str,
    confidence: str,
    metrics: dict,
    scenarios: list,
    risks: list
):
    """
    Explain-only reasoning layer.
    This module MUST NOT:
    - compute metrics
    - change decisions
    - hide uncertainty
    """

    lines = []

    # Opening
    lines.append(
        f"The system recommends to **{recommendation} marketing spend** "
        f"with **{confidence.lower()} confidence**."
    )

    # Metrics-based reasoning
    if metrics.get("revenue_trend") == "positive":
        lines.append(
            "Revenue has been trending upward, indicating that current growth strategies are effective."
        )
    else:
        lines.append(
            "Revenue growth is not clearly positive, which limits aggressive spending decisions."
        )

    if metrics.get("runway_months") == "infinite":
        lines.append(
            "The company is currently profitable, resulting in an effectively infinite cash runway."
        )
    else:
        lines.append(
            f"Cash runway is approximately {metrics.get('runway_months')} months, "
            "which constrains how aggressively spending can increase."
        )

    # Scenario trade-offs
    positive_scenarios = [
        s for s in scenarios if s["change_percent"] > 0
    ]

    if positive_scenarios:
        best = max(
            positive_scenarios,
            key=lambda s: s["expected_revenue"]
        )
        lines.append(
            f"In scenario analysis, increasing marketing spend by "
            f"{best['change_percent']}% leads to the highest expected revenue "
            f"while maintaining financial stability."
        )

    # Risks
    if risks:
        lines.append(
            "Key risks to monitor include:"
        )
        for r in risks:
            lines.append(f"- {r}")
    else:
        lines.append(
            "No immediate financial risks were detected under current assumptions."
        )

    # Explicit uncertainty
    lines.append(
        "This recommendation assumes customer acquisition efficiency remains stable "
        "and that revenue response follows recent trends."
    )

    return "\n".join(lines)
