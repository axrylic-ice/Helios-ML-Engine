import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class FXMetaLearner:
    def __init__(self, calibrator=None):
        self.model = RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=5,
            random_state=42
        )

        self.calibrator = calibrator

    def build_features(self, xgb_out, lstm_out, raw):

        return np.column_stack([
            xgb_out["prob_up"],
            raw["PPoly"],
            raw["PBayse"],
            raw["XSpread"],
            np.full(len(xgb_out["prob_up"]), lstm_out["volatility"])
        ])

    def train(self, X, y):
        self.model.fit(X, y)

    # -------------------------
    # DECISION ENGINE (FIXED)
    # -------------------------
    def decision_engine(self, prob):

        if prob > 0.6:
            action = "BUY FX"
        elif prob < 0.4:
            action = "SELL FX"
        else:
            action = "NO TRADE"

        size = self.position_size(prob)

        return {
            "probability": float(prob),
            "action": action,
            "position_size": float(size)
        }

    # -------------------------
    # POSITION SIZING
    # -------------------------
    def position_size(self, prob):
        edge = abs(prob - 0.5) * 2
        return np.clip(edge, 0, 1)

    # -------------------------
    # PREDICT
    # -------------------------
    def predict(self, xgb_out, lstm_out, raw):

        X = self.build_features(xgb_out, lstm_out, raw)

        raw_prob = self.model.predict_proba(X)[:, 1]

        prob = raw_prob

        if self.calibrator is not None:
            prob = self.calibrator.transform(prob.reshape(-1, 1)).flatten()

        return self.decision_engine(prob[0])

    def save(self):
        joblib.dump(self.model, "ml/models/weights/meta.pkl")

    def load(self):
        self.model = joblib.load("ml/models/weights/meta.pkl")