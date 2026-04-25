def filter_bayse(events):

    cleaned = []

    for e in events["events"]:

        # collapse markets into single signal
        probs = [m["outcome1Price"] for m in e.get("markets", [])]

        if not probs:
            continue

        cleaned.append({
            "prob": sum(probs) / len(probs),
            "liquidity": e.get("liquidity", 0),
            "category": e.get("category"),
            "title": e.get("title"),
        })

    return cleaned