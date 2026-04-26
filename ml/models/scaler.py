# scaler.py

import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler


class FXScaler:
    def __init__(self):
        self.scaler = StandardScaler()
        self.numeric_cols = None
        self.fitted = False

    def fit(self, df: pd.DataFrame, cols: list):
        """
        Fit scaler ONLY on training data (no leakage)
        """
        self.numeric_cols = cols
        self.scaler.fit(df[cols])
        self.fitted = True

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted:
            raise Exception("Scaler not fitted yet")

        df_copy = df.copy()
        df_copy[self.numeric_cols] = self.scaler.transform(df[self.numeric_cols])
        return df_copy

    def fit_transform(self, df: pd.DataFrame, cols: list) -> pd.DataFrame:
        self.fit(df, cols)
        return self.transform(df)

    def save(self, path="ml/models/weights/fx_scaler.pkl"):
        joblib.dump({
            "scaler": self.scaler,
            "cols": self.numeric_cols
        }, path)

    def load(self, path="ml/models/weights/fx_scaler.pkl"):
        data = joblib.load(path)
        self.scaler = data["scaler"]
        self.numeric_cols = data["cols"]
        self.fitted = True