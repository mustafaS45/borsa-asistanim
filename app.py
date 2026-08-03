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

# Direkt panoya kopyalama butonu
st.components.v1.html(f"""
    <textarea id="deepseekText" style="display:none;">{deepseek_metni}</textarea>
    <button onclick="
        var text = document.getElementById('deepseekText');
        text.style.display = 'block';
        text.select();
        text.setSelectionRange(0, 99999);
        navigator.clipboard.writeText(text.value).then(function() {{
            alert('✅ Panoya kopyalandı! Hemen DeepSeek sohbetine yapıştırabilirsiniz.');
        }});
        text.style.display = 'none';
    " style="
        width: 100%;
        padding: 12px 20px;
        background: #2a5298;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    ">
    📋 Tek Tıkla Panoya Kopyala
    </button>
""", height=60)

st.info("👆 Butona tıkla, DeepSeek sohbetine yapıştır (Ctrl+V)")

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

# ------------------------------------------------------------
# BIST 100 DETAYLI TARAMA
# ------------------------------------------------------------
st.divider()
st.subheader("🔍 BIST 100 Detaylı Tarama (F/K, PD/DD, Hacim)")

if st.button("BIST 100 Detaylı Verileri Çek", use_container_width=True):
    with st.spinner("Tüm BIST 100 hisseleri taranıyor... 2-3 dakika sürebilir."):
        
        bist100 = {
            "AEFES": "AEFES.IS", "AGHOL": "AGHOL.IS", "AKBNK": "AKBNK.IS",
            "AKFGY": "AKFGY.IS", "AKSA": "AKSA.IS", "ALARK": "ALARK.IS",
            "ALBRK": "ALBRK.IS", "ALFAS": "ALFAS.IS", "ARCLK": "ARCLK.IS",
            "ASELS": "ASELS.IS", "ASTOR": "ASTOR.IS", "ASUZU": "ASUZU.IS",
            "AYGAZ": "AYGAZ.IS", "BAGFS": "BAGFS.IS", "BERA": "BERA.IS",
            "BIMAS": "BIMAS.IS", "BRSAN": "BRSAN.IS", "BRYAT": "BRYAT.IS",
            "BUCIM": "BUCIM.IS", "CANTE": "CANTE.IS", "CCOLA": "CCOLA.IS",
            "CIMSA": "CIMSA.IS", "CWENE": "CWENE.IS", "DOHOL": "DOHOL.IS",
            "ECILC": "ECILC.IS", "ECZYT": "ECZYT.IS", "EGGUB": "EGGUB.IS",
            "EKGYO": "EKGYO.IS", "ENJSA": "ENJSA.IS", "ENKAI": "ENKAI.IS",
            "EREGL": "EREGL.IS", "EUPWR": "EUPWR.IS", "FENER": "FENER.IS",
            "FROTO": "FROTO.IS", "GARAN": "GARAN.IS", "GESAN": "GESAN.IS",
            "GOLTS": "GOLTS.IS", "GUBRF": "GUBRF.IS", "HALKB": "HALKB.IS",
            "HEKTS": "HEKTS.IS", "IPEKE": "IPEKE.IS", "ISCTR": "ISCTR.IS",
            "ISGYO": "ISGYO.IS", "ISMEN": "ISMEN.IS", "IZENR": "IZENR.IS",
            "KAYSE": "KAYSE.IS", "KCAER": "KCAER.IS", "KCHOL": "KCHOL.IS",
            "KLSER": "KLSER.IS", "KONTR": "KONTR.IS", "KONYA": "KONYA.IS",
            "KOZAA": "KOZAA.IS", "KOZAL": "KOZAL.IS", "KRDMD": "KRDMD.IS",
            "MAVI": "MAVI.IS", "MGROS": "MGROS.IS", "MIATK": "MIATK.IS",
            "ODAS": "ODAS.IS", "OTKAR": "OTKAR.IS", "OYAKC": "OYAKC.IS",
            "PETKM": "PETKM.IS", "PGSUS": "PGSUS.IS", "QUAGR": "QUAGR.IS",
            "SAHOL": "SAHOL.IS", "SASA": "SASA.IS", "SISE": "SISE.IS",
            "SKBNK": "SKBNK.IS", "SMRTG": "SMRTG.IS", "SOKM": "SOKM.IS",
            "TATEN": "TATEN.IS", "TAVHL": "TAVHL.IS", "TCELL": "TCELL.IS",
            "THYAO": "THYAO.IS", "TKFEN": "TKFEN.IS", "TOASO": "TOASO.IS",
            "TSKB": "TSKB.IS", "TTKOM": "TTKOM.IS", "TTRAK": "TTRAK.IS",
            "TUKAS": "TUKAS.IS", "TUPRS": "TUPRS.IS", "ULKER": "ULKER.IS",
            "VAKBN": "VAKBN.IS", "VESTL": "VESTL.IS", "YATAS": "YATAS.IS",
            "YGGYO": "YGGYO.IS", "YKBNK": "YKBNK.IS", "ZOREN": "ZOREN.IS"
        }
        
        sonuclar = []
        progress = st.progress(0)
        toplam = len(bist100)
        
        for i, (isim, sembol) in enumerate(bist100.items()):
            try:
                hisse = yf.Ticker(sembol)
                info = hisse.info
                fiyat = round(hisse.history(period="1d")['Close'].iloc[-1], 2)
                
                # Günlük değişim
                try:
                    prev = hisse.history(period="5d")['Close'].iloc[-2]
                    degisim = round(((fiyat - prev) / prev) * 100, 2)
                except:
                    degisim = 0
                
                sonuclar.append({
                    "Hisse": isim,
                    "Fiyat": fiyat,
                    "Değişim %": degisim,
                    "F/K": info.get("trailingPE", "-"),
                    "PD/DD": info.get("priceToBook", "-"),
                    "Hacim": info.get("volume", "-")
                })
            except:
                sonuclar.append({
                    "Hisse": isim, "Fiyat": 0, "Değişim %": 0,
                    "F/K": "-", "PD/DD": "-", "Hacim": "-"
                })
            progress.progress((i + 1) / toplam)
        
        progress.empty()
        df_bist = pd.DataFrame(sonuclar)
        st.success(f"✅ {len(df_bist)} hisse detaylı tarandı!")
        
        # Filtreleme
        st.subheader("🎯 Filtrele")
        col1, col2, col3 = st.columns(3)
        with col1:
            fk_max = st.number_input("Maks F/K", value=20, step=1)
        with col2:
            pddd_max = st.number_input("Maks PD/DD", value=5, step=1)
        with col3:
            sec = st.selectbox("Sektör", ["Hepsi", "Banka", "Sanayi", "Holding", "Teknoloji"])
        
        # Filtre uygula
        filtreli = df_bist.copy()
        filtreli = filtreli[filtreli["Fiyat"] > 0]
        
        if sec == "Banka":
            bankalar = ["AKBNK", "YKBNK", "GARAN", "ISCTR", "HALKB", "VAKBN", "TSKB", "SKBNK"]
            filtreli = filtreli[filtreli["Hisse"].isin(bankalar)]
        
        st.dataframe(filtreli, use_container_width=True, hide_index=True)
        
        # DeepSeek formatı
        st.subheader("📋 DeepSeek'e Gönder")
        bist_metni = "BIST 100 DETAYLI:\n"
        for _, row in filtreli.iterrows():
            bist_metni += f"{row['Hisse']}: {row['Fiyat']:.2f} TL | Günlük: %{row['Değişim %']} | F/K: {row['F/K']} | PD/DD: {row['PD/DD']}\n"
        
        st.download_button(
            label="📋 Detaylı Veriyi İndir",
            data=bist_metni,
            file_name="bist100_detayli.txt",
            mime="text/plain"
        )
st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance + Investing.com")
