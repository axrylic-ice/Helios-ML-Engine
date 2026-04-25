import requests
from bs4 import BeautifulSoup
import json

def get_nairatoday_rates():

    url = "https://nairatoday.com/black-market-usd-ngn-2"

    html = requests.get(url, timeout=10).text

    soup = BeautifulSoup(html, "html.parser")

    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            data = json.loads(script.string)

            # Case 1: direct ExchangeRateSpecification
            if data.get("@type") == "ExchangeRateSpecification":
                return {
                    "usd_ngn": data["currentExchangeRate"]["price"],
                    "source": "nairatoday"
                }

            # Case 2: list structure (sometimes happens)
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "ExchangeRateSpecification":
                        return {
                            "usd_ngn": item["currentExchangeRate"]["price"],
                            "source": "nairatoday"
                        }

        except:
            continue

    return {
        "usd_ngn": None,
        "error": "not found"
    }