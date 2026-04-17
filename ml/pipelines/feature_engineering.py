import pandas as pd
import os
from pathlib import Path
from functools import reduce

def create_master_matrix():
    PROCESSED_DIR = Path("ml/data/processed")
    
    def safe_load(file_name, rename_dict):
        path = PROCESSED_DIR / file_name
        if not path.exists(): return None
        
        df = pd.read_csv(path)
        df.columns = [c.lower().strip() for c in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns=rename_dict)
        
        # KEY FIX 1: Aggressive Deduplication before resampling
        df = df.drop_duplicates(subset=['date'])
        
        # KEY FIX 2: If it's the Parallel FX file, stretch it to cover the Daily gaps
        if 'XParallel' in rename_dict.values():
            df = df.set_index('date').resample('D').ffill().reset_index()
            print(f"📈 Expanded XParallel to daily timeline.")
            
        return df

    # 1. Load available files
    df_par = safe_load("cleaned_unofficial_fx.csv", {'xparallel': 'XParallel'})
    df_poly = safe_load("prediction_market_signal.csv", {'market_signal_prob': 'PPoly'})
    df_bayse = safe_load("cleaned_bayse.csv", {'probability': 'PBayse'})
    df_news = safe_load("cleaned_GDELT2.0.csv", {'snews_gdelt': 'SNews'})
    df_oil = safe_load("cleaned_oil_prices.csv", {'obrent': 'OBrent'})
    df_off = safe_load("cleaned_official_fx.csv", {'xofficial': 'XOfficial'})
    df_macro = safe_load("cleaned_macro_setup_fixed.csv", {
        'gdp_value': 'MGDP', 'inflation_pct': 'MCPI',
        'foreign_reserves_usd': 'MRes', 'external_debt_usd': 'MDebt'
    })

    # 2. Filter columns (Keep 'date' + Uppercase features)
    all_dfs = [df_par, df_poly, df_bayse, df_news, df_oil, df_off, df_macro]
    valid_dfs = []
    for df in all_dfs:
        if df is not None:
            cols = [c for c in df.columns if c == 'date' or c.isupper()]
            valid_dfs.append(df[cols])

    if not valid_dfs:
        print("❌ No valid dataframes found.")
        return

    # 3. THE "ANCHOR" MERGE (Crucial)
    # Start with XParallel as the base. We only care about dates where we have an FX price.
    master = valid_dfs[0] 
    for next_df in valid_dfs[1:]:
        # We use 'left' join so we don't create extra empty dates from other files
        master = pd.merge(master, next_df, on='date', how='left')

    # 4. Fill Missing Features and Data Gaps
    desired_features = ['PPoly', 'PBayse', 'SNews', 'OBrent', 'XOfficial', 'XParallel', 'MGDP', 'MCPI', 'MRes', 'MDebt']
    for feat in desired_features:
        if feat not in master.columns:
            master[feat] = 0.0

    # Sort and carry values forward (e.g., Oil price from Friday carries to Sunday)
    master = master.sort_values('date').ffill().bfill()

    # 5. Feature Engineering
    master['XSpread'] = (master['XParallel'] - master['XOfficial']) / (master['XOfficial'] + 0.0001)
    # The target needs a 7-day lead.
    master['target'] = (master['XParallel'].shift(-7) > master['XParallel']).astype(int)

    # 6. Final Save
    # We drop the rows where we can't calculate a target (the last 7 days of the FX data)
    final_cols = ['date'] + desired_features + ['XSpread', 'target']
    master_final = master[final_cols].dropna(subset=['target'])

    if master_final.empty:
        print("❌ Final matrix is empty! Your date ranges do not overlap with XParallel.")
    else:
        output_path = Path("ml/data/features/final_master_matrix.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        master_final.to_csv(output_path, index=False)
        print(f"🚀 Success! Matrix created with {len(master_final)} rows.")
        print(master_final.tail(5))

if __name__ == "__main__":
    create_master_matrix()