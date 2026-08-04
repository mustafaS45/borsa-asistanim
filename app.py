import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
import requests

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
# BIST TÜM HİSSELERİ
# ============================================
@st.cache_data(ttl=86400)
def tum_hisseleri_cek():
    hisseler = {}
    try:
        url = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/StockList?sorgu="
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json={}, headers=headers, timeout=15)
        data = response.json()
        for item in data.get('value', []):
            kod = item.get('code', '').strip().upper()
            if kod and len(kod) <= 5 and kod.isalpha():
                hisseler[kod] = f"{kod}.IS"
        if len(hisseler) > 100:
            return hisseler
    except:
        pass
    
    return {
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

BIST_SEMBOLLER = tum_hisseleri_cek()

# ============================================
# HİSSE ADLARI
# ============================================
HISSE_ADLARI = {
    "AEFES": "Anadolu Efes", "AGHOL": "Agrotech", "AKBNK": "Akbank",
    "ASELS": "Aselsan", "BIMAS": "Bim", "CCOLA": "Coca Cola İçecek",
    "DOHOL": "Doğan Holding", "EKGYO": "Emlak Konut", "ENKAI": "Enka İnşaat",
    "EREGL": "Ereğli Demir Çelik", "FROTO": "Ford Otosan", "GARAN": "Garanti Bankası",
    "HALKB": "Halkbank", "ISCTR": "İş Bankası", "KCHOL": "Koç Holding",
    "KRDMD": "Kardemir", "MAVI": "Mavi Giyim", "MGROS": "Migros",
    "ODAS": "Odaş", "OTKAR": "Otokar", "PETKM": "Petkim",
    "PGSUS": "Pegasus", "SAHOL": "Sabancı Holding", "SASA": "Sasa",
    "SISE": "Şişe Cam", "TCELL": "Turkcell", "THYAO": "THY",
    "TOASO": "Tofaş", "TSKB": "TSKB", "TTKOM": "Türk Telekom",
    "TTRAK": "Türk Traktör", "TUPRS": "Tüpraş", "ULKER": "Ülker",
    "VAKBN": "Vakıfbank", "VESTL": "Vestel", "YKBNK": "Yapı Kredi",
    "ZOREN": "Zorlu Enerji", "LIDER": "Lider Turizm",
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
        return {"Fiyat": fiyat, "F/K": info.get("trailingPE", "-"), "PD/DD": info.get("priceToBook", "-")}
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
col1.markdown(f'<div class="tv-metric"><div class="label">BIST 100</div><div class="value">{pv["bist"]:,}</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="tv-metric"><div class="label">USD/TRY</div><div class="value">{pv["usd"]:.2f}</div></div>', unsafe_allow_html=True)
col3.markdown('<div class="tv-metric"><div class="label">GRAM ALTIN</div><div class="value">6,170</div></div>', unsafe_allow_html=True)
col4.markdown('<div class="tv-metric"><div class="label">FAİZ</div><div class="value">%37</div></div>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ============================================
# ÜÇ SÜTUN
# ============================================
sol, orta, sag = st.columns([1, 1.2, 1])

# --- SOL ---
with sol:
    st.markdown('<h3>🤖 DEEPSEEK</h3>', unsafe_allow_html=True)
    deepseek_metni = f"""BIST: {pv['bist']:,} | USD: {pv['usd']:.2f} | Altın: 6170 | Faiz: %37"""
    st.code(deepseek_metni, language="")
    st.components.v1.html(f"""
        <textarea id="ds" style="display:none;">{deepseek_metni}</textarea>
        <button onclick="var t=document.getElementById('ds');t.style.display='block';t.select();navigator.clipboard.writeText(t.value);t.style.display='none';"
        style="width:100%;padding:8px;background:#2962ff;color:white;border:none;border-radius:4px;font-size:12px;font-weight:500;cursor:pointer;">📋 PANOYA KOPYALA</button>
    """, height=40)
    st.caption("👆 DeepSeek sohbetine yapıştır")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<h3>🔍 HİSSE BİLGİ</h3>', unsafe_allow_html=True)
    hisse_kodu = st.text_input("Hisse Kodu", placeholder="Örn: GARAN").upper()
    if hisse_kodu:
        if hisse_kodu in BIST_SEMBOLLER:
            veri = fiyat_cek(BIST_SEMBOLLER[hisse_kodu])
            if veri:
                st.markdown(f"""<div class="tv-panel">
                    <div style="font-size:20px;font-weight:700;color:#22ab94;">{hisse_kodu}</div>
                    <div style="font-size:24px;font-weight:700;color:#d1d4dc;">{veri['Fiyat']:.2f} <span style="font-size:14px;">TL</span></div>
                    <div style="display:flex;gap:20px;margin-top:8px;">
                        <div><span style="color:#787b86;">F/K:</span> {veri['F/K']}</div>
                        <div><span style="color:#787b86;">PD/DD:</span> {veri['PD/DD']}</div>
                    </div></div>""", unsafe_allow_html=True)
            else:
                st.warning("Veri çekilemedi")
        else:
            st.error(f"❌ {hisse_kodu} BIST'te bulunamadı!")

# --- ORTA ---
with orta:
    st.markdown('<h3>🔍 BIST TÜM HİSSELER</h3>', unsafe_allow_html=True)
    
    if st.button("📡 TÜM HİSSELERİ TARA", use_container_width=True):
        with st.spinner("Taranıyor..."):
            sonuclar = []
            progress = st.progress(0)
            toplam = len(BIST_SEMBOLLER)
            for i, (isim, sembol) in enumerate(BIST_SEMBOLLER.items()):
                veri = fiyat_cek(sembol)
                if veri:
                    sonuclar.append({"Hisse": isim, "Fiyat": veri['Fiyat'], "F/K": veri['F/K'], "PD/DD": veri['PD/DD']})
                progress.progress((i + 1) / toplam)
            progress.empty()
            st.success(f"✅ {len(sonuclar)} hisse tarandı")
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True, hide_index=True)
            
            bist_deepseek = "BIST TÜM HİSSELER:\n"
            for _, row in pd.DataFrame(sonuclar).iterrows():
                bist_deepseek += f"{row['Hisse']}: {row['Fiyat']:.2f} TL | F/K: {row['F/K']} | PD/DD: {row['PD/DD']}\n"
            
            st.components.v1.html(f"""
                <textarea id="bist" style="display:none;">{bist_deepseek}</textarea>
                <button onclick="var t=document.getElementById('bist');t.style.display='block';t.select();navigator.clipboard.writeText(t.value);t.style.display='none';"
                style="width:100%;padding:8px;background:#1e222d;color:#787b86;border:1px solid #2a2e39;border-radius:4px;font-size:11px;cursor:pointer;">📋 TÜM VERİYİ KOPYALA</button>
            """, height=40)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h3>💼 PORTFÖYÜM</h3>', unsafe_allow_html=True)
    
    if "portfoy" not in st.session_state:
        st.session_state.portfoy = [{"Ad": "NAKİT", "Lot": 36500, "Alış": 1.00}]
    
    with st.expander("➕ Hisse Ekle"):
        with st.form("ekle_form"):
            h_ad = st.text_input("Hisse Kodu veya Adı", placeholder="Örn: GARAN veya Garanti").upper()
            if h_ad:
                oneriler = []
                for kod, isim in HISSE_ADLARI.items():
                    if h_ad in kod or h_ad in isim.upper():
                        oneriler.append(f"{kod} - {isim}")
                if oneriler:
                    st.caption("🔍 Bulunan:")
                    for o in oneriler[:8]:
                        st.caption(f"  • {o}")
            
            col1, col2 = st.columns(2)
            h_lot = col1.number_input("Lot", value=1, step=1)
            h_alis = col2.number_input("Alış Fiyatı", value=1.0, step=0.01)
            
            if st.form_submit_button("✅ Ekle", use_container_width=True):
                gercek_kod = h_ad if h_ad in BIST_SEMBOLLER else None
                if not gercek_kod:
                    for kod, isim in HISSE_ADLARI.items():
                        if h_ad in isim.upper():
                            gercek_kod = kod
                            break
                
                if gercek_kod:
                    maliyet = h_lot * h_alis
                    for p in st.session_state.portfoy:
                        if p["Ad"] == "NAKİT":
                            if p["Lot"] >= maliyet:
                                p["Lot"] -= maliyet
                            else:
                                st.error(f"❌ Yetersiz nakit! Nakit: {p['Lot']:,.0f} TL, Gereken: {maliyet:,.0f} TL")
                                st.stop()
                            break
                    
                    bulundu = False
                    for p in st.session_state.portfoy:
                        if p["Ad"] == gercek_kod:
                            p["Lot"] = h_lot
                            p["Alış"] = h_alis
                            bulundu = True
                            break
                    if not bulundu:
                        st.session_state.portfoy.append({"Ad": gercek_kod, "Lot": h_lot, "Alış": h_alis})
                    
                    st.session_state.portfoy = [p for p in st.session_state.portfoy if p["Ad"] != "NAKİT" or p["Lot"] > 0]
                    st.success(f"✅ {gercek_kod} eklendi! (-{maliyet:,.0f} TL)")
                    st.rerun()
                else:
                    st.error(f"❌ '{h_ad}' bulunamadı!")
    
    toplam = 0
    toplam_maliyet = 0
    sat_sinyalleri = []
    
    for p in st.session_state.portfoy:
        if p["Ad"] == "NAKİT":
            p["Güncel"] = 1.00
        elif p["Ad"] in BIST_SEMBOLLER:
            veri = fiyat_cek(BIST_SEMBOLLER[p["Ad"]])
            p["Güncel"] = veri["Fiyat"] if veri else p["Alış"]
        else:
            continue
        
        p["Maliyet"] = p["Lot"] * p["Alış"]
        p["Değer"] = p["Lot"] * p["Güncel"]
        p["K/Z"] = p["Değer"] - p["Maliyet"]
        p["K/Z %"] = (p["K/Z"] / p["Maliyet"]) * 100 if p["Maliyet"] > 0 else 0
        toplam += p["Değer"]
        toplam_maliyet += p["Maliyet"]
        
        if p["Ad"] != "NAKİT" and p["K/Z %"] <= -7:
            sat_sinyalleri.append(f"🔴 {p['Ad']}: %{p['K/Z %']:.1f} - STOP-LOSS!")
        elif p["Ad"] != "NAKİT" and p["K/Z %"] >= 20:
            sat_sinyalleri.append(f"🟢 {p['Ad']}: %{p['K/Z %']:.1f} - KÂR AL!")
    
    kar_zarar = toplam - toplam_maliyet
    getiri = (kar_zarar / toplam_maliyet) * 100 if toplam_maliyet > 0 else 0
    renk = "#22ab94" if kar_zarar >= 0 else "#f23645"
    
    st.markdown(f"""<div class="tv-panel" style="text-align:center;">
        <div class="label">TOPLAM DEĞER</div>
        <div style="font-size:28px;font-weight:700;color:#d1d4dc;">{toplam:,.0f} <span style="font-size:14px;">TL</span></div>
        <div style="font-size:14px;color:{renk};">{kar_zarar:+,.0f} TL (%{getiri:+.1f})</div>
    </div>""", unsafe_allow_html=True)
    
    for p in st.session_state.portfoy:
        if p["Ad"] not in BIST_SEMBOLLER and p["Ad"] != "NAKİT":
            continue
        kz_renk = "#22ab94" if p.get('K/Z', 0) >= 0 else "#f23645"
        st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2e39;">
            <div><div style="color:#d1d4dc;font-weight:500;">{p['Ad']}</div>
            <div style="color:#787b86;font-size:11px;">{p['Lot']} lot × {p['Alış']:.2f} TL</div></div>
            <div style="text-align:right;"><div style="color:#d1d4dc;">{p.get('Değer', 0):,.0f} TL</div>
            <div style="color:{kz_renk};font-size:12px;">%{p.get('K/Z %', 0):+.1f}</div></div>
        </div>""", unsafe_allow_html=True)
    
    if st.button("🔄 Portföyü Sıfırla", use_container_width=True):
        st.session_state.portfoy = [{"Ad": "NAKİT", "Lot": 36500, "Alış": 1.00}]
        st.rerun()

# --- SAĞ ---
with sag:
    st.markdown('<h3>📊 GÜN SONU RAPORU</h3>', unsafe_allow_html=True)
    
    tz = pytz.timezone('Europe/Istanbul')
    ts = datetime.now(tz)
    st.markdown(f"""<div class="tv-panel" style="text-align:center;">
        <div style="color:#787b86;font-size:12px;">TÜRKİYE SAATİ</div>
        <div style="font-size:24px;font-weight:700;color:#d1d4dc;">{ts.strftime('%H:%M:%S')}</div>
        <div style="color:#787b86;font-size:11px;">{ts.strftime('%d.%m.%Y')}</div>
    </div>""", unsafe_allow_html=True)
    
    if ts.hour >= 18 and ts.minute >= 30:
        st.markdown('<h3 style="color:#ff9800;">🔔 GÜN SONU ÖZETİ</h3>', unsafe_allow_html=True)
        st.markdown(f"""<div class="tv-panel">
            <div style="color:#d1d4dc;font-size:16px;font-weight:600;">Portföy: {toplam:,.0f} TL</div>
            <div style="color:{renk};">Günlük K/Z: {kar_zarar:+,.0f} TL</div>
        </div>""", unsafe_allow_html=True)
        
        if sat_sinyalleri:
            st.markdown('<h3 style="color:#f23645;">⚠️ SAT SİNYALLERİ</h3>', unsafe_allow_html=True)
            for s in sat_sinyalleri:
                st.markdown(f"""<div class="tv-panel sat"><div style="color:#d1d4dc;">{s}</div></div>""", unsafe_allow_html=True)
        else:
            st.success("✅ Sat sinyali yok.")
    else:
        st.info(f"⏳ Rapor saat 18:30'da hazır olacak.")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance")
