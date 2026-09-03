import ccxt
import os
import streamlit as st

def _get_env_or_secret(key):
    val = os.getenv(key)
    if val:
        return val
    try:
        return st.secrets[key]
    except:
        return None

def get_binance_client():
    api_key = _get_env_or_secret('BINANCE_API_KEY')
    secret_key = _get_env_or_secret('BINANCE_SECRET_KEY')
    if not api_key or not secret_key:
        return None
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
        'enableRateLimit': True,
    })
    return exchange

def get_account_balance():
    client = get_binance_client()
    if not client:
        return None
    try:
        balance = client.fetch_balance()
        balances = []
        for asset, data in balance['total'].items():
            if data and data > 0:
                balances.append({
                    'asset': asset,
                    'total': data,
                    'free': balance['free'].get(asset, 0),
                    'used': balance['used'].get(asset, 0)
                })
        return balances
    except Exception as e:
        st.error(f"Gagal mengambil saldo: {e}")
        return None

def get_open_orders(symbol=None):
    client = get_binance_client()
    if not client:
        return None
    try:
        if symbol:
            orders = client.fetch_open_orders(symbol)
        else:
            orders = client.fetch_open_orders()
        return orders
    except Exception as e:
        st.error(f"Gagal mengambil order terbuka: {e}")
        return None

def get_recent_trades(symbol=None, limit=10):
    client = get_binance_client()
    if not client:
        return None
    try:
        if symbol:
            trades = client.fetch_my_trades(symbol, limit=limit)
        else:
            trades = client.fetch_my_trades(None, limit=limit)
        formatted = []
        for t in trades:
            formatted.append({
                'time': t['datetime'],
                'symbol': t['symbol'],
                'side': t['side'],
                'price': t['price'],
                'amount': t['amount'],
                'cost': t['cost'],
                'fee': t['fee']['cost'] if t.get('fee') else 0,
            })
        return formatted
    except Exception as e:
        st.error(f"Gagal mengambil riwayat trade: {e}")
        return None
