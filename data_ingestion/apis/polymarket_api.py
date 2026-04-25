import requests
import json

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
                "category": item.get("label"),
                "probability": parse_outcome_prices(item.get("outcomePrices"))
            })

        return cleaned

    except Exception as e:
        return {"error": str(e)}
    
   

def parse_outcome_prices(raw):

    # step 1: string → python list
    prices = json.loads(raw)

    # step 2: convert strings → floats
    return [float(p) for p in prices]