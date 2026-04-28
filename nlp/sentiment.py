from transformers import pipeline
import numpy as np

sent_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")

signals = []


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

        scored.append(
            {
                "text": texts[i],
                "label": r["label"],
                "description": r["description"],
                "score": float(score),
                "confidence": float(r["score"]),
            }
        )

    # main aggregated sentiment (UNCHANGED LOGIC)
    avg_score = float(np.mean([x["score"] for x in scored]))

    # top 3 by absolute confidence
    signals.extend(sorted(scored, key=lambda x: x["confidence"], reverse=True)[:3])
    
    print(signals)

    return avg_score
