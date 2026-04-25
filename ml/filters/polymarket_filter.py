def filter_polymarket(data):
    """
    Extract only probability + volume signals from Polymarket
    Handles BOTH list and dict responses safely
    """

    cleaned = []

    # 🔧 handle response shape properly
    if isinstance(data, list):
        events = data
    elif isinstance(data, dict):
        events = data.get("events", [])
    else:
        return []

    for event in events:

        # 🔧 safer probability extraction (Gamma is inconsistent)
        prob = (
            event.get("probability")
            or (event.get("outcomePrices")[0] if event.get("outcomePrices") else None)
            or event.get("yesPrice")
        )

        cleaned.append({
            "prob": prob,
            "volume": event.get("volume", 0),
            "category": event.get("category"),
            "title": event.get("question") or event.get("title")
        })

    return cleaned