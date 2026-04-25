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
    