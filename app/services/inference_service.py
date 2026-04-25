import joblib
import pandas as pd
from app.services.feature_builder import build_features
from app.services.decision_engine import make_decision

MODEL_PATH = "ml/registry/latest_model.pkl"

model = joblib.load(MODEL_PATH)

def run_inference():
    features = build_features()

    df = pd.DataFrame([features])

    prob = model.predict_proba(df)[0][1]

    decision = make_decision(prob, features)

    return {
        "probability": float(prob),
        **decision
    }