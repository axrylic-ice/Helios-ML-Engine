import requests

FIXER_URL = "https://data.fixer.io/api/latest"
API_KEY = "269ee3d7bad196ca67e61144d8dbaf42"

def get_fx_rates(base="USD"):
    params = {
        "access_key": API_KEY,
    }

    response = requests.get(FIXER_URL, params=params)
    data = response.json()

    return {
        "rates": data.get("rates", {}),
        "timestamp": data.get("timestamp")
    }