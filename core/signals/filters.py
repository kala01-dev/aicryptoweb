def filter_by_min_volume(df_tickers, min_volume=1_000_000):
    return df_tickers[df_tickers['quoteVolume'] >= min_volume]

def filter_by_confidence(signals, min_confidence=60):
    return [s for s in signals if s['total_score'] >= min_confidence]
