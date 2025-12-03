import pandas as pd
df = pd.read_parquet("data/DATA1/orders.parquet")
print(df.head(20).to_markdown())
print(df.shape)
print(df['unit_price'].unique()[:30])  # to see price formats
print(df['timestamp'].unique()[:20])