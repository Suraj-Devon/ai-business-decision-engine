from fastapi import APIRouter
from app.core.data_loader import load_demo_data
from app.core.metrics import compute_metrics
from app.core.simulator import simulate_marketing_scenarios
from app.core.decision import decide_marketing_action
from app.ai.reasoning import explain_decision
import pandas as pd
import numpy as np

router = APIRouter()


def normalize_value(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


@router.get("/api/demo/data")
def get_demo_data():
    return load_demo_data()


@router.get("/api/metrics/preview")
def preview_metrics():
    demo = load_demo_data()
    df = pd.DataFrame(demo["data"])

    result = compute_metrics(df)

    return {
        "metrics": {
            k: normalize_value(v)
            for k, v in result["metrics"].items()
        },
        "metric_warnings": result["metric_warnings"]
    }


@router.post("/api/decision/marketing-spend")
def marketing_spend_decision():
    demo = load_demo_data()
    df = pd.DataFrame(demo["data"])

    metrics_result = compute_metrics(df)
    metrics = metrics_result["metrics"]

    simulation = simulate_marketing_scenarios(df)

    decision = decide_marketing_action(
        metrics=metrics,
        scenarios=simulation["scenarios"]
    )

    explanation = explain_decision(
        recommendation=decision["recommendation"],
        confidence=decision["confidence"],
        metrics=metrics,
        scenarios=simulation["scenarios"],
        risks=decision["risks"]
    )

    return {
        "recommendation": decision["recommendation"],
        "confidence": decision["confidence"],
        "explanation": explanation,
        "metrics": {
            k: normalize_value(v)
            for k, v in metrics.items()
        },
        "scenarios": simulation["scenarios"],
        "risks": decision["risks"],
        "data_warnings": demo["data_warnings"] + simulation["warnings"]
    }
