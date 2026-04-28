from sqlalchemy import Column, Integer, Float, DateTime
from ml.db.database import Base
import datetime


class FeatureRow(Base):
    __tablename__ = "feature_rows"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    PPoly = Column(Float)
    PBayse = Column(Float)
    SNews = Column(Float)

    XOfficial = Column(Float)
    XParallel = Column(Float)
    XSpread = Column(Float)

    OBrent = Column(Float)

    MGDP = Column(Float)
    MCPI = Column(Float)
    MRes = Column(Float)
    MDebt = Column(Float)

    y_up = Column(Integer, nullable=True)  # target if training