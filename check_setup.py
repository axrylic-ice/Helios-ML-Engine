import pandas as pd

# 1. Load the broken file
df = pd.read_csv("macro_setup.csv", index_col=0, parse_dates=True)

# 2. Fix the 2025/2026 values (Using USD scale, not percentages)
# debt_usd, reserves_usd, inflation_pct
df.loc['2025-01-01'] = [112000000000.0, 42800000000.0, 23.0]
df.loc['2026-01-01'] = [115500000000.0, 44500000000.0, 14.9]

# 3. Save it correctly
df.to_csv("macro_setup_fixed.csv")
print("Data scales aligned. Debt is now in USD across all rows.")