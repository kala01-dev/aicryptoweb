def pivot_classic(df):
    prev = df.iloc[-2]
    p = (prev['high'] + prev['low'] + prev['close']) / 3
    r1 = 2 * p - prev['low']
    s1 = 2 * p - prev['high']
    r2 = p + (prev['high'] - prev['low'])
    s2 = p - (prev['high'] - prev['low'])
    r3 = prev['high'] + 2 * (p - prev['low'])
    s3 = prev['low'] - 2 * (prev['high'] - p)
    return {'pivot': p, 'r1': r1, 's1': s1, 'r2': r2, 's2': s2, 'r3': r3, 's3': s3}

def pivot_camarilla(df):
    prev = df.iloc[-2]
    h, l, c = prev['high'], prev['low'], prev['close']
    r1 = c + (h - l) * 1.1 / 12
    s1 = c - (h - l) * 1.1 / 12
    r2 = c + (h - l) * 1.1 / 6
    s2 = c - (h - l) * 1.1 / 6
    r3 = c + (h - l) * 1.1 / 4
    s3 = c - (h - l) * 1.1 / 4
    return {'r1': r1, 's1': s1, 'r2': r2, 's2': s2, 'r3': r3, 's3': s3}
