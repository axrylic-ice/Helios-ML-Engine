from ml.pipelines.market_aggregator import aggregate_market
from nlp.sentiment import aggregate_news
from datetime import datetime, timezone


class FeatureEngine:

    def __init__(self, raw_data):
        """
        raw_data = {
            "bayse": [...],
            "polymarket": [...],
            "fx": {...},
            "nairatoday": {...},
            "eia": {...},
            "news": [...]
        }
        """
        self.raw = raw_data or {}

    # -------------------------
    # HELPERS (RAW AWARE)
    # -------------------------
    def _safe_float(self, x, default=0.0):
        try:
            return float(x)
        except:
            return default

    # =========================
    # A. MARKET EXPECTATIONS
    # =========================
    def market_expectations(self):

        poly_events = []
        for e in self.raw.get("polymarket", []):
                poly_events.append({
                    "title": e.get("title"),
                    "probability": self._safe_float(e.get("prob")),
                    "volume": self._safe_float(e.get("volume", 1))
                })

        bayse_events = []
        for e in self.raw.get("bayse", []):
      
                bayse_events.append({
                    "title": e.get("title"),
                    "probability": self._safe_float(e.get("prob")),
                    "volume": self._safe_float(e.get("volume", 1))
                })

        return {
            "PPoly": aggregate_market(poly_events) if poly_events else 0,
            "PBayse": aggregate_market(bayse_events) if bayse_events else 0
        }

    # =========================
    # B. SENTIMENT
    # =========================
    def sentiment(self):

        news_list = [
            {"title": n.get("title"),"source": n.get("source"),"description": n.get("description"),"url": n.get("url"),}
            for n in self.raw.get("news", [])
            if n.get("title")
        ]

        return {
            "SNews": aggregate_news(news_list) if news_list else 0
        }

    # =========================
    # C. FX STRUCTURE
    # =========================
    def fx_structure(self):

        fx = self.raw.get("fx", {})
        naira = self.raw.get("nairatoday", {})

        x_off = self._safe_float(fx.get("USD_NGN"))
        x_par = self._safe_float(naira.get("usd_ngn"))

        return {
            "XOfficial": x_off,
            "XParallel": x_par,
            "XSpread": x_par - x_off
        }

    # =========================
    # D. MACRO (still stubbed)
    # =========================
    def macro(self):

        return {
            "MGDP": 3.2,
            "MCPI": 22.5,
            "MRes": 50,
            "MDebt": 100
        }

    # =========================
    # E. COMMODITY (EIA)
    # =========================
    def commodity(self):

        eia = self.raw.get("eia", {})
        oil_price = self._safe_float(eia.get("oil_price"))

        return {
            "OBrent": oil_price,
        }

    # =========================
    # FINAL PIPELINE
    # =========================
    def build(self):

        return {
            **self.market_expectations(),
            **self.sentiment(),
            **self.fx_structure(),
            **self.macro(),
            **self.commodity()
        }