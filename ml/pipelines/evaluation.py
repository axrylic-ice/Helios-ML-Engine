import numpy as np
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    confusion_matrix,
    log_loss
)


class FXEvaluator:
    def __init__(self):
        pass

    def evaluate_classifier(self, y_true, y_prob, name="MODEL"):
        """
        y_true: (N,)
        y_prob: (N,) probability of class 1
        """

        y_pred = (y_prob > 0.5).astype(int)

        acc = accuracy_score(y_true, y_pred)

        # AUC breaks if only one class exists
        try:
            auc = roc_auc_score(y_true, y_prob)
        except:
            auc = None

        cm = confusion_matrix(y_true, y_pred)

        try:
            ll = log_loss(y_true, y_prob)
        except:
            ll = None

        print(f"\n📊 [{name} EVALUATION]")
        print(f"Accuracy: {acc:.4f}")
        print(f"AUC: {auc}")
        print(f"LogLoss: {ll}")
        print(f"Confusion Matrix:\n{cm}")

        return {
            "accuracy": acc,
            "auc": auc,
            "log_loss": ll,
            "confusion_matrix": cm.tolist()
        }

    def evaluate_meta(self, meta_model, X, y):
        """
        Direct evaluation of meta learner
        """

        prob = meta_model.model.predict_proba(X)[:, 1]

        return self.evaluate_classifier(y, prob, name="META LEARNER")