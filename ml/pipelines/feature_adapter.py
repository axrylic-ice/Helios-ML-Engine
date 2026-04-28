from ml.pipelines.feature_engineering import FeatureEngine


class FeatureAdapter:

    def __init__(self):
        self.engine = None

    def build(self, signals):

        self.engine = FeatureEngine(signals)

        f = self.engine.build()

        return {
            "PPoly": f["PPoly"],
            "PBayse": f["PBayse"],
            "SNews": f["SNews"],
            "OBrent": f["OBrent"],
            "XOfficial": f["XOfficial"],
            "XParallel": f["XParallel"],
            "XSpread": f["XSpread"],
            "MGDP": f["MGDP"],
            "MCPI": f["MCPI"],
            "MRes": f["MRes"],
            "MDebt": f["MDebt"]
        }