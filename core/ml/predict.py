import os
import joblib
from core.ml.feature_engineering import create_features, FEATURE_COLS
from config.settings import MODEL_DIR

def load_model_for_symbol(symbol):
    model_path = os.path.join(MODEL_DIR, f'{symbol}_xgb.pkl')
    if os.path.exists(model_path):
        try:
            return joblib.load(model_path)
        except:
            return None
    return None

def get_ml_probability(symbol, df):
    model = load_model_for_symbol(symbol)
    if model is None:
        return 0.5
    df_feat = create_features(df, include_target=False)
    if len(df_feat) == 0:
        return 0.5
    features = df_feat.iloc[-1][FEATURE_COLS].values.reshape(1, -1)
    prob = model.predict_proba(features)[0][1]
    return prob
