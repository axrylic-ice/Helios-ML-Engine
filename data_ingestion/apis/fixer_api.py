import requests
import os
from dotenv import load_dotenv
load_dotenv()

URL = "https://api.exchangerate.host/live"
API_KEY = os.getenv("FIXER_API_KEY")

store = None  # global shared state

def get_fx_rates():

    global store  # 👈 THIS is what you are missing

    params = {
        "access_key": API_KEY,
        "source": "USD",
        "currencies": "NGN,GBP,EUR,AUD",
        "format": 0
    }

    res = requests.get(URL, params=params, timeout=10)
    data = res.json()

    if not data.get("success"):
        raise Exception(f"FX API error: {data}")

    quotes = data["quotes"]
    timestamp = data["timestamp"]

    usdngn = quotes.get("USDNGN")
    usdgbp = quotes.get("USDGBP")
    usdeur = quotes.get("USDEUR")
    usdaud = quotes.get("USDAUD")

    stored = {
        "GBPNGN": usdngn / usdgbp if usdgbp else 0,
        "EURNGN": usdngn / usdeur if usdeur else 0,
        "AUDNGN": usdngn / usdaud if usdaud else 0,
        "timestamp": timestamp
    }

    # ✅ THIS NOW UPDATES GLOBAL STATE
    store = stored

    if usdngn is None:
        raise Exception("USDNGN missing from response")

    output = {
        "rates": usdngn,
        "timestamp": timestamp
    }

    return output