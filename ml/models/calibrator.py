import joblib
from sklearn.linear_model import LogisticRegression


class FXCalibrator:
    def __init__(self):
        self.model = LogisticRegression()
        self.fitted = False

    def fit(self, probs, y):
        probs = probs.reshape(-1, 1)
        self.model.fit(probs, y)
        self.fitted = True

    def transform(self, probs):
        if not self.fitted:
            raise Exception("Calibrator not fitted")

        probs = probs.reshape(-1, 1)
        return self.model.predict_proba(probs)[:, 1]

    def save(self, path="ml/models/weights/calibrator.pkl"):
        joblib.dump(self.model, path)

    def load(self, path="ml/models/weights/calibrator.pkl"):
        self.model = joblib.load(path)
        self.fitted = True