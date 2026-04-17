import pandas as pd
from pathlib import Path

def debug_dates():
    PROCESSED_DIR = Path("ml/data/processed")
    files = ["prediction_market_signal.csv", "cleaned_oil_prices.csv", 
             "cleaned_official_fx.csv", "cleaned_unofficial_fx.csv"]
    
    for f in files:
        path = PROCESSED_DIR / f
        if path.exists():
            df = pd.read_csv(path)
            df['date'] = pd.to_datetime(df['date'])
            print(f"📅 {f}: {df['date'].min().date()} to {df['date'].max().date()} ({len(df)} rows)")

debug_dates()