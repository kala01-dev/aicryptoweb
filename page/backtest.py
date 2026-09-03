import streamlit as st
import pandas as pd

st.set_page_config(page_title="Backtest", page_icon="📈", layout="wide")

st.title("📈 Backtesting")

if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

try:
    from core.data.fetcher import get_klines
    from core.backtest.engine import backtest_signal
    from config.settings import COINS, TIMEFRAME, LOOKBACK

    col1, col2 = st.columns([1,2])
    with col1:
        symbol = st.selectbox("Pilih Koin", [c['symbol'] for c in COINS])
        lookback_bt = st.slider("Jumlah candle untuk backtest", 200, 1000, 500, step=50)
    if st.button("Jalankan Backtest"):
        with st.spinner("Menjalankan backtest..."):
            df = get_klines(symbol, TIMEFRAME, lookback_bt)
            result = backtest_signal(symbol, df)
            st.metric("ROI", f"{result['roi']:.2f}%")
            st.metric("Win Rate", f"{result['win_rate']:.2f}%")
            st.metric("Total Trades", result['num_trades'])
except ImportError as e:
    st.warning(f"Modul core belum lengkap: {e}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
