import requests

NEWS_API_KEY = "9ef593a798b64ae19dd9e9da75c1f40f"
NEWS_URL = "https://newsapi.org/v2/everything"

def get_news(query="naira OR forex OR inflation"):
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(NEWS_URL, params=params)
    data = response.json()

    articles = data.get("articles", [])

    return [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "description": a["description"],
            "url": a["url"],
            "published": a["publishedAt"]
        }
        for a in articles[:10]
    ]