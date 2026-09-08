# login.py
import streamlit as st
import bcrypt
from config.settings import USERNAME, PASSWORD_HASH  # ambil dari secrets

st.set_page_config(page_title="Login - Crypto AI Signal", page_icon="🪐", layout="centered")

# ==================== CSS TATA SURYA ====================
st.markdown("""
<style>
    /* Background dengan gradient luar angkasa */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #0a0a2e, #000000);
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
    }
    /* Judul besar dengan efek glow */
    .solar-title {
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(90deg, #ffcc00, #ff6600, #ff00cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #ffcc00, 0 0 20px #ff6600; }
        to { text-shadow: 0 0 20px #ff00cc, 0 0 40px #3333ff; }
    }
    /* Barisan planet */
    .planet-row {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        font-size: 2.5rem;
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    /* Kotak login */
    .login-box {
        background: linear-gradient(145deg, #1a1a3e, #0d0d2b);
        border-radius: 20px;
        padding: 2rem;
        margin: 0 auto;
        max-width: 400px;
        box-shadow: 0 0 30px rgba(0,255,255,0.3);
        border: 1px solid #00ffff33;
    }
    /* Tombol login */
    .stButton > button {
        background: linear-gradient(90deg, #ff00cc, #3333ff);
        color: white;
        font-weight: bold;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        border: none;
        box-shadow: 0 0 10px #ff00cc88;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px #ff00cc;
    }
    /* Input field */
    .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.05);
        color: white;
        border: 1px solid #00ffff33;
        border-radius: 10px;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("<div class='solar-title'>🪐 CRYPTO AI SIGNAL</div>", unsafe_allow_html=True)
st.markdown("<div class='planet-row'>☀️ 🪐 🌍 🌕 🔴</div>", unsafe_allow_html=True)

# ==================== FORM LOGIN ====================
st.markdown("<div class='login-box'>", unsafe_allow_html=True)
st.subheader("🔐 Login Dashboard")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Masuk"):
    # Verifikasi dengan bcrypt hash dari secrets
    if username == USERNAME and bcrypt.checkpw(password.encode(), PASSWORD_HASH.encode()):
        st.session_state.logged_in = True
        st.success("Login berhasil! Mengalihkan...")
        st.switch_page("app.py")  # pindah ke halaman utama
        st.rerun()
    else:
        st.error("Username atau password salah")
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div style='text-align:center; color:#888; margin-top:2rem;'>© 2024 Crypto AI Signal</div>", unsafe_allow_html=True)
