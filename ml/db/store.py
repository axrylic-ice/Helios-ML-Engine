from ml.db.database import SessionLocal, engine, Base
from ml.db.models import FeatureRow
from sqlalchemy.exc import SQLAlchemyError


Base.metadata.create_all(bind=engine)


class FeatureStore:

    def save_row(self, features: dict, target=None):

        session = SessionLocal()

        try:
            row = FeatureRow(
                PPoly=features.get("PPoly"),
                PBayse=features.get("PBayse"),
                SNews=features.get("SNews"),
                XOfficial=features.get("XOfficial"),
                XParallel=features.get("XParallel"),
                XSpread=features.get("XSpread"),
                OBrent=features.get("OBrent"),
                MGDP=features.get("MGDP"),
                MCPI=features.get("MCPI"),
                MRes=features.get("MRes"),
                MDebt=features.get("MDebt"),
                y_up=features.get("y_up") 
            )

            session.add(row)
            session.commit()

        except SQLAlchemyError as e:
            session.rollback()
            print("DB ERROR:", e)

        finally:
            session.close()

    def load_last_n(self, n=30):

        session = SessionLocal()

        try:
            rows = (
                session.query(FeatureRow)
                .order_by(FeatureRow.timestamp.desc())
                .limit(n)
                .all()
            )

            rows = list(reversed(rows))

            return rows

        finally:
            session.close()