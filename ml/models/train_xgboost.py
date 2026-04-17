import xgboost as xgb

def train_xgb(X, y):
    model = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6
    )

    model.fit(X, y)
    return model