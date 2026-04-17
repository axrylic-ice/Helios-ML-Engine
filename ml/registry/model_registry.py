import joblib
import os

MODEL_PATH = "ml/registry/latest_model.pkl"

def save_model(model):
    os.makedirs("ml/registry", exist_ok=True)
    joblib.dump(model, MODEL_PATH)