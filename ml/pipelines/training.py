import pandas as pd
from ml.pipelines.pipeline import FXPipeline

df = pd.read_csv("ml/data/features/fx_data.csv")

# ensure datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values("Timestamp")

# start from required date
df = df[df["Timestamp"] >= "2021-02-02"]

# label
df["y_up"] = (df["XOfficial"].shift(-1) > df["XOfficial"]).astype(int)
df = df.dropna()

pipeline = FXPipeline()

pipeline.train(df)
pipeline.save_all()

result = pipeline.run_inference(df)

print(result)