from typing import List, Dict, Any


# -------------------------
# FX NORMALIZATION
# -------------------------
def normalize_fx(value: float) -> float:
    # rough NGN regime bounds (adjust later with real stats)
    min_v, max_v = 1200, 2000
    return max(0.0, min(1.0, (value - min_v) / (max_v - min_v)))


# -------------------------
# PROBABILITY (Bayse/Poly)
# -------------------------
def normalize_prob(value: float) -> float:
    return max(0.0, min(1.0, value))


# -------------------------
# OIL / EIA
# -------------------------
def normalize_oil(value: float) -> float:
    min_v, max_v = 40, 120
    return max(0.0, min(1.0, (value - min_v) / (max_v - min_v)))


# -------------------------
# SENTIMENT (placeholder for now)
# -------------------------
def normalize_sentiment(value: float) -> float:
    return max(-1.0, min(1.0, value))


# -------------------------
# MASTER NORMALIZER
# -------------------------
def normalize_signals(signals: List[Dict[str, Any]]):

    normalized = []

    for s in signals:

        val = s["value"]
        source = s["source"]
        signal_type = s["signal_type"]

        # FX
        if source == "fx":
            val = normalize_fx(val)

        # NAIRA
        elif source == "nairatoday":
            val = normalize_fx(val)

        # BAYSE / POLY
        elif signal_type == "probability":
            val = normalize_prob(val)

        # EIA
        elif source == "eia":
            val = normalize_oil(val)

        # NEWS (still raw sentiment later)
        elif source == "news":
            val = normalize_sentiment(val)

        normalized.append({
            **s,
            "value": val
        })

    return normalized