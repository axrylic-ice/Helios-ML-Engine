import requests

NEWSDATA_KEY = "pub_e22c3bae89b2437c83541051b36be701"
CURRENTS_KEY = "JQFdwt-vDePMQM-w_aNt8CBq70Xg7BOmGmqd9rH4CUwlpHTQ"


def fetch_newsdata(query):
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWSDATA_KEY,
        "q": query,
        "country": "ng",
        "language": "en",
    }

    res = requests.get(url, params=params).json()
    articles = res.get("results", [])

    return [
        {
            "title": a.get("title"),
            "source": a.get("source_id"),
            "description": a.get("description"),
            "url": a.get("link"),
            "published": a.get("pubDate")
        }
        for a in articles
    ]


def fetch_currents(query):
    url = "https://api.currentsapi.services/v1/search"
    headers = {"Authorization": CURRENTS_KEY}

    params = {
        "keywords": query,
        "language": "en",
        "country": "NG"
    }

    res = requests.get(url, headers=headers, params=params).json()
    articles = res.get("news", [])

    return [
        {
            "title": a.get("title"),
            "source": a.get("author"),
            "description": a.get("description"),
            "url": a.get("url"),
            "published": a.get("published")
        }
        for a in articles
    ]


def get_news(query="naira OR forex OR inflation"):
    all_articles = []

    try:
        all_articles.extend(fetch_newsdata(query))
    except:
        pass

    try:
        all_articles.extend(fetch_currents(query))
    except:
        pass

    # 🔑 Deduplicate by URL
    seen = set()
    unique = []

    for a in all_articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    # Sort by time (newest first)
    unique.sort(key=lambda x: x["published"] or "", reverse=True)

    return unique[:]