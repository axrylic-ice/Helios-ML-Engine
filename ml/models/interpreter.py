class FXInterpreter:

    def interpret(self, model_out, features, signals):

        vol = model_out["volatility"]

        # ----------------------------
        # VOLATILITY LEVEL
        # ----------------------------
        if vol > 0.05:
            vol_level = "HIGH"
        elif vol > 0.02:
            vol_level = "MEDIUM"
        else:
            vol_level = "LOW"

        # ----------------------------
        # LIQUIDITY (improved)
        # ----------------------------
        spread = features["XSpread"]
        poly = features["PPoly"]

        if spread > 80 or poly < 0.3:
            liquidity = "LOW"
        elif spread > 30:
            liquidity = "MEDIUM"
        else:
            liquidity = "HIGH"

        # ----------------------------
        # USD FLOW (improved)
        # ----------------------------
        if poly > 0.6 and spread < 30:
            usd_flow = "INFLOW"
        elif poly < 0.4 and spread > 50:
            usd_flow = "OUTFLOW"
        else:
            usd_flow = "NEUTRAL"

        # ----------------------------
        # NEWS SCORING (FIXED)
        # ----------------------------
        impact_score = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}

        news_items = []

        for s in signals:

            title = (s.get("title") or "").lower()

            score = 0
            if "cbn" in title: score += 3
            if "usd" in title: score += 1
            if "inflation" in title: score += 2
            if "rate" in title: score += 2

            if score >= 4:
                impact = "HIGH"
            elif score >= 2:
                impact = "MEDIUM"
            else:
                impact = "LOW"

            news_items.append({
                "headline": title,
                "summary": title[:120],
                "source": s.get("source_name"),
                "url": s.get("url"),
                "impact": impact
            })

        news_items = sorted(
            news_items,
            key=lambda x: impact_score[x["impact"]],
            reverse=True
        )

        # ----------------------------
        # OUTPUT
        # ----------------------------
        return {
            "confidence": model_out["confidence"],
            "decision": model_out["decision"],
            "engine_health": model_out["engine_health"],

            "estimated_devaluation": model_out["estimated_devaluation"],
            "volatility_level": vol_level,
            "liquidity_level": liquidity,
            "usd_flow": usd_flow,

            "polymarket_sentiment": features["PPoly"],

            "x": {
                "parallel": features["XParallel"],
                "official": features["XOfficial"],
                "spread": features["XSpread"]
            },

            "news": news_items[:5],

            "fx_other_pairs": {
                "EURNGN": features["XOfficial"] * 0.91,
                "GBPNGN": features["XOfficial"] * 1.12,
                "AUDNGN": features["XOfficial"] * 0.62
            }
        }