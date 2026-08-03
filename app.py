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
# TRADINGVIEW TARZI KOYU TEMA
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Ana arka plan - TradingView koyu gri */
    .stApp {
        background: #131722;
    }
    
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 1500px;
    }
    
    /* Üst bar */
    .top-bar {
        background: #1e222d;
        border-bottom: 1px solid #2a2e39;
        padding: 10px 0;
        margin-bottom: 15px;
    }
    
    /* LIDER paneli - canlı renk */
    .tv-panel {
        background: #1e222d;
        border: 1px solid #2a2e39;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }
    
    .tv-panel.panik {
        border-left: 3px solid #f23645;
        background: #1a1015;
    }
    
    .tv-panel.zarar {
        border-left: 3px solid #ff9800;
        background: #1a1510;
    }
    
    .tv-panel.kar {
        border-left: 3px solid #22ab94;
        background: #101a17;
    }
    
    /* Metrik kartı */
    .tv-metric {
        background: #1e222d;
        border: 1px solid #2a2e39;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
    }
    
    .tv-metric .label {
        color: #787b86;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .tv-metric .value {
        color: #d1d4dc;
        font-size: 20px;
        font-weight: 700;
    }
    
    .tv-metric .value.red { color: #f23645; }
    .tv-metric .value.green { color: #22ab94; }
    .tv-metric .value.orange { color: #ff9800; }
    
    /* Butonlar */
    .stButton > button {
        background: #2962ff !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        letter-spacing: 0.3px !important;
        transition: background 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #1e4bd8 !important;
    }
    
    /* Tablo */
    .stDataFrame {
        background: #1e222d !important;
        border: 1px solid #2a2e39 !important;
        border-radius: 4px !important;
    }
    
    .stDataFrame th {
        background: #2a2e39 !important;
        color: #787b86 !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 8px 12px !important;
    }
    
    .stDataFrame td {
        color: #d1d4dc !important;
        font-size: 13px !important;
        padding: 6px 12px !important;
        border-bottom: 1px solid #2a2e39 !important;
    }
    
    /* Başlıklar */
    h1 {
        color: #d1d4dc !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    h2, h3 {
        color: #d1d4dc !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px !important;
    }
    
    /* Text */
    p, span, div {
        color: #d1d4dc;
    }
    
    .caption {
        color: #787b86 !important;
        font-size: 12px;
    }
    
    /* Code block */
    .stCodeBlock {
        background: #1e222d !important;
        border: 1px solid #2a2e39 !important;
        border-radius: 4px !important;
    }
    
    code {
        color: #22ab94 !important;
    }
    
    /* Divider */
    hr {
        border-color: #2a2e39 !important;
        margin: 15px 0 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: #2962ff !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #131722; }
    ::-webkit-scrollbar-thumb { background: #2a2e39; border-radius: 3px; }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #2962ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LIDER PANEL
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
panel_renk = "#f23645" if lider_fiyat <= panik else "#ff9800" if lider_fiyat < maliyet else "#22ab94"
panel_emoji = "🔴" if lider_fiyat <= panik else "🟠" if lider_fiyat < maliyet else "🟢"

st.markdown(f"""
<div class="tv-panel {panel_class}">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 14px; font-weight: 600; color: #d1d4dc;">{panel_emoji} LIDER</span>
            <span style="font-size: 22px; font-weight: 700; color: {panel_renk};">{lider_fiyat:.2f}</span>
            <span style="color: #787b86; font-size: 12px;">TRY</span>
        </div>
        <div style="display: flex; gap: 25px;">
            <div>
                <div style="color: #787b86; font-size: 10px;">MALİYET</div>
                <div style="color: #d1d4dc; font-weight: 500;">{maliyet:.2f}</div>
            </div>
            <div>
                <div style="color: #787b86; font-size: 10px;">ZARAR</div>
                <div style="color: #f23645; font-weight: 600;">{zarar:,.0f} TL (%{zarar_yuzde:.1f})</div>
            </div>
            <div>
                <div style="color: #787b86; font-size: 10px;">PANİK</div>
                <div style="color: #ff9800; font-weight: 500;">{panik:.2f}</div>
            </div>
            <div>
                <div style="color: #787b86; font-size: 10px;">HEDEF</div>
                <div style="color: #22ab94; font-weight: 500;">{hedef:.2f}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Kopyala butonu
lider_veri = f"LIDER: {lider_fiyat:.2f} TL | Maliyet: {maliyet} | Zarar: {zarar:,.0f} TL (%{zarar_yuzde:.1f})"
st.components.v1.html(f"""
    <div style="margin-bottom: 15px;">
        <textarea id="liderMini" style="display:none;">{lider_veri}</textarea>
        <button onclick="
            var t = document.getElementById('liderMini');
            t.style.display='block'; t.select();
            navigator.clipboard.writeText(t.value);
            t.style.display='none';
        " style="padding:6px 14px; background:#1e222d; color:#787b86; border:1px solid #2a2e39; border-radius:4px; cursor:pointer; font-size:11px;">
        📋 KOPYALA</button>
    </div>
""", height=30)

# ============================================
# VERİ ÇEKME
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
# ÜST BAR - PİYASA ÖZETİ
# ============================================
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""
    <div class="tv-metric">
        <div class="label">BIST 100</div>
        <div class="value">{v['bist']:,}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="tv-metric">
        <div class="label">USD/TRY</div>
        <div class="value">{v['usd']:.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="tv-metric">
        <div class="label">GRAM ALTIN</div>
        <div class="value">{altin_manual:,}</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="tv-metric">
        <div class="label">FAİZ</div>
        <div class="value">%{faiz_manual:.1f}</div>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
    <div class="tv-metric">
        <div class="label">SON GÜNCELLEME</div>
        <div class="value" style="font-size:12px;">{datetime.now().strftime('%H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================
# ÜÇ SÜTUN
# ============================================
sol, orta, sag = st.columns([1, 1.2, 1])

# --- SOL: DeepSeek ---
with sol:
    st.markdown('<h3>🤖 DEEPSEEK ANALİZ</h3>', unsafe_allow_html=True)
    
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
        " style="width:100%; padding:8px; background:#2962ff; color:white; border:none; border-radius:4px; font-size:12px; font-weight:500; cursor:pointer;">
        📋 PANOYA KOPYALA</button>
    """, height=40)
    
    st.caption("👆 DeepSeek sohbetine yapıştır")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h3>📈 TAKİP LİSTESİ</h3>', unsafe_allow_html=True)
    
    takip = [
        ("GARAN", v['garan'], "4.46", "1.10"),
        ("ISCTR", v['isctr'], "4.16", "0.75"),
        ("AKBNK", v['akbnk'], "5.48", "1.13"),
        ("SISE", v['sise'], "11.15", "0.31"),
        ("TTKOM", v['ttkom'], "6.91", "0.76"),
    ]
    
    for hisse, fiyat, fk, pddd in takip:
        renk = "#22ab94" if fiyat > 0 else "#f23645"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2a2e39;">
            <span style="color: #d1d4dc; font-weight: 500;">{hisse}</span>
            <span style="color: {renk};">{fiyat:.2f}</span>
            <span style="color: #787b86; font-size: 11px;">F/K:{fk}</span>
            <span style="color: #787b86; font-size: 11px;">PD/DD:{pddd}</span>
        </div>
        """, unsafe_allow_html=True)

# --- ORTA: BIST 100 ---
with orta:
    st.markdown('<h3>🔍 BIST 100 TARAMA</h3>', unsafe_allow_html=True)
    
    if st.button("📡 BIST 100 VERİLERİNİ ÇEK", use_container_width=True):
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
            st.success(f"✅ {len(sonuclar)} hisse tarandı")
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True, hide_index=True)

            st.markdown("<hr>", unsafe_allow_html=True)
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
                " style="width:100%; padding:8px; background:#1e222d; color:#787b86; border:1px solid #2a2e39; border-radius:4px; font-size:11px; cursor:pointer;">
                📋 BIST 100 VERİSİNİ KOPYALA</button>
            """, height=40)

# --- SAĞ: Portföy ---
with sag:
    st.markdown('<h3>💼 PORTFÖYÜM</h3>', unsafe_allow_html=True)
    
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
    
    kar_zarar_toplam = toplam - 40000
    getiri = ((toplam - 40000) / 40000) * 100
    renk = "#22ab94" if kar_zarar_toplam >= 0 else "#f23645"
    
    st.markdown(f"""
    <div class="tv-panel" style="text-align: center;">
        <div class="label">TOPLAM DEĞER</div>
        <div style="font-size: 28px; font-weight: 700; color: #d1d4dc;">{toplam:,.0f} <span style="font-size:14px;">TL</span></div>
        <div style="font-size: 14px; color: {renk}; margin-top: 4px;">{kar_zarar_toplam:+,.0f} TL (%{getiri:+.1f})</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    for p in portfoy:
        kz_renk = "#22ab94" if p['K/Z'] >= 0 else "#f23645"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #2a2e39;">
            <div>
                <div style="color: #d1d4dc; font-weight: 500;">{p['Ad']}</div>
                <div style="color: #787b86; font-size: 11px;">{p['Lot']} lot</div>
            </div>
            <div style="text-align: right;">
                <div style="color: #d1d4dc;">{p['Değer']:,.0f} TL</div>
                <div style="color: {kz_renk}; font-size: 12px;">%{p['K/Z %']:+.1f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance")
