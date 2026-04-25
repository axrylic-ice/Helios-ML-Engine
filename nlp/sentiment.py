from transformers import pipeline

nlp = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def get_sentiment(text):
    result = nlp(text)[0]

    label = result["label"]
    score = result["score"]

    if label == "negative":
        return -score
    elif label == "positive":
        return score
    return 0