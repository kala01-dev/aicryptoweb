import os
import pandas as pd
import numpy as np
import joblib

from core.indicators.technical import (rsi, macd, bollinger_bands, stochastic, ichimoku,
                                       atr, adx, obv, find_support_resistance)
from core.indicators.fibonacci import fibonacci_retracement, fibonacci_extension
from core.indicators.pivot import pivot_classic, pivot_camarilla
from core.fundamental.coingecko import get_fundamental_score
from core.sentiment.micro.news import get_news_sentiment_score
from core.ml.feature_engineering import FEATURE_COLS, create_features
from core.ml.predict import get_ml_probability
from core.signals.scorer import combine_scores
from config.settings import (WEIGHT_TECHNICAL, WEIGHT_FUNDAMENTAL, WEIGHT_NEWS,
                             STRONG_BUY_THRESHOLD, STRONG_SELL_THRESHOLD)

def calculate_technical_score(df):
    score = 50
    signals = []
    # RSI
    rsi_val = rsi(df['close']).iloc[-1]
    if rsi_val < 30:
        score += 15
        signals.append(f"RSI Oversold ({rsi_val:.1f}) - Bullish")
    elif rsi_val > 70:
        score -= 15
        signals.append(f"RSI Overbought ({rsi_val:.1f}) - Bearish")
    else:
        signals.append(f"RSI Netral ({rsi_val:.1f})")
    # MACD
    macd_line, signal_line, hist = macd(df['close'])
    if macd_line.iloc[-1] > signal_line.iloc[-1] and hist.iloc[-1] > 0:
        score += 15
        signals.append("MACD Bullish")
    elif macd_line.iloc[-1] < signal_line.iloc[-1] and hist.iloc[-1] < 0:
        score -= 15
        signals.append("MACD Bearish")
    # Bollinger
    upper, mid, lower = bollinger_bands(df['close'])
    close = df['close'].iloc[-1]
    if close < lower.iloc[-1]:
        score += 10
        signals.append("Di bawah Lower Bollinger - Bullish")
    elif close > upper.iloc[-1]:
        score -= 10
        signals.append("Di atas Upper Bollinger - Bearish")
    # Stochastic
    k, d = stochastic(df)
    if k.iloc[-1] < 20 and d.iloc[-1] < 20:
        score += 10
        signals.append("Stochastic Oversold - Bullish")
    elif k.iloc[-1] > 80 and d.iloc[-1] > 80:
        score -= 10
        signals.append("Stochastic Overbought - Bearish")
    # Ichimoku
    tenkan, kijun, senkou_a, senkou_b = ichimoku(df)
    cloud_top = max(senkou_a.iloc[-1], senkou_b.iloc[-1])
    cloud_bottom = min(senkou_a.iloc[-1], senkou_b.iloc[-1])
    if close > cloud_top:
        score += 10
        signals.append("Harga di atas Cloud - Bullish")
    elif close < cloud_bottom:
        score -= 10
        signals.append("Harga di bawah Cloud - Bearish")
    # ADX
    adx_val, plus_di, minus_di = adx(df)
    if adx_val.iloc[-1] > 25:
        if plus_di.iloc[-1] > minus_di.iloc[-1]:
            score += 10
            signals.append(f"ADX {adx_val.iloc[-1]:.1f} - Tren Naik Kuat")
        else:
            score -= 10
            signals.append(f"ADX {adx_val.iloc[-1]:.1f} - Tren Turun Kuat")
    # OBV
    obv_series = obv(df)
    if len(obv_series) > 5:
        if obv_series.iloc[-1] > obv_series.iloc[-5]:
            score += 5
            signals.append("OBV naik - Akumulasi")
        else:
            score -= 5
            signals.append("OBV turun - Distribusi")
    score = max(0, min(100, score))
    return score, signals

def generate_signal(symbol, coingecko_id, df, fund_score=None, news_score=None):
    tech_score, tech_signals = calculate_technical_score(df)
    if fund_score is None:
        fund_score = get_fundamental_score(coingecko_id)
    if news_score is None:
        news_score, relevant_news = get_news_sentiment_score(symbol)
    else:
        _, relevant_news = get_news_sentiment_score(symbol)

    ml_prob = get_ml_probability(symbol, df)
    total = combine_scores(tech_score, fund_score, news_score, ml_prob)

    if total >= STRONG_BUY_THRESHOLD:
        signal = "STRONG BUY"
    elif total >= 60:
        signal = "BUY"
    elif total <= 100 - STRONG_SELL_THRESHOLD:
        signal = "STRONG SELL"
    elif total <= 40:
        signal = "SELL"
    else:
        signal = "NEUTRAL"

    fib_retrace, swing_high, swing_low = fibonacci_retracement(df)
    fib_ext = fibonacci_extension(df)
    pivot_classic_data = pivot_classic(df)
    pivot_camarilla_data = pivot_camarilla(df)
    support_resistance = find_support_resistance(df)

    return {
        'symbol': symbol,
        'coingecko_id': coingecko_id,
        'current_price': df['close'].iloc[-1],
        'signal': signal,
        'total_score': total,
        'tech_score': tech_score,
        'fund_score': fund_score,
        'news_score': news_score,
        'ml_prob': ml_prob,
        'tech_signals': tech_signals,
        'fib_retrace': fib_retrace,
        'fib_ext': fib_ext,
        'swing_high': swing_high,
        'swing_low': swing_low,
        'pivot_classic': pivot_classic_data,
        'pivot_camarilla': pivot_camarilla_data,
        'support_resistance': support_resistance,
        'news': relevant_news
    }
