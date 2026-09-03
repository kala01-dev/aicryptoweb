def fibonacci_retracement(df, lookback=100):
    data = df.tail(lookback)
    swing_high = data['high'].max()
    swing_low = data['low'].min()
    diff = swing_high - swing_low
    levels = {
        '0%': swing_high,
        '23.6%': swing_high - 0.236 * diff,
        '38.2%': swing_high - 0.382 * diff,
        '50%': swing_high - 0.5 * diff,
        '61.8%': swing_high - 0.618 * diff,
        '78.6%': swing_high - 0.786 * diff,
        '100%': swing_low,
    }
    return levels, swing_high, swing_low

def fibonacci_extension(df, lookback=100):
    data = df.tail(lookback)
    swing_high = data['high'].max()
    swing_low = data['low'].min()
    diff = swing_high - swing_low
    levels = {
        '0%': swing_high,
        '61.8%': swing_high + 0.618 * diff,
        '100%': swing_high + diff,
        '161.8%': swing_high + 1.618 * diff,
        '261.8%': swing_high + 2.618 * diff,
    }
    return levels
