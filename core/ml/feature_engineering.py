import pandas as pd
from core.indicators.technical import rsi, macd, bollinger_bands, stochastic, ichimoku, atr, adx, obv

FEATURE_COLS = [
    'rsi', 'macd', 'macd_signal', 'macd_hist',
    'bb_upper', 'bb_lower', 'stoch_k', 'stoch_d',
    'tenkan', 'kijun', 'senkou_a', 'senkou_b',
    'atr', 'adx', 'plus_di', 'minus_di', 'obv',
    'returns', 'volatility'
]

def create_features(df, include_target=True):
    df = df.copy()
    df['rsi'] = rsi(df['close'])
    df['macd'], df['macd_signal'], df['macd_hist'] = macd(df['close'])
    df['bb_upper'], df['bb_mid'], df['bb_lower'] = bollinger_bands(df['close'])
    df['stoch_k'], df['stoch_d'] = stochastic(df)
    df['tenkan'], df['kijun'], df['senkou_a'], df['senkou_b'] = ichimoku(df)
    df['atr'] = atr(df)
    df['adx'], df['plus_di'], df['minus_di'] = adx(df)
    df['obv'] = obv(df)
    df['returns'] = df['close'].pct_change()
    df['volatility'] = df['returns'].rolling(20).std()
    if include_target:
        df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
        df.dropna(inplace=True)
    else:
        df.dropna(subset=FEATURE_COLS, inplace=True)
    return df
