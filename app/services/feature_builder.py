from data_ingestion.scheduler.jobs import collect_all_data

def build_features():

    data = collect_all_data()

    bayse = data["bayse"]
    poly = data["polymarket"]
    naira = data["naira_local"]

    # SAFE DEFAULTS (important for production stability)
    bayse_prob = 0.6
    poly_prob = 0.6

    if isinstance(bayse, list) and len(bayse) > 0:
        bayse_prob = bayse[0].get("probability", 0.6)

    if isinstance(poly, list) and len(poly) > 0:
        poly_prob = poly[0].get("probability", 0.6)

    return {
        "parallel_gap": 0.36,
        "bayse_prob": bayse_prob,
        "polymarket_prob": poly_prob,
        "naira_rate_signal": 1.0,  # placeholder normalized signal
        "sentiment": -0.5,
        "volatility": 0.3
    }