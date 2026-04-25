# scripts/run_pipeline_check.py

from data_ingestion.apis.fixer_api import get_fx_rates
from data_ingestion.apis.polymarket_api import get_polymarket_data
from data_ingestion.apis.news_api import get_news
from data_ingestion.apis.bayse_api import get_bayse_events
from data_ingestion.apis.eia_api import get_oil_data


from ml.filters.fx_filter import filter_fx
from ml.filters.news_filter import filter_news
from ml.filters.polymarket_filter import filter_polymarket
from ml.filters.eia_filter import filter_eia
from ml.filters.bayse_filter import filter_bayse


def run_fx_test():
    print("\n===== FX FILTER TEST =====")

    raw = get_fx_rates()

    filtered = filter_fx(raw)
    print("FILTERED FX:", filtered)


def run_news_test():
    print("\n===== NEWS FILTER TEST =====")

    raw = get_news()
    print("RAW NEWS COUNT:", len(raw))

    filtered = filter_news(raw)
    print("FILTERED NEWS COUNT:", len(filtered))


def run_polymarket_test():
    print("\n===== POLYMARKET FILTER TEST =====")

    raw = get_polymarket_data()
    # handle both dict and list responses safely

    if isinstance(raw, list):
        raw_events = raw
    else:
        raw_events = raw.get("events", [])

    print("RAW EVENTS COUNT:", len(raw_events))

    filtered = filter_polymarket(raw)
    print("FILTERED COUNT:", len(filtered))


def run_eia_test():
    print("\n===== EIA FILTER TEST =====")

    raw = get_oil_data()

    filtered = filter_eia(raw)
    print("FILTERED EIA:", filtered)


def run_bayse_test():
    print("\n===== BAYSE FILTER TEST =====")

    raw = get_bayse_events()
    print("RAW EVENTS COUNT:", len(raw.get("events", [])))

    filtered = filter_bayse(raw)
    print("FILTERED COUNT:", len(filtered))


if __name__ == "__main__":

    run_fx_test()
    run_news_test()
    run_polymarket_test()
    run_eia_test()
    run_bayse_test()

    print("\n===== PIPELINE CHECK COMPLETE =====")