import pandas as pd
import numpy as np
import os
from pathlib import Path

# Setup paths relative to the project root
RAW_DIR = Path("ml/data/raw")
PROCESSED_DIR = Path("ml/data/processed")

def clean_column_names(df):
    """Standardize column names: lowercase, no spaces, no special chars."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('(', '')
        .str.replace(')', '')
    )
    return df

def process_polymarket(file_name):
    print(f"--- Processing {file_name} ---")
    df = pd.read_csv(RAW_DIR / file_name)
    df = clean_column_names(df)
    
    # 1. Clean the messy Volume/Prob columns we fixed earlier
    if 'volume_usd' in df.columns:
        df['volume_usd'] = df['volume_usd'].astype(str).str.replace(r'[$,]', '', regex=True)
        df['volume_usd'] = pd.to_numeric(df['volume_usd'], errors='coerce').fillna(0)
    
    # 2. Standardize Dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date']) # Remove rows with invalid dates
    
    # Save to processed
    output_path = PROCESSED_DIR / f"cleaned_{file_name}"
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

def process_fx_rates(file_name):
    print(f"--- Processing {file_name} ---")
    df = pd.read_csv(RAW_DIR / file_name)
    df = clean_column_names(df)
    
    # Standardize column naming for your specific features
    # Rename 'parallel_rate' to 'xparallel' etc. to match your feature list
    rename_map = {
        'official_rate': 'xofficial',
        'parallel_market': 'xparallel',
        'black_market': 'xparallel',
        'brent_price': 'obrent'
    }
    df = df.rename(columns=rename_map)
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date to ensure time-series integrity
    df = df.sort_values('date')
    
    output_path = PROCESSED_DIR / f"cleaned_{file_name}"
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

def process_unofficial_fx(file_name):
    print(f"--- 🛠️ Converting {file_name} to DAILY Data ---")
    df = pd.read_csv(RAW_DIR / file_name)
    df = clean_column_names(df)
    
    # 1. Standardize and Deduplicate
    df['date'] = pd.to_datetime(df['date']).dt.normalize()
    # Keep the first price for each date, killing the 60+ duplicates
    df = df.drop_duplicates(subset=['date'], keep='first')
    
    # 2. Re-index to a DAILY Calendar
    df = df.set_index('date')
    # This creates a row for every single day (Jan 1, Jan 2, Jan 3...)
    daily_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    
    # 3. Fill the Gaps (The "Daily-fication")
    # .ffill() takes the Jan 1st price and carries it forward to Jan 2nd, 3rd, etc.
    df_daily = df.reindex(daily_index).ffill().reset_index()
    df_daily.rename(columns={'index': 'date', 'close': 'xparallel'}, inplace=True)
    
    # 4. Save only the columns needed for the Master Merge
    df_daily = df_daily[['date', 'xparallel']]
    
    output_path = PROCESSED_DIR / "cleaned_parallel_fx.csv"
    df_daily.to_csv(output_path, index=False)
    print(f"✅ Success! Created {len(df_daily)} daily rows from monthly data.")
    
def process_macro_data(file_name):
    print(f"--- Processing Macro: {file_name} ---")
    df = pd.read_csv(RAW_DIR / file_name)
    df = clean_column_names(df)
    
    # 1. Standardize the Date
    df['date'] = pd.to_datetime(df['date'])
    
    # 2. Force Numeric (Macro data often has 'B' for billion or 'M' for million)
    # This regex removes non-numeric chars except the decimal point
    for col in [c for c in df.columns if c != 'date']:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(r'[^\d.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').ffill()

    # 3. Create Daily Continuity
    # We create a daily date range and join the monthly data to it
    all_dates = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    df = df.set_index('date').reindex(all_dates).ffill().reset_index()
    df.rename(columns={'index': 'date'}, inplace=True)

    output_path = PROCESSED_DIR / f"cleaned_{file_name}"
    df.to_csv(output_path, index=False)
    
def process_gdelt_data(file_name):
    print(f"--- Processing GDELT: {file_name} ---")
    df = pd.read_csv(RAW_DIR / file_name)
    df = clean_column_names(df) # lowercase names
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Feature Coding: 
    # Rename to match your Helios-AiML feature list
    df = df.rename(columns={
        'stability_index': 'sgoldstein', 
        'avg_sentiment': 'snews_gdelt'
    })
    
    # Calculate "Sentiment Momentum" (Is the news getting worse?)
    df['snews_momentum'] = df['snews_gdelt'].diff().fillna(0)
    
    output_path = PROCESSED_DIR / f"cleaned_{file_name}"
    df.to_csv(output_path, index=False)
    print(f"Saved GDELT features to {output_path}")
    
def process_oil_data(file_name):
    print(f"--- Processing Brent: {file_name} ---")
    df = pd.read_csv(RAW_DIR / file_name)
    df = clean_column_names(df)
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.rename(columns={'brent_price': 'obrent'})
    df = df.sort_values('date')

    # 1. Handle Weekend Gaps (Fill Jan 2, 3 with Jan 1's price)
    all_dates = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    df = df.set_index('date').reindex(all_dates).ffill().reset_index()
    df.rename(columns={'index': 'date'}, inplace=True)

    # 2. Mathematical Signals (The 'Shock' features)
    # Log returns capture the percentage move
    df['obrent_return'] = np.log(df['obrent'] / df['obrent'].shift(1)).fillna(0)
    
    # 7-day Volatility: Standard deviation of returns
    # This tells the model if the oil market is "panicking"
    df['obrent_vol_7d'] = df['obrent_return'].rolling(window=7).std().fillna(0)

    output_path = PROCESSED_DIR / f"cleaned_{file_name}"
    df.to_csv(output_path, index=False)
    print(f"Saved Brent features to {output_path}")

def run_ingestion():
    """Main runner to ingest all raw files."""
    # Create directory if it doesn't exist
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # List of your specific files
    files = os.listdir(RAW_DIR)
    
    for f in files:
        if  'polymarket' in f or 'bayse' in f:
            process_polymarket(f)
        elif 'official' in f or 'brent' in f:
            process_fx_rates(f)
        elif 'unofficial' in f:
            process_unofficial_fx(f)
        elif 'macro' in f:
            process_macro_data(f)
        elif 'GDELT' in f:
            process_gdelt_data(f)
        elif 'oil' in f:
            process_oil_data(f)
        else:
            print(f"Skipping unknown file format: {f}")

if __name__ == "__main__":
    run_ingestion()