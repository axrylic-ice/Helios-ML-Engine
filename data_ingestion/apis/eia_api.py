import requests

EIA_URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

API_KEY = "1KhZktcBp8g8yfJ910kv6NwxpU60E4buJEdKrgGy"

def get_oil_data():
    params = {
        "api_key": API_KEY
    }

    try:
        response = requests.get(EIA_URL, params=params)
        return response.json()
    except:
        return {"error": "failed to fetch oil data"}