def make_decision(prob, features):
    sentiment = features["sentiment"]
    gap = features["parallel_gap"]

    if prob > 0.75 and sentiment < -0.5 and gap > 0.3:
        return {
            "recommendation": "ACT",
            "risk": "HIGH"
        }

    if prob > 0.7 and features["oil_trend"] > 0:
        return {
            "recommendation": "WAIT",
            "risk": "MEDIUM"
        }

    return {
        "recommendation": "MONITOR",
        "risk": "LOW"
    }