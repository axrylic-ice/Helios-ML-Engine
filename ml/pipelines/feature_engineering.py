def build_features(df):
    X = df.drop(columns=["target"])
    y = df["target"]
    return X, y