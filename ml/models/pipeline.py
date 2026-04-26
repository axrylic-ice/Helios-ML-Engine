import numpy as np
import os
from ml.models.scaler import FXScaler
from ml.models.train_xgboost import FXXGBoostModel
from ml.models.train_lstm import FXLSTMModel
from ml.models.meta_learner import FXMetaLearner


class FXPipeline:
    def __init__(self):
        self.scaler = FXScaler()
        self.xgb = FXXGBoostModel()
        self.lstm = FXLSTMModel()
        self.meta = FXMetaLearner()

    def train(self, df):

        os.makedirs("models", exist_ok=True)

        numeric_cols = [
            "PPoly","PBayse","SNews","OBrent",
            "XOfficial","XParallel","XSpread",
            "MGDP","MCPI","MRes","MDebt"
        ]

        # SCALE
        df_scaled = self.scaler.fit_transform(df, numeric_cols)
        df_scaled = df_scaled.replace([np.inf, -np.inf], np.nan).fillna(0)

        # -----------------------------
        # XGBOOST
        # -----------------------------
        self.xgb.train(df_scaled, "y_up")
        xgb_probs = self.xgb.predict(df_scaled)["prob_up"]

        # -----------------------------
        # LSTM (VOLATILITY)
        # -----------------------------
        returns = df_scaled["XOfficial"].pct_change().fillna(0)
        vol = returns.rolling(10).std().fillna(0)

        lstm_X, lstm_y = self.lstm.prepare_data(
            df_scaled[numeric_cols].values, vol.values
        )

        self.lstm.train(lstm_X, lstm_y)

        lstm_preds = self.lstm.predict_all(lstm_X)

        # -----------------------------
        # ALIGN ALL MODELS
        # -----------------------------
        offset = self.lstm.time_steps

        xgb_aligned = xgb_probs[offset:]
        raw_ppoly = df_scaled["PPoly"].values[offset:]
        raw_pbayse = df_scaled["PBayse"].values[offset:]
        raw_spread = df_scaled["XSpread"].values[offset:]
        y_meta = df["y_up"].values[offset:]

        lstm_aligned = lstm_preds

        # -----------------------------
        # META TRAINING DATA
        # -----------------------------
        X_meta = np.column_stack([
            xgb_aligned,
            raw_ppoly,
            raw_pbayse,
            raw_spread,
            lstm_aligned
        ])

        self.meta.train(X_meta, y_meta)

        # -----------------------------
        # METRICS
        # -----------------------------
        self.evaluate(y_meta, X_meta)

        print("✅ FULL TRAINING COMPLETE")

    def evaluate(self, y_true, X_meta):
        from sklearn.metrics import accuracy_score

        preds = self.meta.model.predict(X_meta)
        acc = accuracy_score(y_true, preds)

        print(f"[META Accuracy]: {acc:.4f}")

    def run_inference(self, df):

        numeric_cols = [
            "PPoly","PBayse","SNews","OBrent",
            "XOfficial","XParallel","XSpread",
            "MGDP","MCPI","MRes","MDebt"
        ]

        df_scaled = self.scaler.transform(df)
        df_scaled = df_scaled.replace([np.inf, -np.inf], np.nan).fillna(0)

        # XGB
        xgb = self.xgb.predict(df_scaled)["prob_up"][-1]

        # LSTM
        seq = df_scaled[numeric_cols].values[-30:]
        lstm = self.lstm.predict_single(seq)

        # RAW
        ppoly = df_scaled["PPoly"].values[-1]
        pbayse = df_scaled["PBayse"].values[-1]
        spread = df_scaled["XSpread"].values[-1]

        X = np.array([[xgb, ppoly, pbayse, spread, lstm]])

        return self.meta.predict_single(X)

    def save_all(self):
        self.xgb.save()
        self.lstm.save()
        self.meta.save()
        self.scaler.save()

    def load_all(self):
        self.xgb.load()
        self.lstm.load()
        self.meta.load()
        self.scaler.load()