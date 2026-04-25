# ml/pipelines/filters/eia_filter.py

def filter_eia(data):
    """
    Extract oil / energy macro signals
    """

    return {
        "oil_price": data.get("brent_price"),
        "timestamp": data.get("timestamp")
    }