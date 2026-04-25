def make_decision(probability: float, features: dict):

    sentiment = features["sentiment"]
    gap = features["parallel_gap"]
    oil = features["oil_trend"]

    # HIGH RISK SCENARIO
    if probability > 0.75 and sentiment < -0.5 and gap > 0.3:
        return {
            "recommendation": "BUY_NOW",
            "risk_level": "HIGH",
            "reason": "High FX spike probability + negative sentiment + widening spread"
        }

    # MEDIUM RISK SCENARIO
    if probability > 0.7 and oil < 0:
        return {
            "recommendation": "WAIT",
            "risk_level": "MEDIUM",
            "reason": "Moderate probability with negative oil pressure"
        }

    # DEFAULT
    return {
        "recommendation": "MONITOR",
        "risk_level": "LOW",
        "reason": "No strong market signal detected"
    }