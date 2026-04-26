import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class FXMetaLearner:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=5,
            random_state=42
        )

    def train(self, X, y):
        self.model.fit(X, y)

    def predict_single(self, X):
        prob = self.model.predict_proba(X)

        if prob.shape[1] == 1:
            p = prob[:, 0]
        else:
            p = prob[:, 1]

        action = (
            "BUY FX" if p > 0.65 else
            "WAIT" if p < 0.4 else
            "HEDGE"
        )

        return {
            "probability": float(p),
            "action": action
        }

    def save(self):
        joblib.dump(self.model, "ml/models/weights/meta.pkl")

    def load(self):
        self.model = joblib.load("ml/models/weights/meta.pkl")