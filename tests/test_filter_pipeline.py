from ml.pipelines.filter_pipeline import run_filter_pipeline


def test_filter_pipeline():

    data = run_filter_pipeline()

    print("\n===== FILTERED BAYSE =====")
    print(data["bayse"][:3])  # preview

    print("\n===== FILTERED FX =====")
    print(data["fx"])

    print("\n===== FILTERED NEWS =====")
    print(data["news"][:3])

    print("\n===== EIA =====")
    print(data["eia"])
    
    print("\n===== POLYMARKET =====")
    print(data["polymarket"][:3])

test_filter_pipeline()