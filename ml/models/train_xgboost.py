import xgboost as xgb
import joblib

def train_xgboost(X_train, y_train):
    # Optimized for Nigerian market volatility
    model = xgb.XGBClassifier(
        n_estimators=500,
        max_depth=5,
        learning_rate=0.05,
        objective='binary:logistic',
        tree_method='hist' # Faster training
    )
    
    model.fit(X_train, y_train)
    joblib.dump(model, 'ml/models/weights/xgb_helios.pkl')
    return model

def get_xgb_prediction(data_row):
    model = joblib.load('ml/models/weights/xgb_helios.pkl')
    # Returns probability of devaluation
    return model.predict_proba(data_row)[:, 1]
