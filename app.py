import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Borsa Asistanım", page_icon="📊", layout="wide")

st.title("📊 Borsa Asistanım")
st.caption(f"Son güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

# ------------------------------------------------------------
# 1. PİYASA VERİLERİNİ ÇEK
# ------------------------------------------------------------
@st.cache_data(ttl=3600)
def veri_cek():
    v = {}
    try:
        v['bist'] = round(yf.Ticker("XU100.IS").history(period="1d")['Close'].iloc[-1], 0)
    except: v['bist'] = 13411
    try:
        v['usd'] = round(yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1], 2)
    except: v['usd'] = 47.53
    try:
        v['altin'] = 6170  # Manuel güncel değer
    except: v['altin'] = 6170
    try:
        v['aselsan'] = round(yf.Ticker("ASELS.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['aselsan'] = 336.25
    try:
        v['akbnk'] = round(yf.Ticker("AKBNK.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['akbnk'] = 66.00
    try:
        v['ykbnk'] = round(yf.Ticker("YKBNK.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['ykbnk'] = 34.00
    try:
        v['thy'] = round(yf.Ticker("THYAO.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['thy'] = 317.00
    return v

v = veri_cek()

# ------------------------------------------------------------
# 2. TEMEL GÖSTERGELER
# ------------------------------------------------------------
st.subheader("📈 Piyasa Özeti")
c1, c2, c3 = st.columns(3)
c1.metric("BIST 100", f"{v['bist']:,.0f}")
c2.metric("USD/TRY", f"{v['usd']:.2f} ₺")
c3.metric("Gram Altın", f"{v['altin']:,.0f} ₺")

st.divider()

# ------------------------------------------------------------
# 3. PORTFÖY
# ------------------------------------------------------------
st.subheader("💼 Portföyüm (40.000 TL)")

# Portföy tanımı
portfoy = [
    {"Ad": "PPF",              "Lot": 12000, "Alış": 1.00,   "Güncel": 1.00},
    {"Ad": "Altın Fonu",       "Lot": 6000,  "Alış": 6170,   "Güncel": v['altin']},
    {"Ad": "AKBNK",            "Lot": 121,   "Alış": 66.00,  "Güncel": v['akbnk']},
    {"Ad": "ASELSAN",          "Lot": 18,    "Alış": 336.25, "Güncel": v['aselsan']},
    {"Ad": "YKBNK",            "Lot": 118,   "Alış": 34.00,  "Güncel": v['ykbnk']},
    {"Ad": "THYAO",            "Lot": 13,    "Alış": 317.00, "Güncel": v['thy']},
]

# Hesaplamalar
toplam = 0
for p in portfoy:
    p["Maliyet"] = p["Lot"] * p["Alış"] if p["Ad"] not in ["PPF", "Altın Fonu"] else p["Lot"]
    p["Değer"] = p["Lot"] * p["Güncel"] if p["Ad"] not in ["PPF", "Altın Fonu"] else p["Lot"] * (p["Güncel"]/p["Alış"])
    p["K/Z"] = p["Değer"] - p["Maliyet"]
    p["K/Z %"] = (p["K/Z"] / p["Maliyet"]) * 100
    toplam += p["Değer"]

# Özet
c1, c2, c3 = st.columns(3)
c1.metric("Toplam Değer", f"{toplam:,.0f} TL")
c2.metric("Kâr/Zarar", f"{toplam-40000:,.0f} TL")
c3.metric("Getiri", f"%{((toplam-40000)/40000)*100:.1f}")

# Tablo
df = pd.DataFrame(portfoy)
df = df[["Ad", "Lot", "Alış", "Güncel", "Maliyet", "Değer", "K/Z", "K/Z %"]]
st.dataframe(df.round(2), use_container_width=True, hide_index=True)

# Pasta grafik
st.subheader("Dağılım")
fig = px.pie(df, values='Değer', names='Ad')
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# 4. HİSSE FİYATLARI
# ------------------------------------------------------------
st.divider()
st.subheader("📈 Hisse Fiyatları")
c1, c2, c3, c4 = st.columns(4)
c1.metric("ASELSAN", f"{v['aselsan']:.2f} TL")
c2.metric("AKBNK", f"{v['akbnk']:.2f} TL")
c3.metric("YKBNK", f"{v['ykbnk']:.2f} TL")
c4.metric("THYAO", f"{v['thy']:.2f} TL")

st.divider()
st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance")
