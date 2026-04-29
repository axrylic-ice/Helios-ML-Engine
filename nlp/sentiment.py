from transformers import pipeline
import numpy as np

sent_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")

# internal store (top signals only)
signals = []


def aggregate_news(news_list):

    if not news_list:
        return 0.0

    texts = [n.get("title", "") for n in news_list]

    results = sent_model(texts)

    scored = []

    for i, r in enumerate(results):

        label = r["label"].lower()

        if label == "positive":
            score = r["score"]
        elif label == "negative":
            score = -r["score"]
        else:
            score = 0.0

        item = {
            "text": texts[i],
            "label": r["label"],
            "score": float(score),
            "confidence": float(r["score"]),

            # ✅ correctly preserved metadata from input
            "description": news_list[i].get("description"),
            "source": news_list[i].get("source"),
            "url": news_list[i].get("url"),
        }

        scored.append(item)

    # -------------------------
    # aggregate sentiment
    # -------------------------
    avg_score = float(np.mean([x["score"] for x in scored]))

    # -------------------------
    # store TOP signals only
    # -------------------------
    top_signals = sorted(
        scored,
        key=lambda x: abs(x["confidence"]),
        reverse=True
    )[:3]

    signals.extend(top_signals)

    return avg_score