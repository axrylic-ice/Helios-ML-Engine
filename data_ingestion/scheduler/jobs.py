from data_ingestion.apis.fixer_api import get_fx_rates
from data_ingestion.apis.polymarket_api import get_polymarket_data
from data_ingestion.apis.news_api import get_news
from data_ingestion.apis.bayse_api import get_bayse_events
from data_ingestion.scrapers.nairatoday_scraper import get_nairatoday_rates
from data_ingestion.apis.eia_api import get_oil_data


def collect_all_data():

    fx_global = get_fx_rates()
    poly = get_polymarket_data()
    news = get_news()
    bayse = get_bayse_events()
    naira_local = get_nairatoday_rates()
    eia = get_oil_data()

    return {
        "fx_global": fx_global,
        "polymarket": poly,
        "bayse": bayse,
        "news": news,
        "naira_local": naira_local,
        "eia": eia
    }
    
if __name__ == "__main__":
    collect_all_data()