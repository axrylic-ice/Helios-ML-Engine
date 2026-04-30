class FXInterpreter:

    def interpret(self, model_out, features, signals):

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
            for s in signals[:3]
        ]

        # ----------------------------
        # DECISION BASE SIGNAL SCORE (NEW CORE LOGIC)
        # ----------------------------
        estimated_devaluation = model_out.get("estimated_devaluation", 0)

        score = 0

        # FX direction signal
        if estimated_devaluation > 0:
            score += 1
        elif estimated_devaluation < 0:
            score -= 1

        # USD flow signal
        if usd_flow == "INFLOW":
            score += 1
        elif usd_flow == "OUTFLOW":
            score -= 1

        # Liquidity signal (risk adjustment)
        if liquidity == "HIGH":
            score += 1
        elif liquidity == "LOW":
            score -= 1

        # Volatility penalty (risk, not engine health)
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
        # CONFIDENCE (REAL VERSION)
        # ----------------------------
        base_conf = model_out.get("confidence", 0)

        # normalize score influence into confidence boost
        signal_strength = min(1.0, abs(score) / 3)

        confidence = (base_conf * 0.6) + (signal_strength * 0.4)

        # volatility reduces confidence slightly (risk-based, not engine health)
        if vol_level == "HIGH":
            confidence *= 0.85
        elif vol_level == "MEDIUM":
            confidence *= 0.95

        # ----------------------------
        # OUTPUT
        # ----------------------------
        return {
            "confidence": confidence,
            "decision": decision,

            "estimated_devaluation": estimated_devaluation,
            "volatility_level": vol_level,
            "liquidity_level": liquidity,
            "usd_flow": usd_flow,
            "polymarket_sentiment": poly,

            "x": {
                "parallel": features.get("XParallel", 0),
                "official": features.get("XOfficial", 0),
                "spread": spread
            },

            "news": news_items,

            "fx_other_pairs": {
                "EURNGN": features.get("XOfficial", 0) * 0.91,
                "GBPNGN": features.get("XOfficial", 0) * 1.12,
                "AUDNGN": features.get("XOfficial", 0) * 0.62
            }
        }