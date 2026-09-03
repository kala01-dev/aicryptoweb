# app.py
import streamlit as st

st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide")

# Cek login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu.")
    st.switch_page("login.py")
    st.stop()  # hentikan eksekusi halaman ini

# Jika sudah login, tampilkan navigasi halaman
st.sidebar.title("Navigasi")
st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False))

# Gunakan multi-page bawaan Streamlit
pages = [
    st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊"),
    st.Page("pages/2_Signals.py", title="Sinyal", icon="🚦"),
    st.Page("pages/3_Backtest.py", title="Backtest", icon="📈"),
    st.Page("pages/4_Portfolio.py", title="Portofolio", icon="💼"),
    st.Page("pages/5_Settings.py", title="Pengaturan", icon="⚙️"),
]
pg = st.navigation(pages)
pg.run()
