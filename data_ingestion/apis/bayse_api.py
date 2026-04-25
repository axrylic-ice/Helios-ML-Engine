import requests

BASE_URL = "https://relay.bayse.markets/v1/pm/events"

CATEGORIES = ["finance", "economy", "politics", "crypto"]

def get_bayse_events():

    all_events = []

    for cat in CATEGORIES:

        params = {
            "page": 1,
            "size": 20,
            "category": cat,
            "status": "open",
            "currency": "NGN"
        }

        try:
            res = requests.get(BASE_URL, params=params, timeout=10)
            data = res.json()

            events = data.get("events", [])

            all_events.extend(events)

        except Exception as e:
            continue

    return {
        "source": "bayse",
        "events": all_events
    }
    
def filter_bayse(events):

    cleaned = []

    for e in events["events"]:

        for m in e.get("markets", []):

            cleaned.append({
                "prob": m["outcome1Price"],
                "liquidity": e.get("liquidity", 0),
                "category": e.get("category"),
                "title": e.get("title"),
                "timestamp": e.get("createdAt")
            })

    return cleaned