from data_ingestion.apis.fixer_api import store


class FXInterpreter:

    def interpret(self, model_out, features, signals):

        from data_ingestion.apis.fixer_api import store

        # ----------------------------
        # VOLATILITY LEVEL
        # ----------------------------
        vol = model_out.get("volatility", 0)

        if vol > 0.05:
            vol_level = "HIGH"
        elif vol > 0.02:
            vol_level = "MEDIUM"
        else:
            vol_level = "LOW"

        # ----------------------------
        # LIQUIDITY
        # ----------------------------
        spread = features.get("XSpread", 0)
        poly = features.get("PPoly", 0)

        if spread > 80:
            liquidity = "LOW"
        elif spread > 30:
            liquidity = "MEDIUM"
        else:
            liquidity = "HIGH"

        # ----------------------------
        # USD FLOW
        # ----------------------------
        if poly > 0.6 and spread < 30:
            usd_flow = "INFLOW"
        elif poly < 0.4 and spread > 50:
            usd_flow = "OUTFLOW"
        else:
            usd_flow = "NEUTRAL"

        # ----------------------------
        # NEWS (already structured signals)
        # ----------------------------
        news_items = [
            {
                "headline": s.get("text"),
                "description": s.get("description"),
                "source": s.get("source"),
                "url": s.get("url"),
                "impact": s.get("label")
            }
            for s in signals
        ]

        # =========================================================
        # CORE SIGNAL
        # =========================================================

        # ----------------------------
        # EXPECTED DEVALUATION (%)  ✅ FIXED MEANING
        # ----------------------------
        base_move = vol * 100  # volatility → % move estimate

        spread_factor = min(spread / 50, 2.0)

        if liquidity == "HIGH":
            liq_factor = 0.7
        elif liquidity == "MEDIUM":
            liq_factor = 1.0
        else:
            liq_factor = 1.3

        estimated_devaluation = base_move * spread_factor * liq_factor

        # direction (from model probability)
        direction = model_out.get("direction", 0)  # assume -1, 0, +1 OR similar

        # ----------------------------
        # SCORE
        # ----------------------------
        score = 0

        if direction > 0:
            score += 1
        elif direction < 0:
            score -= 1

        if usd_flow == "INFLOW":
            score += 1
        elif usd_flow == "OUTFLOW":
            score -= 1

        if liquidity == "HIGH":
            score += 1
        elif liquidity == "LOW":
            score -= 1

        if vol_level == "HIGH":
            score -= 1

        # ----------------------------
        # DECISION
        # ----------------------------
        if model_out.get("confidence", 0) < 0.4:
            decision = "WAIT"

        elif score >= 2:
            decision = "BUY_USD"

        elif score <= -2:
            decision = "SELL_USD"

        else:
            decision = "WAIT"

        # ----------------------------
        # CONFIDENCE (STABLE, NO 1.0 SATURATION)
        # ----------------------------
        base_conf = float(model_out.get("confidence", 0))

        signal_votes = 0

        if direction > 0:
            signal_votes += 1
        elif direction < 0:
            signal_votes -= 1

        if usd_flow == "INFLOW":
            signal_votes += 1
        elif usd_flow == "OUTFLOW":
            signal_votes -= 1

        if liquidity == "HIGH":
            signal_votes += 1
        elif liquidity == "LOW":
            signal_votes -= 1

        if vol_level == "HIGH":
            signal_votes -= 1

        agreement = abs(signal_votes) / 3

        confidence = (
            base_conf * 0.5 +
            agreement * 0.3 +
            min(1.0, abs(estimated_devaluation) / 100) * 0.2
        )

        confidence = max(0.05, min(0.95, confidence))

        # ----------------------------
        # OUTPUT
        # ----------------------------
        return {
            "confidence": confidence,
            "decision": decision,

            "estimated_devaluation": estimated_devaluation,  # ✅ % MOVE ONLY

            "volatility_level": vol_level,
            "liquidity_level": liquidity,
            "usd_flow": usd_flow,
            "engine_health": "good",
            "polymarket_sentiment": poly,

            "x": {
                "parallel": features.get("XParallel", 0),
                "official": features.get("XOfficial", 0),
                "spread": spread
            },

            "news": news_items,

            "fx_other_pairs": {
                "EURNGN": store["EURNGN"],
                "GBPNGN": store["GBPNGN"],
                "AUDNGN": store["AUDNGN"]
            }
        }