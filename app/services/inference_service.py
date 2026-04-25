import random
from app.services.feature_builder import build_features
from app.services.decision_engine import make_decision

def run_inference():

    # Step 1: Build features
    features = build_features()

    # Step 2: MOCK MODEL OUTPUT (replace later with real ML model)
    probability = random.uniform(0.5, 0.9)

    # Step 3: Decision logic
    decision = make_decision(probability, features)

    return {
        "fx_spike_probability": round(probability, 3),
        "features": features,
        "decision": decision
    }