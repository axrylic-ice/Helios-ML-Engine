import pandas as pd
from sqlalchemy.orm import Session
from ml.db.database import engine
from ml.db.models import FeatureRow
from scripts.backfill import BackfillDB

def seed_if_empty():
    with Session(engine) as session:
        # Check if table has at least 1 row
        exists = session.query(FeatureRow).first()

        if exists:
            print("DB already has data — skipping seed.")
            return

    print("DB is empty — seeding now...")

    df = pd.read_csv("ml/data/features/fx_data.csv")

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values("Timestamp")
    df = df[df["Timestamp"] >= "2021-01-01"]

    df["y_up"] = (df["XOfficial"].shift(-1) > df["XOfficial"]).astype(int)
    df = df.dropna()

    BackfillDB().run(df)


if __name__ == "__main__":
    seed_if_empty()