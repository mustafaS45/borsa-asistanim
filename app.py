import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Borsa Asistanım", page_icon="📊", layout="wide")

st.title("📊 Borsa Asistanım")
st.caption(f"Son güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

# ------------------------------------------------------------
# INVESTING.COM'DAN VERİ ÇEKME
# ------------------------------------------------------------
@st.cache_data(ttl=3600)
def cek_altin():
    """Gram altın fiyatını investing.com'dan çeker"""
    try:
        url = "https://tr.investing.com/currencies/gau-try"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        # Fiyatı bul
        fiyat = soup.find("div", {"data-test": "instrument-price-last"})
        if fiyat:
            return float(fiyat.text.replace(".", "").replace(",", "."))
    except:
        pass
    return 6170  # yedek değer

@st.cache_data(ttl=3600)
def cek_faiz():
    """Politika faizini investing.com'dan çeker"""
    try:
        url = "https://tr.investing.com/central-banks/tcmb"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        # Faiz değerini ara
        text = soup.get_text()
        # "%37.00" gibi bir ifade ara
        match = re.search(r"(\d+[.,]\d+)%", text)
        if match:
            return float(match.group(1).replace(",", "."))
    except:
        pass
    return 37.0  # yedek değer

# ------------------------------------------------------------
# YAHOO FINANCE'TEN HİSSE VERİSİ ÇEKME
# ------------------------------------------------------------
@st.cache_data(ttl=3600)
def veri_cek():
    v = {}
    try: v['bist'] = round(yf.Ticker("XU100.IS").history(period="1d")['Close'].iloc[-1], 0)
    except: v['bist'] = 0
    try: v['usd'] = round(yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1], 2)
    except: v['usd'] = 0
    try: v['aselsan'] = round(yf.Ticker("ASELS.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['aselsan'] = 0
    try: v['akbnk'] = round(yf.Ticker("AKBNK.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['akbnk'] = 0
    try: v['ykbnk'] = round(yf.Ticker("YKBNK.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['ykbnk'] = 0
    try: v['thy'] = round(yf.Ticker("THYAO.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['thy'] = 0
    return v

# Tüm verileri topla
with st.spinner("Veriler çekiliyor..."):
    v = veri_cek()
    v['altin'] = cek_altin()
    v['faiz'] = cek_faiz()

# ------------------------------------------------------------
# DEEPSEEK'E GÖNDER
# ------------------------------------------------------------
st.markdown("---")
st.subheader("🤖 DeepSeek Analizi İçin")

deepseek_metni = f"""BIST: {v['bist']:,.0f}
USD: {v['usd']:.2f}
Altın: {v['altin']:,.0f}
Faiz: %{v['faiz']:.1f}
ASELSAN: {v['aselsan']:.2f}
AKBNK: {v['akbnk']:.2f}
THYAO: {v['thy']:.2f}
YKBNK: {v['ykbnk']:.2f}"""

st.code(deepseek_metni, language="")

col1, col2 = st.columns([1, 3])
with col1:
    st.download_button(
        label="📋 Dosyayı İndir",
        data=deepseek_metni,
        file_name="bist_veri.txt",
        mime="text/plain"
    )
with col2:
    st.info("👆 Butona tıkla, inen dosyayı aç, metni kopyalayıp DeepSeek'e yapıştır.")

st.markdown("---")

# ------------------------------------------------------------
# PİYASA ÖZETİ
# ------------------------------------------------------------
st.subheader("📈 Piyasa Özeti")
c1, c2, c3, c4 = st.columns(4)
c1.metric("BIST 100", f"{v['bist']:,.0f}")
c2.metric("USD/TRY", f"{v['usd']:.2f} ₺")
c3.metric("Gram Altın", f"{v['altin']:,.0f} ₺")
c4.metric("Faiz", f"%{v['faiz']:.1f}")

st.divider()

# ------------------------------------------------------------
# PORTFÖY
# ------------------------------------------------------------
st.subheader("💼 Portföyüm (40.000 TL)")

portfoy = [
    {"Ad": "PPF",              "Lot": 12000, "Alış": 1.00,   "Güncel": 1.00},
    {"Ad": "Altın Fonu",       "Lot": 6000,  "Alış": 6170,   "Güncel": v['altin']},
    {"Ad": "AKBNK",            "Lot": 121,   "Alış": 66.00,  "Güncel": v['akbnk']},
    {"Ad": "ASELSAN",          "Lot": 18,    "Alış": 336.25, "Güncel": v['aselsan']},
    {"Ad": "YKBNK",            "Lot": 118,   "Alış": 34.00,  "Güncel": v['ykbnk']},
    {"Ad": "THYAO",            "Lot": 13,    "Alış": 317.00, "Güncel": v['thy']},
]

toplam = 0
for p in portfoy:
    if p["Ad"] == "PPF":
        p["Maliyet"] = p["Lot"]
        p["Değer"] = p["Lot"]
    elif p["Ad"] == "Altın Fonu":
        p["Maliyet"] = p["Lot"]
        p["Değer"] = p["Lot"] * (p["Güncel"] / p["Alış"])
    else:
        p["Maliyet"] = p["Lot"] * p["Alış"]
        p["Değer"] = p["Lot"] * p["Güncel"]
    p["K/Z"] = p["Değer"] - p["Maliyet"]
    p["K/Z %"] = (p["K/Z"] / p["Maliyet"]) * 100
    toplam += p["Değer"]

c1, c2, c3 = st.columns(3)
c1.metric("Toplam", f"{toplam:,.0f} TL")
c2.metric("Kâr/Zarar", f"{toplam-40000:,.0f} TL")
c3.metric("Getiri", f"%{((toplam-40000)/40000)*100:.1f}")

df = pd.DataFrame(portfoy)
st.dataframe(df[["Ad", "Lot", "Alış", "Güncel", "Maliyet", "Değer", "K/Z", "K/Z %"]].round(2), 
             use_container_width=True, hide_index=True)

fig = px.pie(df, values='Değer', names='Ad')
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📈 Hisse Fiyatları")
c1, c2, c3, c4 = st.columns(4)
c1.metric("ASELSAN", f"{v['aselsan']:.2f} TL")
c2.metric("AKBNK", f"{v['akbnk']:.2f} TL")
c3.metric("YKBNK", f"{v['ykbnk']:.2f} TL")
c4.metric("THYAO", f"{v['thy']:.2f} TL")

st.divider()
st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance + Investing.com")
