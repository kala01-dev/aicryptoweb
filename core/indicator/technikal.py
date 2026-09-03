import pandas as pd
import numpy as np

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def bollinger_bands(series, window=20, num_std=2):
    sma = series.rolling(window).mean()
    std = series.rolling(window).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    return upper, sma, lower

def stochastic(df, k_period=14, d_period=3):
    low_min = df['low'].rolling(k_period).min()
    high_max = df['high'].rolling(k_period).max()
    k = 100 * ((df['close'] - low_min) / (high_max - low_min))
    d = k.rolling(d_period).mean()
    return k, d

def ichimoku(df):
    tenkan = (df['high'].rolling(9).max() + df['low'].rolling(9).min()) / 2
    kijun = (df['high'].rolling(26).max() + df['low'].rolling(26).min()) / 2
    senkou_a = ((tenkan + kijun) / 2).shift(26)
    senkou_b = ((df['high'].rolling(52).max() + df['low'].rolling(52).min()) / 2).shift(26)
    return tenkan, kijun, senkou_a, senkou_b

def atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def adx(df, period=14):
    up_move = df['high'] - df['high'].shift(1)
    down_move = df['low'].shift(1) - df['low']
    plus_dm = pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=df.index)
    minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=df.index)
    tr = atr(df, period) * period
    plus_di = 100 * (plus_dm.rolling(period).sum() / tr)
    minus_di = 100 * (minus_dm.rolling(period).sum() / tr)
    dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di))
    adx = dx.rolling(period).mean()
    return adx, plus_di, minus_di

def obv(df):
    sign = np.sign(df['close'].diff()).fillna(0)
    return (sign * df['volume']).cumsum()

def find_support_resistance(df, lookback=50):
    highs = df['high'].rolling(window=5, center=True).max()
    lows = df['low'].rolling(window=5, center=True).min()
    swing_highs = df[(df['high'] == highs) & (df['high'] > df['high'].shift(1)) & (df['high'] > df['high'].shift(-1))]
    swing_lows = df[(df['low'] == lows) & (df['low'] < df['low'].shift(1)) & (df['low'] < df['low'].shift(-1))]
    levels = []
    for price in pd.concat([swing_highs['high'], swing_lows['low']]):
        if levels:
            found = False
            for i, lvl in enumerate(levels):
                if abs(price - lvl) / lvl < 0.005:
                    levels[i] = (lvl + price) / 2
                    found = True
                    break
            if not found:
                levels.append(price)
        else:
            levels.append(price)
    levels = sorted(levels)
    filtered = []
    for lvl in levels:
        if filtered and abs(lvl - filtered[-1]) / filtered[-1] < 0.005:
            continue
        filtered.append(lvl)
    return filtered
