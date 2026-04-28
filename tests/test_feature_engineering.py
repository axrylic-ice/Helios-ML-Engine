from ml.pipelines.feature_engineering import FeatureEngine


def test_feature_engine():

    signals = [
        {"source": "fx", "value": 1500, "context": {"type": "official"}},
        {"source": "naira", "value": 1700, "context": {"type": "parallel"}},

        {"source": "polymarket", "value": 0.7, "context": {"title": "Naira falls", "volume": 1000}},
        {"source": "bayse", "value": 0.6, "context": {"title": "NGN weakens", "volume": 500}},

        {"source": "news", "value": 0, "context": {"title": "Inflation rises"}},

        {"source": "eia", "value": 75, "context": {}},
    ]

    engine = FeatureEngine(signals)
    features = engine.build()

    print(features)

    assert "PPoly" in features
    assert "SNews" in features
    assert features["XSpread"] == 200
    
test_feature_engine()