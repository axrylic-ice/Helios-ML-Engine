from ml.pipelines.standardizer import standardize_all
from ml.pipelines.filter_pipeline import run_filter_pipeline


def test_standardizer():

    filtered = run_filter_pipeline()

    signals = standardize_all(filtered)

    print("\nTOTAL SIGNALS:", len(signals))

    # ---- STRUCTURE CHECK ----
    for s in signals[:10]:

        assert "source" in s
        assert "timestamp" in s
        assert "signal_type" in s
        assert "value" in s
        assert "context" in s

        assert isinstance(s["context"], dict)
        assert isinstance(s["value"], (int, float))

    # ---- SOURCE CHECK ----
    sources = set([s["source"] for s in signals])
    print("\nSOURCES FOUND:", sources)

    # ---- VALUE CHECK (quick sanity) ----
    for s in signals:

        if s["signal_type"] == "probability":
            assert 0 <= s["value"] <= 1

    print("\nSTANDARDIZER OK")
    
test_standardizer()