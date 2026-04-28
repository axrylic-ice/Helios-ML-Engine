import numpy as np
import pandas as pd
from collections import deque
from datetime import datetime

from ml.db.database import DB
from ml.db.repository import FeatureRepo


class FXRuntime:

    def __init__(self, scaler, xgb, lstm, meta, calibrator):

        self.scaler = scaler
        self.xgb = xgb
        self.lstm = lstm
        self.meta = meta
        self.calibrator = calibrator

        self.db = DB()
        self.repo = FeatureRepo(self.db)

        self.buffer = deque(maxlen=30)

        self.cols = [
            "PPoly","PBayse","SNews","OBrent",
            "XOfficial","XParallel","XSpread",
            "MGDP","MCPI","MRes","MDebt"
        ]

    # =====================================================
    # BOOTSTRAP (CRITICAL FIX FOR YOUR PROBLEM)
    # =====================================================
    def bootstrap(self):

        df = self.repo.load_last_n(30)

        if len(df) < 30:
            raise Exception("Not enough DB history for warm start")

        df_scaled = self.scaler.transform(df)
        df_scaled = df_scaled.replace([np.inf, -np.inf], 0)

        self.buffer.clear()

        for row in df_scaled[self.cols].values:
            self.buffer.append(row)

        print("✅ BOOTSTRAP COMPLETE (30-day memory loaded)")

    # =====================================================
    # MAIN INFERENCE
    # =====================================================
    def run(self, feature_row: dict):

        ts = str(datetime.utcnow())

        # 1. STORE
        self.repo.insert(feature_row, ts)

        # 2. SCALE SINGLE ROW
        df = pd.DataFrame([feature_row])
        df_scaled = self.scaler.transform(df)
        df_scaled = df_scaled.replace([np.inf, -np.inf], 0)

        row = df_scaled[self.cols].values[0]

        # 3. UPDATE MEMORY
        self.buffer.append(row)

        # 4. WARMUP CHECK
        if len(self.buffer) < 30:
            return {
                "status": "warming_up",
                "needed": 30 - len(self.buffer)
            }

        # 5. LSTM (sequence)
        seq = np.array(self.buffer).reshape(1, 30, len(self.cols))
        lstm_val = float(self.lstm.model.predict(seq, verbose=0)[0][0])

        # 6. XGB
        xgb_val = self.xgb.predict(df_scaled)["return"][0]

        # 7. META INPUT
        X = np.array([[
            xgb_val,
            lstm_val,
            df_scaled["PPoly"].values[0],
            df_scaled["PBayse"].values[0],
            df_scaled["XSpread"].values[0]
        ]])

        # 8. META
        raw = self.meta.model.predict(X)[0]

        # 9. CALIBRATE
        prob = self.calibrator.transform(np.array([raw]))[0]

        # 10. DECISION
        if prob > 0.01:
            action = "BUY"
        elif prob < -0.01:
            action = "SELL"
        else:
            action = "HOLD"

        return {
            "signal": float(prob),
            "volatility": lstm_val,
            "action": action
        }