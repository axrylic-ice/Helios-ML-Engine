from ml.pipelines.data_ingestion import load_data
from ml.pipelines.feature_engineering import build_features
from ml.models.train_xgboost import train_xgb
from ml.registry.model_registry import save_model

def train_pipeline():
    df = load_data()

    X, y = build_features(df)

    model = train_xgb(X, y)

    save_model(model)