import pandas as pd
from ml.db.models import FeatureRow


class FeatureRepo:

    def __init__(self, db):
        self.db = db

    # ---------------- SAVE ----------------
    def insert(self, features: dict, timestamp: str):

        session = self.db.session()

        row = FeatureRow(timestamp=timestamp, **features)

        session.add(row)
        session.commit()
        session.close()

    # ---------------- LOAD LAST N DAYS ----------------
    def load_last_n(self, n=30):

        session = self.db.session()

        rows = (
            session.query(FeatureRow)
            .order_by(FeatureRow.id.desc())
            .limit(n)
            .all()
        )

        session.close()

        rows = rows[::-1]

        data = [{
            "PPoly": r.PPoly,
            "PBayse": r.PBayse,
            "SNews": r.SNews,
            "OBrent": r.OBrent,
            "XOfficial": r.XOfficial,
            "XParallel": r.XParallel,
            "XSpread": r.XSpread,
            "MGDP": r.MGDP,
            "MCPI": r.MCPI,
            "MRes": r.MRes,
            "MDebt": r.MDebt,
        } for r in rows]

        return pd.DataFrame(data)