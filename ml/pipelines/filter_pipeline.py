from data_ingestion.scheduler.jobs import collect_all_data

from ml.filters.bayse_filter import filter_bayse
from ml.filters.fx_filter import filter_fx
from ml.filters.news_filter import filter_news
from ml.filters.polymarket_filter import filter_polymarket
from ml.filters.eia_filter import filter_eia
from data_ingestion.scrapers.nairatoday_scraper import get_nairatoday_rates


def run_filter_pipeline():

    raw = collect_all_data()

    filtered = {}

    # --- Bayse ---
    filtered["bayse"] = filter_bayse(raw.get("bayse", {}))

    # --- FX ---
    filtered["fx"] = filter_fx(raw.get("fx_global", {}))

    # --- News ---
    filtered["news"] = filter_news(raw.get("news", []))

    # placeholders (add later)
    filtered["polymarket"] = filter_polymarket(raw.get("polymarket"))
    
    filtered["eia"] = filter_eia(raw.get("eia"))
    
    filtered["nairatoday"] = get_nairatoday_rates()
    

    return filtered