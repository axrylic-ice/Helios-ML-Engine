import joblib
from tensorflow.keras.models import load_model
import numpy as np

class HeliosMetaLearner:
    def __init__(self):
        self.xgb = joblib.load('ml/models/weights/xgb_helios.pkl')
        self.lstm = load_model('ml/models/weights/lstm_helios.h5')

    def generate_signal(self, current_features, sequence_7d):
        """
        current_features: shape (1, 11) -> For XGBoost
        sequence_7d: shape (1, 7, 11)   -> For LSTM
        """
        prob_xgb = self.xgb.predict_proba(current_features)[:, 1]
        prob_lstm = self.lstm.predict(sequence_7d).flatten()

        # Meta-Weighted Score
        # We weight the LSTM higher for 'Momentum' and XGB for 'Fundamentals'
        combined_score = (prob_xgb * 0.4) + (prob_lstm * 0.6)

        # Decision Logic
        if combined_score > 0.75:
            return {"action": "ACT", "confidence": combined_score, "risk": "CRITICAL"}
        elif combined_score > 0.50:
            return {"action": "ACT", "confidence": combined_score, "risk": "MODERATE"}
        else:
            return {"action": "WAIT", "confidence": combined_score, "risk": "LOW"}

# Example Usage:
# radar = HeliosMetaLearner()
# print(radar.generate_signal(latest_row, last_week_block))