import requests
import pandas as pd
import time
from functools import lru_cache

BINANCE_BASE = "https://api.binance.com"
BINANCE_MIRRORS = [
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com",
    "https://api4.binance.com",
]
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

def _binance_request(endpoint, params=None, retries=2):
    urls = [BINANCE_BASE] + BINANCE_MIRRORS
    for url in urls:
        try:
            resp = requests.get(url + endpoint, params=params, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except requests.exceptions.RequestException:
            continue
        time.sleep(0.5)
    raise Exception(f"Binance API gagal: {endpoint}")

def get_klines(symbol, interval='1h', limit=200):
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    data = _binance_request("/api/v3/klines", params)
    df = pd.DataFrame(data, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df.set_index('open_time', inplace=True)
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    return df

def get_24hr_tickers():
    data = _binance_request("/api/v3/ticker/24hr")
    df = pd.DataFrame(data)
    df_usdt = df[df['symbol'].str.endswith('USDT')].copy()
    for col in ['lastPrice', 'quoteVolume', 'priceChangePercent']:
        df_usdt[col] = pd.to_numeric(df_usdt[col], errors='coerce')
    df_usdt = df_usdt.sort_values('quoteVolume', ascending=False)
    return df_usdt.reset_index(drop=True)

@lru_cache(maxsize=32)
def get_coin_market_data(coingecko_id):
    url = f"{COINGECKO_BASE}/coins/{coingecko_id}"
    params = {
        'localization': 'false',
        'tickers': 'false',
        'market_data': 'true',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None
