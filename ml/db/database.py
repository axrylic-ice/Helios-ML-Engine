from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "sqlite:///fx_store.db"

engine = create_engine(DB_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

from ml.db.models import FeatureRow

def get_recent_features(limit=10):

    session = SessionLocal()

    try:
        rows = (
            session.query(FeatureRow)
            .order_by(FeatureRow.timestamp.asc())
            .limit(limit)
            .all()
        )
        return [
            {col.name: getattr(row, col.name)
             for col in row.__table__.columns
             if col.name not in ("id", "timestamp","y_up")}
            for row in rows
        ]

    finally:
        session.close()