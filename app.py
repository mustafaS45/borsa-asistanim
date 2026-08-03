import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Borsa Asistanım", page_icon="📊", layout="wide")

# ============================================
# MODERN TASARIM - CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    .modern-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .lider-panel {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
    }
    
    .lider-panel.panik {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .lider-panel.zarar {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333 !important;
    }
    
    .lider-panel.kar {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333 !important;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(5px);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-card h3 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 8px 0;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-card small {
        color: #a0a0b0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
    }
    
    h2, h3 {
        color: #e0e0f0 !important;
        font-weight: 600 !important;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LIDER MİNİ PANEL
# ============================================
try:
    lider = yf.Ticker("LIDER.IS")
    lider_fiyat = round(lider.history(period="1d")['Close'].iloc[-1], 2)
except:
    lider_fiyat = 87.70

maliyet = 98.90
lot = 342
guncel_deger = lider_fiyat * lot
toplam_yatirim = maliyet * lot
zarar = guncel_deger - toplam_yatirim
zarar_yuzde = (zarar / toplam_yatirim) * 100
panik = maliyet * 0.90
hedef = maliyet * 1.10

panel_class = "panik" if lider_fiyat <= panik else "zarar" if lider_fiyat < maliyet else "kar"
panel_emoji = "🔴" if lider_fiyat <= panik else "🟡" if lider_fiyat < maliyet else "🟢"

st.markdown(f"""
<div class="lider-panel {panel_class}">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div>
            <div style="font-size: 0.8rem; opacity: 0.8; letter-spacing: 1px;">{panel_emoji} LIDER TAKİP</div>
            <div style="font-size: 2rem; font-weight: 700;">{lider_fiyat:.2f} <span style="font-size: 1rem;">TL</span></div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.8rem; opacity: 0.8;">Maliyet: {maliyet:.2f} TL</div>
            <div style="font-size: 1.2rem; font-weight: 600;">Zarar: {zarar:,.0f} TL (%{zarar_yuzde:.1f})</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 0.7rem; opacity: 0.7;">PANİK</div>
            <div style="font-weight: 600;">{panik:.2f}</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 0.7rem; opacity: 0.7;">HEDEF</div>
            <div style="font-weight: 600;">{hedef:.2f}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

lider_veri = f"LIDER: {lider_fiyat:.2f} TL | Maliyet: {maliyet} | Zarar: {zarar:,.0f} TL (%{zarar_yuzde:.1f})"
st.components.v1.html(f"""
    <textarea id="liderMini" style="display:none;">{lider_veri}</textarea>
    <button onclick="
        var t = document.getElementById('liderMini');
        t.style.display='block'; t.select();
        navigator.clipboard.writeText(t.value);
        t.style.display='none';
    " style="padding:6px 12px; background:#2a5298; color:white; border:none; border-radius:5px; cursor:pointer; font-size:12px;">
    📋 LIDER Kopyala</button>
""", height=35)

st.title("📊 Borsa Asistanım")
st.caption(f"Son güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
st.markdown("---")

# ============================================
# VERİ ÇEKME FONKSİYONLARI
# ============================================
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
    try: v['garan'] = round(yf.Ticker("GARAN.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['garan'] = 0
    try: v['isctr'] = round(yf.Ticker("ISCTR.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['isctr'] = 0
    try: v['sise'] = round(yf.Ticker("SISE.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['sise'] = 0
    try: v['ttkom'] = round(yf.Ticker("TTKOM.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['ttkom'] = 0
    try: v['thy'] = round(yf.Ticker("THYAO.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['thy'] = 0
    try: v['ykbnk'] = round(yf.Ticker("YKBNK.IS").history(period="1d")['Close'].iloc[-1], 2)
    except: v['ykbnk'] = 0
    return v

v = veri_cek()
altin_manual = 6170
faiz_manual = 37.0

# ============================================
# ÜÇ SÜTUN
# ============================================
sol, orta, sag = st.columns([1, 1, 1])

# --- SOL: DeepSeek ---
with sol:
    st.subheader("🤖 DeepSeek")
    
    deepseek_metni = f"""BIST: {v['bist']:,.0f} | USD: {v['usd']:.2f} | Altın: {altin_manual:,.0f} | Faiz: %{faiz_manual:.1f}
ASELSAN: {v['aselsan']:.2f} | AKBNK: {v['akbnk']:.2f} | GARAN: {v['garan']:.2f} | ISCTR: {v['isctr']:.2f}
THYAO: {v['thy']:.2f} | YKBNK: {v['ykbnk']:.2f} | SISE: {v['sise']:.2f} | TTKOM: {v['ttkom']:.2f}"""
    
    st.code(deepseek_metni, language="")
    
    st.components.v1.html(f"""
        <textarea id="deepseekText3" style="display:none;">{deepseek_metni}</textarea>
        <button onclick="
            var t = document.getElementById('deepseekText3');
            t.style.display='block'; t.select();
            navigator.clipboard.writeText(t.value);
            t.style.display='none';
        " style="width:100%; padding:10px; background:#2a5298; color:white; border:none; border-radius:8px; font-size:14px; font-weight:bold; cursor:pointer;">
        📋 Panoya Kopyala</button>
    """, height=50)
    
    st.caption("👆 DeepSeek sohbetine yapıştır")
    st.markdown("---")
    st.subheader("📈 Piyasa")
    c1, c2 = st.columns(2)
    c1.metric("BIST", f"{v['bist']:,.0f}")
    c2.metric("USD", f"{v['usd']:.2f}")
    c1.metric("Altın", f"{altin_manual:,.0f}")
    c2.metric("Faiz", f"%{faiz_manual:.1f}")

# --- ORTA: BIST 100 ---
with orta:
    st.subheader("🔍 BIST 100 Tarama")
    
    if st.button("BIST 100 Çek", use_container_width=True):
        with st.spinner("Taranıyor..."):
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
                    sonuclar.append({
                        "Hisse": isim, "Fiyat": fiyat,
                        "F/K": info.get("trailingPE", "-"),
                        "PD/DD": info.get("priceToBook", "-")
                    })
                except:
                    pass
                progress.progress((i + 1) / toplam)
            
            progress.empty()
            st.success(f"✅ {len(sonuclar)} hisse")
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True, hide_index=True)

            # DeepSeek için BIST 100
            st.markdown("---")
            bist_deepseek = "BIST 100 TARAMA:\n"
            for _, row in pd.DataFrame(sonuclar).iterrows():
                bist_deepseek += f"{row['Hisse']}: {row['Fiyat']:.2f} TL | F/K: {row['F/K']} | PD/DD: {row['PD/DD']}\n"
            
            st.components.v1.html(f"""
                <textarea id="bist100Text" style="display:none;">{bist_deepseek}</textarea>
                <button onclick="
                    var t = document.getElementById('bist100Text');
                    t.style.display='block'; t.select();
                    navigator.clipboard.writeText(t.value);
                    t.style.display='none';
                " style="width:100%; padding:8px; background:#dc3545; color:white; border:none; border-radius:5px; font-size:13px; font-weight:bold; cursor:pointer;">
                📋 BIST 100 Kopyala</button>
            """, height=45)

# --- SAĞ: Portföy ---
with sag:
    st.subheader("💼 Portföyüm")
    
    portfoy = [
        {"Ad": "PPF", "Lot": 12000, "Alış": 1.00, "Güncel": 1.00},
        {"Ad": "Altın Fonu", "Lot": 6000, "Alış": 6170, "Güncel": altin_manual},
        {"Ad": "AKBNK", "Lot": 121, "Alış": 66.00, "Güncel": v['akbnk']},
        {"Ad": "ASELSAN", "Lot": 18, "Alış": 336.25, "Güncel": v['aselsan']},
        {"Ad": "YKBNK", "Lot": 118, "Alış": 34.00, "Güncel": v['ykbnk']},
        {"Ad": "THYAO", "Lot": 13, "Alış": 317.00, "Güncel": v['thy']},
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
    
    c1, c2 = st.columns(2)
    c1.metric("Değer", f"{toplam:,.0f} TL")
    c2.metric("Getiri", f"%{((toplam-40000)/40000)*100:.1f}")
    
    st.dataframe(pd.DataFrame(portfoy)[["Ad", "Lot", "Alış", "Değer", "K/Z %"]], use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📈 Hisseler")
    c1, c2 = st.columns(2)
    c1.metric("GARAN", f"{v['garan']:.2f}")
    c2.metric("ISCTR", f"{v['isctr']:.2f}")
    c1.metric("SISE", f"{v['sise']:.2f}")
    c2.metric("TTKOM", f"{v['ttkom']:.2f}")

st.markdown("---")
st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance")
