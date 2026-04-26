import os
import xgboost as xgb
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score


class FXXGBoostModel:
    def __init__(self):
        self.model = xgb.XGBClassifier(
            n_estimators=1000,
            max_depth=5,
            learning_rate=0.02,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            gamma=0.1,
            min_child_weight=3,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1
        )

        self.feature_cols = None

    # -----------------------------
    # FEATURE ENGINEERING
    # -----------------------------
    def build_features(self, df: pd.DataFrame):
        df = df.copy()

        # --- core engineered signals ---
        df["spread_pressure"] = df["XParallel"] - df["XOfficial"]
        df["fx_divergence"] = df["XParallel"] / (df["XOfficial"] + 1e-6)

        df["inflation_shock"] = df["MCPI"].diff().fillna(0)
        df["reserve_stress"] = df["MDebt"] / (df["MRes"] + 1e-6)

        # --- momentum features (VERY IMPORTANT) ---
        df["oil_momentum"] = df["OBrent"].pct_change().fillna(0)
        df["fx_momentum"] = df["XOfficial"].pct_change().fillna(0)
        df["spread_change"] = df["XSpread"].diff().fillna(0)

        # --- rolling features ---
        df["news_mean_7"] = df["SNews"].rolling(7).mean().fillna(0)
        df["news_vol_7"] = df["SNews"].rolling(7).std().fillna(0)

        self.feature_cols = [
            "PPoly", "PBayse", "SNews",
            "OBrent", "XOfficial", "XParallel", "XSpread",
            "MGDP", "MCPI", "MRes", "MDebt",

            "spread_pressure", "fx_divergence",
            "inflation_shock", "reserve_stress",

            "oil_momentum", "fx_momentum", "spread_change",
            "news_mean_7", "news_vol_7"
        ]

        return df[self.feature_cols].replace([float("inf"), -float("inf")], 0).fillna(0)

    # -----------------------------
    # TRAIN
    # -----------------------------
    def train(self, df, target_col="y_up"):
        X = self.build_features(df)
        y = df[target_col]

        # time-based split (NO SHUFFLE)
        split = int(len(X) * 0.8)

        X_train, X_val = X[:split], X[split:]
        y_train, y_val = y[:split], y[split:]

        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )

        # evaluation
        preds = self.model.predict(X_val)
        probs = self.model.predict_proba(X_val)[:, 1]

        acc = accuracy_score(y_val, preds)
        auc = roc_auc_score(y_val, probs)

        print(f"[XGBoost Accuracy]: {acc:.4f}")
        print(f"[XGBoost AUC]: {auc:.4f}")

    # -----------------------------
    # PREDICT
    # -----------------------------
    def predict(self, df):
        X = self.build_features(df)

        prob = self.model.predict_proba(X)[:, 1]

        return {
            "prob_up": prob
        }

    # -----------------------------
    # SAVE / LOAD
    # -----------------------------
    def save(self, path="ml/models/weights/xgb_model.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save_model(path)

    def load(self, path="ml/models/weights/xgb_model.json"):
        self.model.load_model(path)