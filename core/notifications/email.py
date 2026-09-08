import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import streamlit as st

def _get_env_or_secret(key):
    val = os.getenv(key)
    if val:
        return val
    try:
        return st.secrets[key]
    except:
        return None

def send_email_notification(subject, body):
    sender = _get_env_or_secret('GMAIL_USER')
    password = _get_env_or_secret('GMAIL_APP_PASSWORD')
    to_email = _get_env_or_secret('NOTIFY_EMAIL')
    if not sender or not password or not to_email:
        return False
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def notify_strong_signal(signal_data):
    symbol = signal_data['symbol']
    signal = signal_data['signal']
    price = signal_data['current_price']
    score = signal_data['total_score']
    subject = f"[Crypto Signal] {symbol} - {signal} (Skor: {score:.1f})"
    body = f"Koin: {symbol}\nSinyal: {signal}\nHarga: ${price:,.2f}\nSkor: {score:.1f}\nWaktu: {datetime.utcnow()}"
    return send_email_notification(subject, body)
