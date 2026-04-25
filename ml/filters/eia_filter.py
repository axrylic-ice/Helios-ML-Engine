# ml/pipelines/filters/eia_filter.py

def filter_eia(data):
    """
    Extract oil / energy macro signals
    """

    return {
        "oil_price": data.get("price"),
        "inventory_change": data.get("inventory"),
        "timestamp": data.get("timestamp")
    }