import requests

POLY_URL = "https://gamma-api.polymarket.com/markets"

def get_polymarket_data():
    try:
        response = requests.get(POLY_URL)
        data = response.json()

        return [
            {
                "market": item.get("question"),
                "probability": item.get("probability"),
                "volume": item.get("volume"),
            }
            for item in data.get("markets", [])[:2]
        ]

    except Exception as e:
        return {"error": str(e)}