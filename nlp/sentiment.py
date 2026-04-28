from transformers import pipeline
import numpy as np

sent_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")


def aggregate_news(news_list):

    if not news_list:
        return 0

    texts = [n["title"] for n in news_list]

    results = sent_model(texts)

    scored = []

    for i, r in enumerate(results):

        if r["label"] == "positive":
            score = r["score"]
        elif r["label"] == "negative":
            score = -r["score"]
        else:
            score = 0

        scored.append({
            "text": texts[i],
            "label": r["label"],
            "score": float(score),
            "confidence": float(r["score"])
        })

    # main aggregated sentiment (UNCHANGED LOGIC)
    avg_score = float(np.mean([x["score"] for x in scored]))

    # top 3 by absolute confidence
    top3 = sorted(
        scored,
        key=lambda x: x["confidence"],
        reverse=True
    )[:3]
    print(top3)

    return avg_score