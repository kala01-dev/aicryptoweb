import streamlit as st

st.set_page_config(page_title="Pengaturan", page_icon="⚙️", layout="wide")

st.title("⚙️ Pengaturan")

if not st.session_state.get("logged_in", False):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.markdown("Pengaturan global aplikasi disimpan di `config/settings.py` dan `secrets.toml`.")

try:
    from config import settings
    st.write("**Daftar Koin yang Dimonitor:**")
    st.json([c['symbol'] for c in settings.COINS])
    st.write(f"**Timeframe:** {settings.TIMEFRAME}")
    st.write(f"**Lookback:** {settings.LOOKBACK}")
except ImportError as e:
    st.warning(f"Modul config belum lengkap: {e}")
