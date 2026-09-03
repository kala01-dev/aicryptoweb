import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard")

# Cek login
if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.markdown("Ringkasan pasar dan sinyal terbaru.")

try:
    from core.data.fetcher import get_24hr_tickers
    from core.signals.engine import generate_signal
    from config.settings import COINS, TIMEFRAME, LOOKBACK

    # Ambil top 3 koin berdasarkan volume
    tickers_df = get_24hr_tickers()
    top3 = tickers_df.head(3)
    cols = st.columns(3)
    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.metric(label=row['symbol'], value=f"${row['lastPrice']:,.2f}", delta=f"{row['priceChangePercent']:.2f}%")
except ImportError as e:
    st.warning(f"Modul core belum lengkap: {e}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
