# ml/pipelines/filters/news_filter.py

KEYWORDS = [
    "inflation", "forex", "ngn", "usd", "fuel", "energy", "subsidy", "exchange",
    "cbn", "interest", "oil", "rate", "dollar"
]

def filter_news(news_list):
    """
    Keep only macro-FX relevant news
    """

    filtered = []

    for n in news_list:

        text = (n.get("title", "") + n.get("source", "")).lower()

        if any(k in text for k in KEYWORDS):
            filtered.append(n)

    return filtered