import numpy as np
import os

from sklearn.metrics import accuracy_score, roc_auc_score

from ml.models.train_xgboost import FXXGBoostModel
from ml.models.train_lstm import FXLSTMModel
from ml.models.meta_learner import FXMetaLearner
from ml.models.scaler import FXScaler
from ml.models.calibrator import FXCalibrator
from ml.pipelines.walk_forward import WalkForwardEngine


class FXPipeline:

    def __init__(self):

        self.scaler = FXScaler()
        self.xgb = FXXGBoostModel()
        self.lstm = FXLSTMModel()
        self.meta = FXMetaLearner()
        self.calibrator = FXCalibrator()

        self.numeric_cols = [
            "PPoly",
            "PBayse",
            "SNews",
            "OBrent",
            "XOfficial",
            "XParallel",
            "XSpread",
            "MGDP",
            "MCPI",
            "MRes",
            "MDebt",
        ]

    # -------------------------
    # META EVALUATION
    # -------------------------
    def evaluate_meta(self, X, y):

        prob = self.meta.model.predict_proba(X)[:, 1]
        pred = (prob > 0.5).astype(int)

        acc = accuracy_score(y, pred)
        auc = roc_auc_score(y, prob)

        print(f"[META ACC]: {acc:.4f}")
        print(f"[META AUC]: {auc:.4f}")

        return {"accuracy": acc, "auc": auc}

    # -------------------------
    # TRAINING
    # -------------------------
    def train(self, df):

        engine = WalkForwardEngine()

        meta_X, meta_y = [], []

        for tr_s, tr_e, te_s, te_e in engine.split(df):

            train_df = df.iloc[tr_s:tr_e].copy()
            test_df = df.iloc[te_s:te_e].copy()

            # ---------------- SCALE ----------------
            self.scaler.fit(train_df, self.numeric_cols)

            train_scaled = self.scaler.transform(train_df)
            test_scaled = self.scaler.transform(test_df)

            train_scaled = train_scaled.replace([np.inf, -np.inf], 0)
            test_scaled = test_scaled.replace([np.inf, -np.inf], 0)

            # ---------------- XGBOOST ----------------
            self.xgb.train(train_scaled, "y_up")

            xgb_prob = self.xgb.predict(test_scaled)["prob_up"]

            # ---------------- LSTM ----------------
            self.lstm.train(
                train_scaled[self.numeric_cols].values,
                train_df["XOfficial"].pct_change().fillna(0).values,
            )

            seq_input = test_scaled[self.numeric_cols].values[-30:]
            seq_input = seq_input.reshape(1, 30, len(self.numeric_cols))

            lstm_pred = self.lstm.model.predict(seq_input, verbose=0)[0][0]

            # ---------------- ALIGN META DATA ----------------
            n = len(test_df)

            xgb_feat = xgb_prob[-n:]
            lstm_feat = np.repeat(lstm_pred, n)

            poly = test_scaled["PPoly"].values[-n:]
            bayse = test_scaled["PBayse"].values[-n:]
            spread = test_scaled["XSpread"].values[-n:]

            X_meta = np.column_stack([xgb_feat, lstm_feat, poly, bayse, spread])

            y_meta = test_df["y_up"].values[-n:]

            meta_X.append(X_meta)
            meta_y.append(y_meta)

        # ---------------- FINAL STACK ----------------
        X_meta = np.vstack(meta_X)
        y_meta = np.concatenate(meta_y)

        # ---------------- META TRAIN ----------------
        self.meta.train(X_meta, y_meta)

        # ---------------- CALIBRATION ----------------
        raw_probs = self.meta.model.predict_proba(X_meta)[:, 1]
        self.calibrator.fit(raw_probs, y_meta)

        # ---------------- EVAL ----------------
        metrics = self.evaluate_meta(X_meta, y_meta)

        print(metrics)
        print("✅ WALK-FORWARD TRAINING COMPLETE")

    # -------------------------
    # INFERENCE
    # -------------------------
    def run_inference(self, df):

        df_scaled = self.scaler.transform(df)
        df_scaled = df_scaled.replace([np.inf, -np.inf], 0)

        # ---------------- XGBOOST ----------------
        xgb_prob = self.xgb.predict(df_scaled)["prob_up"][-1]

        # ---------------- LSTM ----------------
        seq = df_scaled[self.numeric_cols].values[-30:]
        seq = seq.reshape(1, 30, len(self.numeric_cols))

        lstm_pred = float(self.lstm.model.predict(seq, verbose=0)[0][0])

        # ---------------- RAW FEATURES ----------------
        raw = np.array(
            [
                xgb_prob,
                lstm_pred,
                df_scaled["PPoly"].values[-1],
                df_scaled["PBayse"].values[-1],
                df_scaled["XSpread"].values[-1],
            ]
        ).reshape(1, -1)

        # ---------------- META ----------------
        prob = self.meta.model.predict_proba(raw)[:, 1][0]

        # ---------------- CALIBRATION ----------------
        prob = self.calibrator.transform(np.array([prob]))[0]

        # ---------------- DECISION ----------------
        if prob > 0.65:
            action = "BUY FX"
        elif prob < 0.4:
            action = "WAIT"
        else:
            action = "HEDGE"
        edge = prob / lstm_pred if lstm_pred > 0 else 0

        return {
            "confidence": float(abs(edge)),
            "decision": action,
            "engine_health": "GOOD",
            "estimated_devaluation": float(prob),
            "volatility": float(lstm_pred),
                "xgb": float(xgb_prob),
                "lstm": float(lstm_pred),
                "meta": float(prob),
        }

    # -------------------------
    # SAVE / LOAD
    # -------------------------
    def save_all(self):

        os.makedirs("models", exist_ok=True)

        self.xgb.save()
        self.lstm.save()
        self.meta.save()
        self.scaler.save()
        self.calibrator.save("models/calibrator.pkl")

        print("✅ ALL MODELS SAVED")

    def load_all(self):

        os.makedirs("models", exist_ok=True)

        self.xgb.load()
        self.lstm.load()
        self.meta.load()
        self.scaler.load()
        self.calibrator.load()

        print("✅ ALL MODELS SAVED")
