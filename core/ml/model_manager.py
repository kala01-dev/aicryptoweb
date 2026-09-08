import os
import json
import joblib
from config.settings import MODEL_DIR

def save_model(model, symbol):
    path = os.path.join(MODEL_DIR, f'{symbol}_xgb.pkl')
    joblib.dump(model, path)

def load_model(symbol):
    path = os.path.join(MODEL_DIR, f'{symbol}_xgb.pkl')
    if os.path.exists(path):
        return joblib.load(path)
    return None

def get_model_metrics():
    metrics_path = os.path.join(MODEL_DIR, 'metrics.json')
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            return json.load(f)
    return {}
