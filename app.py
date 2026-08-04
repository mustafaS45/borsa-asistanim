import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="Borsa Asistanım", page_icon="📊", layout="wide")

# ============================================
# TRADINGVIEW TARZI TEMA
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #131722; }
    .main .block-container { padding: 1.5rem 2rem; max-width: 1500px; }
    
    .tv-panel {
        background: #1e222d; border: 1px solid #2a2e39;
        border-radius: 6px; padding: 12px 16px; margin-bottom: 12px;
    }
    .tv-panel.sat {
        border-left: 3px solid #f23645; background: #1a1015;
    }
    .tv-metric {
        background: #1e222d; border: 1px solid #2a2e39;
        border-radius: 6px; padding: 12px; text-align: center;
    }
    .tv-metric .label { color: #787b86; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
    .tv-metric .value { color: #d1d4dc; font-size: 20px; font-weight: 700; }
    
    .stButton > button {
        background: #2962ff !important; color: white !important;
        border: none !important; border-radius: 4px !important;
        padding: 8px 16px !important; font-weight: 500 !important;
    }
    .stButton > button:hover { background: #1e4bd8 !important; }
    
    .stDataFrame {
        background: #1e222d !important; border: 1px solid #2a2e39 !important; border-radius: 4px !important;
    }
    .stDataFrame th {
        background: #2a2e39 !important; color: #787b86 !important;
        font-size: 11px !important; text-transform: uppercase !important;
    }
    .stDataFrame td { color: #d1d4dc !important; font-size: 13px !important; }
    
    h1 { color: #d1d4dc !important; font-weight: 700 !important; }
    h2, h3 { color: #d1d4dc !important; font-weight: 600 !important; font-size: 14px !important; }
    hr { border-color: #2a2e39 !important; }
    .stProgress > div > div { background: #2962ff !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #131722; }
    ::-webkit-scrollbar-thumb { background: #2a2e39; border-radius: 3px; }
    
    .stTextInput > div > div > input {
        background: #1e222d !important; color: #d1d4dc !important;
        border: 1px solid #2a2e39 !important; border-radius: 4px !important;
    }
    .stNumberInput > div > div > input {
        background: #1e222d !important; color: #d1d4dc !important;
        border: 1px solid #2a2e39 !important; border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# BIST TÜM HİSSE VERİTABANI (600+ hisse)
# ============================================
BIST_SEMBOLLER = {
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
    "YGGYO": "YGGYO.IS", "YKBNK": "YKBNK.IS", "ZOREN": "ZOREN.IS",
}

# ============================================
# VERİ ÇEKME
# ============================================
@st.cache_data(ttl=300)
def fiyat_cek(sembol):
    try:
        hisse = yf.Ticker(sembol)
        fiyat = round(hisse.history(period="1d")['Close'].iloc[-1], 2)
        info = hisse.info
        return {
            "Fiyat": fiyat,
            "F/K": info.get("trailingPE", "-"),
            "PD/DD": info.get("priceToBook", "-")
        }
    except:
        return None

@st.cache_data(ttl=3600)
def piyasa_cek():
    v = {}
    try: v['bist'] = round(yf.Ticker("XU100.IS").history(period="1d")['Close'].iloc[-1], 0)
    except: v['bist'] = 0
    try: v['usd'] = round(yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1], 2)
    except: v['usd'] = 0
    return v

pv = piyasa_cek()

# ============================================
# ÜST BAR
# ============================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="tv-metric"><div class="label">BIST 100</div><div class="value">{pv["bist"]:,}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="tv-metric"><div class="label">USD/TRY</div><div class="value">{pv["usd"]:.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="tv-metric"><div class="label">GRAM ALTIN</div><div class="value">6,170</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="tv-metric"><div class="label">FAİZ</div><div class="value">%37</div></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================
# ÜÇ SÜTUN
# ============================================
sol, orta, sag = st.columns([1, 1.2, 1])

# --- SOL: HİSSE ARAMA ---
with sol:
    st.markdown('<h3>🔍 HİSSE BİLGİ</h3>', unsafe_allow_html=True)
    
    hisse_kodu = st.text_input("Hisse Kodu", placeholder="Örn: GARAN").upper()
    
    if hisse_kodu:
        if hisse_kodu in BIST_SEMBOLLER:
            veri = fiyat_cek(BIST_SEMBOLLER[hisse_kodu])
            if veri:
                st.markdown(f"""
                <div class="tv-panel">
                    <div style="font-size: 20px; font-weight: 700; color: #22ab94;">{hisse_kodu}</div>
                    <div style="font-size: 24px; font-weight: 700; color: #d1d4dc;">{veri['Fiyat']:.2f} <span style="font-size:14px;">TL</span></div>
                    <div style="display: flex; gap: 20px; margin-top: 8px;">
                        <div><span style="color:#787b86;">F/K:</span> {veri['F/K']}</div>
                        <div><span style="color:#787b86;">PD/DD:</span> {veri['PD/DD']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Veri çekilemedi")
        else:
            st.error(f"❌ {hisse_kodu} BIST'te bulunamadı!")

# --- ORTA: PORTFÖY ---
with orta:
    st.markdown('<h3>💼 PORTFÖYÜM</h3>', unsafe_allow_html=True)
    
    if "portfoy" not in st.session_state:
        st.session_state.portfoy = [{"Ad": "PPF", "Lot": 36500, "Alış": 1.00}]
    
    # Hisse ekle
    with st.expander("➕ Hisse Ekle"):
        with st.form("ekle_form"):
            h_ad = st.text_input("Hisse Kodu", placeholder="GARAN").upper()
            col1, col2 = st.columns(2)
            with col1: h_lot = st.number_input("Lot", value=1, step=1)
            with col2: h_alis = st.number_input("Alış Fiyatı", value=1.0, step=0.01)
            
            if st.form_submit_button("✅ Ekle", use_container_width=True):
                if h_ad in BIST_SEMBOLLER:
                    bulundu = False
                    for p in st.session_state.portfoy:
                        if p["Ad"] == h_ad:
                            p["Lot"] = h_lot
                            p["Alış"] = h_alis
                            bulundu = True
                            break
                    if not bulundu:
                        st.session_state.portfoy.append({"Ad": h_ad, "Lot": h_lot, "Alış": h_alis})
                    st.success(f"✅ {h_ad} eklendi!")
                    st.rerun()
                else:
                    st.error(f"❌ {h_ad} BIST'te bulunamadı!")
    
    # Portföy hesaplama
    toplam = 0
    toplam_maliyet = 0
    sat_sinyalleri = []
    
    for p in st.session_state.portfoy:
        if p["Ad"] == "PPF":
            p["Güncel"] = 1.00
            p["F/K"] = "-"
            p["PD/DD"] = "-"
        elif p["Ad"] in BIST_SEMBOLLER:
            veri = fiyat_cek(BIST_SEMBOLLER[p["Ad"]])
            if veri:
                p["Güncel"] = veri["Fiyat"]
                p["F/K"] = veri["F/K"]
                p["PD/DD"] = veri["PD/DD"]
            else:
                p["Güncel"] = p["Alış"]
                p["F/K"] = "-"
                p["PD/DD"] = "-"
        else:
            continue
        
        p["Maliyet"] = p["Lot"] * p["Alış"]
        p["Değer"] = p["Lot"] * p["Güncel"]
        p["K/Z"] = p["Değer"] - p["Maliyet"]
        p["K/Z %"] = (p["K/Z"] / p["Maliyet"]) * 100 if p["Maliyet"] > 0 else 0
        toplam += p["Değer"]
        toplam_maliyet += p["Maliyet"]
        
        # Sat sinyali kontrolü (%7 zarar veya %20 kâr)
        if p["Ad"] != "PPF" and p["K/Z %"] <= -7:
            sat_sinyalleri.append(f"🔴 {p['Ad']}: %{p['K/Z %']:.1f} zarar - STOP-LOSS!")
        elif p["Ad"] != "PPF" and p["K/Z %"] >= 20:
            sat_sinyalleri.append(f"🟢 {p['Ad']}: %{p['K/Z %']:.1f} kâr - KÂR AL!")
    
    # Toplam kartı
    kar_zarar = toplam - toplam_maliyet
    getiri = (kar_zarar / toplam_maliyet) * 100 if toplam_maliyet > 0 else 0
    renk = "#22ab94" if kar_zarar >= 0 else "#f23645"
    
    st.markdown(f"""
    <div class="tv-panel" style="text-align: center;">
        <div class="label">TOPLAM DEĞER</div>
        <div style="font-size: 28px; font-weight: 700; color: #d1d4dc;">{toplam:,.0f} <span style="font-size:14px;">TL</span></div>
        <div style="font-size: 14px; color: {renk};">{kar_zarar:+,.0f} TL (%{getiri:+.1f})</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Portföy listesi
    for p in st.session_state.portfoy:
        if p["Ad"] not in BIST_SEMBOLLER and p["Ad"] != "PPF":
            continue
        kz_renk = "#22ab94" if p.get('K/Z', 0) >= 0 else "#f23645"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #2a2e39;">
            <div>
                <div style="color: #d1d4dc; font-weight: 500;">{p['Ad']}</div>
                <div style="color: #787b86; font-size: 11px;">{p['Lot']} lot × {p['Alış']:.2f} TL</div>
            </div>
            <div style="text-align: right;">
                <div style="color: #d1d4dc;">{p.get('Değer', 0):,.0f} TL</div>
                <div style="color: {kz_renk}; font-size: 12px;">%{p.get('K/Z %', 0):+.1f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sıfırla
    if st.button("🔄 Portföyü Sıfırla", use_container_width=True):
        st.session_state.portfoy = [{"Ad": "PPF", "Lot": 36500, "Alış": 1.00}]
        st.rerun()

# --- SAĞ: GÜN SONU RAPORU ---
with sag:
    st.markdown('<h3>📊 GÜN SONU RAPORU</h3>', unsafe_allow_html=True)
    
    turkiye_saati = datetime.now(pytz.timezone('Europe/Istanbul'))
    st.markdown(f"""
    <div class="tv-panel" style="text-align: center;">
        <div style="color: #787b86; font-size: 12px;">TÜRKİYE SAATİ</div>
        <div style="font-size: 24px; font-weight: 700; color: #d1d4dc;">{turkiye_saati.strftime('%H:%M:%S')}</div>
        <div style="color: #787b86; font-size: 11px;">{turkiye_saati.strftime('%d.%m.%Y')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 18:30 kontrolü
    saat = turkiye_saati.hour
    dakika = turkiye_saati.minute
    
    if saat == 18 and dakika >= 30 or saat > 18:
        st.markdown("---")
        st.markdown('<h3 style="color: #ff9800;">🔔 GÜN SONU ÖZETİ</h3>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="tv-panel">
            <div style="color: #d1d4dc; font-size: 16px; font-weight: 600;">Portföy Değeri: {toplam:,.0f} TL</div>
            <div style="color: {renk}; margin-top: 4px;">Günlük K/Z: {kar_zarar:+,.0f} TL</div>
        </div>
        """, unsafe_allow_html=True)
        
        if sat_sinyalleri:
            st.markdown("---")
            st.markdown('<h3 style="color: #f23645;">⚠️ SAT SİNYALLERİ</h3>', unsafe_allow_html=True)
            for sinyal in sat_sinyalleri:
                st.markdown(f"""
                <div class="tv-panel sat" style="margin-bottom: 6px;">
                    <div style="color: #d1d4dc; font-weight: 500;">{sinyal}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Sat sinyali yok. Portföy sağlıklı.")
    else:
        st.info(f"⏳ Gün sonu raporu saat 18:30'da hazır olacak.\nKalan süre: {18 - saat} saat {60 - dakika if dakika <= 30 else 90 - dakika} dakika")
    
    # Dünkü özet (manuel)
    st.markdown("---")
    st.markdown('<h3 style="color: #787b86;">📋 DÜN</h3>', unsafe_allow_html=True)
    st.caption("Henüz dünkü veri yok.")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance")
