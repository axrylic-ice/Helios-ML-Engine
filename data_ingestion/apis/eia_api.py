import requests
from datetime import datetime, timedelta

url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"
API_KEY = "1KhZktcBp8g8yfJ910kv6NwxpU60E4buJEdKrgGy"  # rotate this later

def get_oil_data():

    # --- FIX 1: define time range ---
    end = datetime.utcnow().date()
    start = end - timedelta(days=14)

    params = {
        "api_key": API_KEY,
        "frequency": "daily",
        "data[0]": "value",
        "facets[product][]": "EPCBRENT",

        # time constraint
        "start": str(start),
        "end": str(end),

        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 1
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()

        data = res.json()

        point = data["response"]["data"][0]

        return {
            "brent_price": float(point["value"]),
            "timestamp": point["period"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }