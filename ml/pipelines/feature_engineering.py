from ml.pipelines.market_aggregator import aggregate_market
from nlp.sentiment import aggregate_news


class FeatureEngine:

    def __init__(self, signals):
        self.signals = signals

    # -------------------------
    # HELPERS (CRITICAL)
    # -------------------------
    def _get(self, source, ctx_key=None, ctx_val=None):

        results = []

        for s in self.signals:
            if s["source"] != source:
                continue

            if ctx_key:
                if s.get("context", {}).get(ctx_key) != ctx_val:
                    continue

            results.append(s)

        return results

    # =========================
    # A. MARKET EXPECTATIONS
    # =========================
    def market_expectations(self):

        poly = self._get("polymarket")
        bayse = self._get("bayse")

        poly_events = [
            {
                "title": s["context"].get("title"),
                "probability": s["value"],
                "volume": s["context"].get("volume", 1)
            }
            for s in poly
        ]

        bayse_events = [
            {
                "title": s["context"].get("title"),
                "probability": s["value"],
                "volume": s["context"].get("volume", 1)
            }
            for s in bayse
        ]

        ppoly = aggregate_market(poly_events)
        pbayse = aggregate_market(bayse_events)

        return {
            "PPoly": ppoly,
            "PBayse": pbayse,
            "divergence": ppoly - pbayse,
            "avg_expectation": (ppoly + pbayse) / 2
        }

    # =========================
    # B. SENTIMENT
    # =========================
    def sentiment(self):

        news = self._get("news")

        news_list = [
            {"title": s["context"].get("title")}
            for s in news
        ]

        snews = aggregate_news(news_list)

        return {
            "SNews": snews
        }

    # =========================
    # C. FX STRUCTURE
    # =========================
    def fx_structure(self):

        official = self._get("fx", "type", "official")
        parallel = self._get("naira", "type", "parallel")

        x_off = official[0]["value"] if official else 0
        x_par = parallel[0]["value"] if parallel else 0

        spread = x_par - x_off
        stress = x_par / x_off if x_off != 0 else 0

        return {
            "XOfficial": x_off,
            "XParallel": x_par,
            "XSpread": spread,
            "FXStress": stress
        }

    # =========================
    # D. MACRO
    # =========================
    def macro(self):

        mgdp = 3.2
        mcpi = [20, 25]
        mres = 50
        mdebt = 100

        inflation_shock = mcpi[-1] - mcpi[-2]
        reserve_stress = mdebt / mres if mres != 0 else 0

        return {
            "MGDP": mgdp,
            "inflation_shock": inflation_shock,
            "reserve_stress": reserve_stress
        }

    # =========================
    # E. COMMODITY
    # =========================
    def commodity(self):

        oil = self._get("eia")

        obr = oil[0]["value"] if oil else 0

        return {
            "OBrent": obr,
            "oil_pressure": (80 - obr) / 80
        }

    # =========================
    # FINAL
    # =========================
    def build(self):

        features = {}

        features.update(self.market_expectations())
        features.update(self.sentiment())
        features.update(self.fx_structure())
        features.update(self.macro())
        features.update(self.commodity())

        return features