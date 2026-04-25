import requests

POLY_URL = "https://gamma-api.polymarket.com/markets"

def get_polymarket_data():

    try:
        response = requests.get(POLY_URL, timeout=10)
        data = response.json()

        # FIX: handle LIST directly
        if isinstance(data, list):
            markets = data
        else:
            markets = data.get("markets", [])

        cleaned = []

        for item in markets[:20]:

            cleaned.append({
                "market": item.get("question") or item.get("title"),
                "volume": item.get("volume", 0),
                "category": item.get("category"),
            })

        return cleaned

    except Exception as e:
        return {"error": str(e)}