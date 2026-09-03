import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portofolio", page_icon="💼", layout="wide")

st.title("💼 Portofolio")

if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

try:
    from core.data.database import get_account_balance, get_open_orders, get_recent_trades

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Muat Saldo"):
            balances = get_account_balance()
            if balances:
                df = pd.DataFrame(balances)
                st.dataframe(df)
            else:
                st.info("Tidak ada saldo atau API key tidak diatur.")
    with col2:
        if st.button("Muat Order Terbuka"):
            orders = get_open_orders()
            if orders:
                df = pd.DataFrame(orders)
                st.dataframe(df[['symbol','side','amount','price','status']])
            else:
                st.info("Tidak ada order terbuka.")
    with col3:
        if st.button("Muat Riwayat Trade"):
            trades = get_recent_trades(limit=10)
            if trades:
                df = pd.DataFrame(trades)
                st.dataframe(df)
            else:
                st.info("Tidak ada riwayat trade.")
except ImportError as e:
    st.warning(f"Modul core belum lengkap: {e}")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
