from typing import List, Dict, Any
from datetime import datetime, timezone

def get_today_timestamp():
    return datetime.now(timezone.utc).isoformat()


# -----------------------------
# BAYSE (prediction markets)
# -----------------------------
def standardize_bayse(events: List[Dict[str, Any]]):

    signals = []

    for e in events:
        for m in e.get("markets", []):

            signals.append({
                "source": "bayse",
                "timestamp": get_today_timestamp(),
                "signal_type": "probability",
                "value": float(m.get("prob", 0)),
                "context": {
                    "title": e.get("title"),
                    "liquidity": e.get("liquidity")
                }
            })

    return signals


# -----------------------------
# POLYMARKET
# -----------------------------
def standardize_polymarket(events: List[Dict[str, Any]]):

    signals = []

    for e in events:
        for m in e.get("markets", []):

            signals.append({
                "source": "polymarket",
                "timestamp": get_today_timestamp(),
                "signal_type": "probability",
                "value": float(m.get("prob", 0)),
                "context": {
                    "title": e.get("title"),
                    "volume": e.get("volume")
                }
            })

    return signals


# -----------------------------
# FX GLOBAL (USD/NGN etc)
# -----------------------------
def standardize_fx(data: Dict[str, Any]):

    return [
        {
            "source": "fx",
            "timestamp": get_today_timestamp(),
            "signal_type": "price",
            "value": float(data["USD_NGN"]),
            "context": {
                "pair": "USD/NGN"
            }
        }
    ]


# -----------------------------
# NAIRA PARALLEL MARKET
# -----------------------------
def standardize_naira(data: Dict[str, Any]):

    if not data:
        return []

    return [
        {
            "source": "nairatoday",
            "timestamp": get_today_timestamp(),
            "signal_type": "price",
            "value": float(data.get("usd_ngn", 0)),
            "context": {
                "market": "black_market"
            }
        }
    ]


# -----------------------------
# EIA (macro oil signal)
# -----------------------------
def standardize_eia(data: Dict[str, Any]):

    if not data:
        return []

    return [
        {
            "source": "eia",
            "timestamp": get_today_timestamp(),
            "signal_type": "macro",
            "value": float(data.get("oil_price", 0)),
            "context": {
                "commodity": "crude_oil"
            }
        }
    ]


# -----------------------------
# NEWS (RAW STRUCTURE ONLY)
# IMPORTANT: no sentiment yet
# -----------------------------
def standardize_news(news_list: List[Dict[str, Any]]):

    signals = []

    for n in news_list:

        signals.append({
            "source": "news",
            "timestamp": get_today_timestamp(),
            "signal_type": "text",
            "value": 0.0,  # placeholder → sentiment later
            "context": {
                "title": n.get("title"),
                "source_name": n.get("source")
            }
        })

    return signals


# -----------------------------
# MASTER ENTRY POINT
# -----------------------------
def standardize_all(filtered: Dict[str, Any]):

    signals = []

    signals += standardize_bayse(filtered.get("bayse", []))
    signals += standardize_polymarket(filtered.get("polymarket", []))
    signals += standardize_fx(filtered.get("fx", {}))
    signals += standardize_naira(filtered.get("nairatoday", {}))
    signals += standardize_eia(filtered.get("eia", {}))
    signals += standardize_news(filtered.get("news", []))

    return signals