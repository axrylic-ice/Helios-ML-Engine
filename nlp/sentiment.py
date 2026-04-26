from transformers import pipeline
import numpy as np

sent_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")


def aggregate_news(news_list):

    if not news_list:
        return 0

    texts = [n["title"] for n in news_list]

    results = sent_model(texts)

    scores = []

    for r in results:
        if r["label"] == "positive":
            scores.append(r["score"])
        elif r["label"] == "negative":
            scores.append(-r["score"])
        else:
            scores.append(0)

    return float(np.mean(scores))