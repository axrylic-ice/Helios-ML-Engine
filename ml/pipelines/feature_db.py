import sqlite3
import pandas as pd

class FeatureDB:

    def __init__(self, path="models/features.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS feature_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            PPoly REAL,
            PBayse REAL,
            SNews REAL,
            OBrent REAL,
            XOfficial REAL,
            XParallel REAL,
            XSpread REAL,
            MGDP REAL,
            MCPI REAL,
            MRes REAL,
            MDebt REAL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert(self, row: dict, timestamp: str):
        cols = ",".join(row.keys())
        vals = tuple(row.values())

        query = f"""
        INSERT INTO feature_store (timestamp, {cols})
        VALUES (?, {','.join(['?'] * len(row))})
        """

        self.conn.execute(query, (timestamp, *vals))
        self.conn.commit()

    def load_last_n(self, n=30):
        df = pd.read_sql_query(
            f"SELECT * FROM feature_store ORDER BY id DESC LIMIT {n}",
            self.conn
        )

        return df.sort_values("id")