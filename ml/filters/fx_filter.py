# ml/pipelines/filters/fx_filter.py

def filter_fx(data):
    """
    Keep ONLY relevant FX pairs (USD/NGN focus)
    """

    return {
        "USD_NGN": data["rates"].get("NGN"),
        "timestamp": data.get("timestamp")
    }