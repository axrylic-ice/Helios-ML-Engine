import pandas as pd
import time

from ml.pipelines.interpreter import FXInterpreter
from ml.pipelines.filter_pipeline import run_filter_pipeline
from ml.pipelines.standardizer import standardize_all
from ml.pipelines.feature_engineering import FeatureEngine
from ml.pipelines.pipeline import FXPipeline
from scripts.run_training import seed_if_empty
from ml.db.database import get_recent_features
from nlp.sentiment import signals
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "1"   # keep TF, but isolate it
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

class LiveFXSystem:

    def __init__(self, window_size=30):

        self.pipeline = FXPipeline()
        self.pipeline.load_all()

        self.window_size = window_size

    # -------------------------
    # FETCH + PROCESS SIGNALS
    # -------------------------
    def fetch_features(self):

        print ("jolly3")

        # 1. Pull raw data
        filtered = run_filter_pipeline()
        print ("jolly")

        # 2. Standardize
        signals = filtered
        print ("jolly")

        # 3. Feature engineering
        engine = FeatureEngine(signals)
        features = engine.build()
        print ("jolly")

        return features

    def get_history(self, limit=29):
        rows = get_recent_features(limit)

        return rows

    def normalize(self,row):
      FEATURES = [
       "PPoly", "PBayse", "SNews",
       "XOfficial", "XParallel", "XSpread",
       "MGDP", "MCPI", "MRes", "MDebt", "OBrent"]
      return {k: row.get(k, 0) for k in FEATURES} 
        
    def rows_to_dicts(self, rows):
        return [
            {c.name: getattr(r, c.name) for c in r.__table__.columns}
            for r in rows
        ]
    # -------------------------
    # UPDATE STATE + PREDICT
    # -------------------------
    def step(self):
        seed_if_empty()

        print('jolly')

        features = self.fetch_features()
        print(features)
        print('jolly')

        # 2. get history
        prev_rows = self.get_history()
        print(prev_rows[0])
      
        print('jolly')
        rows = [self.normalize(r) for r in prev_rows]
        rows.append(self.normalize(features))
        df = pd.DataFrame(rows)
        print(rows[0])
        df = pd.DataFrame(rows)
        print('jolly')

        # -------------------------
        # MODEL INFERENCE
        # -------------------------
        result = self.pipeline.run_inference(df)
        interpreter = FXInterpreter()

        final = interpreter.interpret(
            model_out=result,
            features=features,
            signals=signals
            )

        return final


# -------------------------
# RUN LOOP
# -------------------------
if __name__ == "__main__":

    system = LiveFXSystem(window_size=30)

    

    try:
        result = system.step()

        if result:
            print("📊 RESULT:", result)
      

    except Exception as e:
         print("❌ ERROR:", e)
         exit()
         

    # adjust frequency (e.g. every 5 mins)
    