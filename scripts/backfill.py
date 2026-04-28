import pandas as pd
from ml.db.store import FeatureStore


class BackfillDB:

    def __init__(self):
        self.store = FeatureStore()

    def run(self, df: pd.DataFrame):

        df = df.sort_values("Timestamp").reset_index(drop=True)

        for _, row in df.iterrows():

            features = {
                "PPoly": row["PPoly"],
                "PBayse": row["PBayse"],
                "SNews": row["SNews"],

                "XOfficial": row["XOfficial"],
                "XParallel": row["XParallel"],
                "XSpread": row["XSpread"],

                "OBrent": row["OBrent"],

                "MGDP": row["MGDP"],
                "MCPI": row["MCPI"],
                "MRes": row["MRes"],
                "MDebt": row["MDebt"],
            }

            target = int(row["y_up"]) if "y_up" in row else None

            self.store.save_row(features, target)

        print("✅ BACKFILL COMPLETE (RAW → DB FEATURE STORE)")