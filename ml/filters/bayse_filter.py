def filter_bayse(events):

    cleaned = []

    for e in events["events"]:

        # collapse markets into single signal
        probs = [m["outcome1Price"] for m in e.get("markets", [])]

        if not probs:
            continue

        cleaned.append({
            "prob": probs[0],
            "volume": e.get("liquidity", 0),
            "category": e.get("category"),
            "title": e.get("description"),
        })

    return cleaned