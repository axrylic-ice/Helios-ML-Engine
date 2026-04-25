from ml.pipelines.standardizer import standardize_all
from ml.pipelines.filter_pipeline import run_filter_pipeline
from ml.pipelines.normalizer import normalize_signals


def test_normalizer():

    filtered = run_filter_pipeline()
    standardized = standardize_all(filtered)
    normalized = normalize_signals(standardized)

    print("\nSAMPLE NORMALIZED SIGNALS:\n")
    for s in normalized[:10]:
        print(s)

    # sanity checks
    for s in normalized:

        assert 0.0 <= s["value"] <= 1.0 or s["source"] == "news"

    print("\nNORMALIZER OK")
test_normalizer()