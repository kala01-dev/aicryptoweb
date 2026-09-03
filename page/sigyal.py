import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sinyal", page_icon="🚦", layout="wide")

st.title("🚦 Sinyal Trading")

if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

try:
    from core.data.fetcher import get_klines, get_24hr_tickers
    from core.signals.engine import generate_signal
    from config.settings import COINS, TIMEFRAME, LOOKBACK, MIN_VOLUME_24H

    tickers = get_24hr_tickers()
    liquid_symbols = set(tickers[tickers['quoteVolume'] >= MIN_VOLUME_24H]['symbol'])
    selected_coins = [c for c in COINS if c['symbol'] in liquid_symbols][:15]

    signals = []
    with st.spinner("Menghitung sinyal..."):
        for coin in selected_coins:
            df = get_klines(coin['symbol'], TIMEFRAME, LOOKBACK)
            if len(df) < 100:
                continue
            sig = generate_signal(coin['symbol'], coin['coingecko_id'], df)
            signals.append(sig)

    df_signals = pd.DataFrame([{
        'Symbol': s['symbol'],
        'Signal': s['signal'],
        'Score': f"{s['total_score']:.1f}",
        'ML Prob': f"{s['ml_prob']*100:.1f}%",
        'Price': f"${s['current_price']:,.2f}"
    } for s in signals])
    st.dataframe(df_signals, use_container_width=True)
except ImportError as e:
    st.warning(f"Modul core belum lengkap: {e}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
