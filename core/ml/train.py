import os
import json
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from core.data.fetcher import get_klines
from core.ml.feature_engineering import FEATURE_COLS, create_features
from config.settings import COINS, TIMEFRAME, MODEL_DIR

def train_model_for_coin(symbol):
    print(f"Training model untuk {symbol}...")
    df = get_klines(symbol, TIMEFRAME, limit=2000)
    if len(df) < 500:
        print(f"Data {symbol} tidak cukup, skip.")
        return None
    df = create_features(df)
    X = df[FEATURE_COLS]
    y = df['target']
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print(f"{symbol} - Accuracy: {acc:.4f}, F1: {f1:.4f}")
    model_path = os.path.join(MODEL_DIR, f"{symbol}_xgb.pkl")
    joblib.dump(model, model_path)
    return {symbol: {'accuracy': acc, 'f1': f1}}

def train_all():
    metrics = {}
    for coin in COINS:
        try:
            result = train_model_for_coin(coin['symbol'])
            if result:
                metrics.update(result)
        except Exception as e:
            print(f"Gagal melatih {coin['symbol']}: {e}")
    metrics_path = os.path.join(MODEL_DIR, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrik disimpan di {metrics_path}")

if __name__ == "__main__":
    train_all()
