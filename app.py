import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz
import pandas as pd

st.set_page_config(page_title="Portföy Asistanım", page_icon="📊", layout="wide")

# ============================================
# TEMA
# ============================================
st.markdown("""
<style>
    .stApp { background: #131722; }
    .main .block-container { padding: 1.5rem 2rem; max-width: 1200px; }
    
    .tv-panel {
        background: #1e222d; border: 1px solid #2a2e39;
        border-radius: 6px; padding: 16px; margin-bottom: 12px;
    }
    
    .stButton > button {
        background: #2962ff !important; color: white !important;
        border: none !important; border-radius: 4px !important;
        padding: 8px 16px !important; font-weight: 500 !important;
    }
    
    h1, h2, h3 { color: #d1d4dc !important; }
    hr { border-color: #2a2e39 !important; }
    
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: #1e222d !important; color: #d1d4dc !important;
        border: 1px solid #2a2e39 !important; border-radius: 4px !important;
    }
    
    .sinyal-kar { border-left: 3px solid #22ab94 !important; }
    .sinyal-zarar { border-left: 3px solid #f23645 !important; }
    .sinyal-normal { border-left: 3px solid #2a2e39 !important; }
    .rapor-baslik { color: #ff9800 !important; }
    
    .ust-metric {
        background: #1e222d; border: 1px solid #2a2e39;
        border-radius: 6px; padding: 10px; text-align: center;
    }
    .ust-metric .label { color: #787b86; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
    .ust-metric .value { color: #d1d4dc; font-size: 18px; font-weight: 700; }
    
    .stDataFrame {
        background: #1e222d !important; border: 1px solid #2a2e39 !important; border-radius: 4px !important;
    }
    .stDataFrame th {
        background: #2a2e39 !important; color: #787b86 !important;
        font-size: 11px !important; text-transform: uppercase !important;
    }
    .stDataFrame td { color: #d1d4dc !important; font-size: 13px !important; }
    
    .stProgress > div > div { background: #2962ff !important; }
    
    .sekmeler > button {
        background: #1e222d !important; color: #787b86 !important;
        border: 1px solid #2a2e39 !important;
    }
    .sekmeler > button[aria-selected="true"] {
        background: #2962ff !important; color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# VERİ ÇEKME
# ============================================
@st.cache_data(ttl=300)
def fiyat_cek(sembol):
    try:
        hisse = yf.Ticker(sembol)
        f = round(hisse.history(period="1d")['Close'].iloc[-1], 2)
        info = hisse.info
        
        try:
            prev = hisse.history(period="5d")['Close'].iloc[-2]
            degisim = round(((f - prev) / prev) * 100, 2)
        except:
            degisim = 0
        
        return {
            "Fiyat": f,
            "F/K": info.get("trailingPE", "-"),
            "PD/DD": info.get("priceToBook", "-"),
            "Değişim": degisim,
            "Beta": info.get("beta", "-"),
            "52H Dip": info.get("fiftyTwoWeekLow", "-"),
            "52H Zirve": info.get("fiftyTwoWeekHigh", "-"),
            "Hacim": info.get("volume", "-"),
        }
    except:
        return None

@st.cache_data(ttl=3600)
def bist_cek():
    try: return round(yf.Ticker("XU100.IS").history(period="1d")['Close'].iloc[-1], 0)
    except: return 0

@st.cache_data(ttl=3600)
def usd_cek():
    try: return round(yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1], 2)
    except: return 0

@st.cache_data(ttl=600)
def altin_cek():
    try:
        ons = yf.Ticker("GC=F")
        ons_fiyat = round(ons.history(period="1d")['Close'].iloc[-1], 2)
        try:
            prev_ons = ons.history(period="5d")['Close'].iloc[-2]
            ons_degisim = round(((ons_fiyat - prev_ons) / prev_ons) * 100, 2)
        except:
            ons_degisim = 0
        usd = usd_cek()
        gram = round((ons_fiyat * usd) / 31.1, 2)
        return {"Gram": gram, "Ons": ons_fiyat, "Ons Değişim": ons_degisim}
    except:
        return {"Gram": 0, "Ons": 0, "Ons Değişim": 0}

@st.cache_data(ttl=600)
def petrol_cek():
    try:
        brent = yf.Ticker("BZ=F")
        fiyat = round(brent.history(period="1d")['Close'].iloc[-1], 2)
        try:
            prev = brent.history(period="5d")['Close'].iloc[-2]
            degisim = round(((fiyat - prev) / prev) * 100, 2)
        except:
            degisim = 0
        return {"Fiyat": fiyat, "Değişim": degisim}
    except:
        return {"Fiyat": 0, "Değişim": 0}

@st.cache_data(ttl=600)
def vix_cek():
    try:
        vix = yf.Ticker("^VIX")
        fiyat = round(vix.history(period="1d")['Close'].iloc[-1], 2)
        try:
            prev = vix.history(period="5d")['Close'].iloc[-2]
            degisim = round(((fiyat - prev) / prev) * 100, 2)
        except:
            degisim = 0
        return {"Fiyat": fiyat, "Değişim": degisim}
    except:
        return {"Fiyat": 0, "Değişim": 0}

@st.cache_data(ttl=600)
def bist100_tara():
    """BIST 100 hisselerini tarar, en ucuzları bulur"""
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
        "YGGYO": "YGGYO.IS", "YKBNK": "YKBNK.IS", "ZOREN": "ZOREN.IS",
    }
    
    sonuclar = []
    for isim, sembol in bist100.items():
        veri = fiyat_cek(sembol)
        if veri and veri["Fiyat"] > 0:
            sonuclar.append({
                "Hisse": isim,
                "Fiyat": veri["Fiyat"],
                "F/K": veri["F/K"],
                "PD/DD": veri["PD/DD"],
                "Değişim": veri["Değişim"],
            })
    
    df = pd.DataFrame(sonuclar)
    return df

bist = bist_cek()
usd = usd_cek()
altin = altin_cek()
petrol = petrol_cek()
vix = vix_cek()

if vix["Fiyat"] < 15:
    vix_seviye = "🟢 Sakin"
    vix_renk = "#22ab94"
elif vix["Fiyat"] < 25:
    vix_seviye = "⚪ Normal"
    vix_renk = "#d1d4dc"
elif vix["Fiyat"] < 35:
    vix_seviye = "🟡 Tedirgin"
    vix_renk = "#ff9800"
else:
    vix_seviye = "🔴 Korku"
    vix_renk = "#f23645"

# ============================================
# ÜST BAR
# ============================================
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    st.markdown(f'<div class="ust-metric"><div class="label">BIST 100</div><div class="value">{bist:,}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="ust-metric"><div class="label">USD/TRY</div><div class="value">{usd:.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="ust-metric"><div class="label">GRAM ALTIN</div><div class="value">{altin["Gram"]:,.0f}</div><div style="color:#787b86;font-size:10px;">Ons: ${altin["Ons"]:,.0f}</div></div>', unsafe_allow_html=True)
with col4:
    altin_renk = "#22ab94" if altin["Ons Değişim"] >= 0 else "#f23645"
    st.markdown(f'<div class="ust-metric"><div class="label">ALTIN G.</div><div class="value" style="color:{altin_renk};">%{altin["Ons Değişim"]:+.1f}</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="ust-metric"><div class="label">BRENT</div><div class="value">${petrol["Fiyat"]:,.1f}</div></div>', unsafe_allow_html=True)
with col6:
    petrol_renk = "#22ab94" if petrol["Değişim"] >= 0 else "#f23645"
    st.markdown(f'<div class="ust-metric"><div class="label">PETROL G.</div><div class="value" style="color:{petrol_renk};">%{petrol["Değişim"]:+.1f}</div></div>', unsafe_allow_html=True)
with col7:
    st.markdown(f'<div class="ust-metric"><div class="label">VIX KORKU</div><div class="value" style="color:{vix_renk};">{vix["Fiyat"]:.1f}</div><div style="color:{vix_renk};font-size:10px;">{vix_seviye}</div></div>', unsafe_allow_html=True)

# ============================================
# SEKMELER
# ============================================
st.title("📊 Portföy Asistanım")
st.caption(f"{datetime.now(pytz.timezone('Europe/Istanbul')).strftime('%H:%M')} | Altın: {altin['Gram']:,.0f} TL/g | Petrol: ${petrol['Fiyat']:,.1f} | VIX: {vix['Fiyat']:.1f}")

tab1, tab2, tab3 = st.tabs(["💼 Portföyüm", "🔍 BIST 100 Analiz", "🤖 DeepSeek"])

# ============================================
# SEKMELER
# ============================================

# --- SEKMELER ---
tab1, tab2, tab3 = st.tabs(["💼 Portföyüm", "🔍 BIST 100 Analiz", "🤖 DeepSeek"])

# ============================================
# TAB 1: PORTFÖY
# ============================================
with tab1:
    st.markdown("---")
    
    if "portfoy" not in st.session_state:
        st.session_state.portfoy = [
            {"Ad": "GARAN", "Lot": 72, "Alış": 127.90},
            {"Ad": "SISE", "Lot": 130, "Alış": 41.86},
            {"Ad": "AKBNK", "Lot": 110, "Alış": 66.45},
            {"Ad": "ISCTR", "Lot": 907, "Alış": 12.39},
            {"Ad": "NAKİT", "Lot": 5, "Alış": 1.00},
        ]
    
    with st.expander("✏️ Hisse Ekle / Düzenle", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            hisse_kod = st.text_input("Hisse", placeholder="GARAN").upper()
        with col2:
            hisse_lot = st.number_input("Lot", value=1, step=1)
        with col3:
            hisse_alis = st.number_input("Alış Fiyatı", value=1.0, step=0.01)
        with col4:
            st.write("")
            st.write("")
            ekle_btn = st.button("✅ Ekle", use_container_width=True)
        
        if ekle_btn and hisse_kod:
            bulundu = False
            for p in st.session_state.portfoy:
                if p["Ad"] == hisse_kod:
                    p["Lot"] = hisse_lot
                    p["Alış"] = hisse_alis
                    bulundu = True
                    break
            if not bulundu:
                st.session_state.portfoy.append({"Ad": hisse_kod, "Lot": hisse_lot, "Alış": hisse_alis})
            st.success(f"✅ {hisse_kod} güncellendi!")
            st.rerun()
        
        st.caption("Mevcut: " + ", ".join([f"{p['Ad']}({p['Lot']:.0f})" for p in st.session_state.portfoy]))
    
    # Hesaplama
    sinyaller_kar = []
    sinyaller_zarar = []
    toplam = 0
    toplam_maliyet = 0
    
    for p in st.session_state.portfoy:
        if p["Ad"] == "NAKİT":
            p["Güncel"] = 1.00
            p["F/K"] = "-"
            p["PD/DD"] = "-"
            p["Değişim"] = 0
            p["Beta"] = "-"
            p["52H Dip"] = "-"
            p["52H Zirve"] = "-"
            p["Hacim"] = "-"
            p["Hedef"] = "-"
            p["Konum"] = "-"
        else:
            veri = fiyat_cek(f"{p['Ad']}.IS")
            if veri:
                p["Güncel"] = veri["Fiyat"]
                p["F/K"] = veri["F/K"]
                p["PD/DD"] = veri["PD/DD"]
                p["Değişim"] = veri["Değişim"]
                p["Beta"] = veri["Beta"]
                p["52H Dip"] = veri["52H Dip"]
                p["52H Zirve"] = veri["52H Zirve"]
                p["Hacim"] = veri["Hacim"]
                p["Hedef"] = round(p["Alış"] * 1.20, 2)
                try:
                    dip = float(veri["52H Dip"])
                    zirve = float(veri["52H Zirve"])
                    konum = round(((p["Güncel"] - dip) / (zirve - dip)) * 100, 1)
                    p["Konum"] = f"%{konum} ({'🔴 Zirvede' if konum >= 90 else '🟢 Dipte' if konum <= 20 else '⚪ Orta'})"
                except:
                    p["Konum"] = "-"
            else:
                p["Güncel"] = p["Alış"]
                p["F/K"] = "-"
                p["PD/DD"] = "-"
                p["Değişim"] = 0
                p["Beta"] = "-"
                p["52H Dip"] = "-"
                p["52H Zirve"] = "-"
                p["Hacim"] = "-"
                p["Hedef"] = round(p["Alış"] * 1.20, 2)
                p["Konum"] = "-"
        
        p["Maliyet"] = p["Lot"] * p["Alış"]
        p["Değer"] = p["Lot"] * p["Güncel"]
        p["K/Z"] = p["Değer"] - p["Maliyet"]
        p["K/Z %"] = (p["K/Z"] / p["Maliyet"]) * 100 if p["Maliyet"] > 0 else 0
        toplam += p["Değer"]
        toplam_maliyet += p["Maliyet"]
        
        if p["Ad"] != "NAKİT":
            if p["K/Z %"] >= 20:
                sinyaller_kar.append(p)
            elif p["K/Z %"] <= -7:
                sinyaller_zarar.append(p)
    
    kar_zarar = toplam - toplam_maliyet
    getiri = (kar_zarar / toplam_maliyet) * 100 if toplam_maliyet > 0 else 0
    renk = "#22ab94" if kar_zarar >= 0 else "#f23645"
    
    # Özet kart
    st.markdown(f"""
    <div class="tv-panel" style="text-align:center;">
        <div style="color:#787b86;font-size:12px;">TOPLAM DEĞER</div>
        <div style="font-size:32px;font-weight:700;color:#d1d4dc;">{toplam:,.0f} TL</div>
        <div style="font-size:16px;color:{renk};">{kar_zarar:+,.0f} TL (%{getiri:+.1f})</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sinyaller
    if sinyaller_kar or sinyaller_zarar:
        st.markdown("---")
        st.subheader("⚠️ SİNYALLER")
        for p in sinyaller_kar:
            st.markdown(f"""<div class="tv-panel sinyal-kar"><span style="color:#22ab94;font-weight:600;">🟢 {p['Ad']}</span> %{p['K/Z %']:.1f} kâr → KÂR AL!</div>""", unsafe_allow_html=True)
        for p in sinyaller_zarar:
            st.markdown(f"""<div class="tv-panel sinyal-zarar"><span style="color:#f23645;font-weight:600;">🔴 {p['Ad']}</span> %{p['K/Z %']:.1f} zarar → STOP!</div>""", unsafe_allow_html=True)
    else:
        st.info("✅ Tüm hisseler güvenli aralıkta.")
    
    # Portföy tablosu
    st.markdown("---")
    st.subheader("📋 Portföy Detay")
    
    for i, p in enumerate(st.session_state.portfoy):
        kz_renk = "#22ab94" if p.get('K/Z', 0) >= 0 else "#f23645"
        emoji = "🔴" if p in sinyaller_zarar else "🟢" if p in sinyaller_kar else "⚪"
        sinif = "sinyal-zarar" if p in sinyaller_zarar else "sinyal-kar" if p in sinyaller_kar else "sinyal-normal"
        
        hacim = p.get('Hacim', '-')
        if isinstance(hacim, (int, float)) and hacim != '-':
            if hacim > 1_000_000_000: hacim = f"{hacim/1_000_000_000:.1f}B"
            elif hacim > 1_000_000: hacim = f"{hacim/1_000_000:.1f}M"
        
        st.markdown(f"""
        <div class="tv-panel {sinif}" style="margin-bottom:6px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">
                <span style="color:#d1d4dc;font-weight:600;width:55px;">{emoji} {p['Ad']}</span>
                <span style="color:#787b86;font-size:11px;width:50px;">{p['Lot']:.0f} lot</span>
                <span style="color:#787b86;font-size:11px;width:65px;">Alış:{p['Alış']:.2f}</span>
                <span style="color:#d1d4dc;width:60px;">{p['Güncel']:.2f} TL</span>
                <span style="color:{kz_renk};font-weight:600;width:70px;text-align:right;">%{p.get('K/Z %',0):+.1f}</span>
                <span style="color:#787b86;font-size:10px;width:55px;">Hedef:{p.get('Hedef','-')}</span>
                <span style="color:#787b86;font-size:10px;width:55px;">F/K:{p.get('F/K','-')}</span>
                <span style="color:#787b86;font-size:10px;">PD/DD:{p.get('PD/DD','-')}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:4px;">
                <span style="color:#787b86;font-size:10px;">📊 52H: {p.get('52H Dip','-')} - {p.get('52H Zirve','-')} | Konum: {p.get('Konum','-')}</span>
                <span style="color:#787b86;font-size:10px;">📈 Günlük: %{p.get('Değişim',0):+.1f} | Hacim: {hacim} | Beta: {p.get('Beta','-')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if p["Ad"] != "NAKİT":
            if st.button(f"🗑️ {p['Ad']} kaldır", key=f"sil_{i}"):
                st.session_state.portfoy = [x for x in st.session_state.portfoy if x["Ad"] != p["Ad"]]
                st.warning(f"🗑️ {p['Ad']} kaldırıldı!")
                st.rerun()

# ============================================
# TAB 2: BIST 100 ANALİZ
# ============================================
with tab2:
    st.markdown("---")
    st.subheader("🔍 BIST 100 Derin Analiz")
    
    if st.button("📡 BIST 100 TARA", use_container_width=True):
        with st.spinner("Taranıyor... 1-2 dakika sürebilir"):
            df = bist100_tara()
            
            # Sayısal F/K ve PD/DD filtreleme için dönüştür
            df_num = df.copy()
            df_num["F/K_num"] = pd.to_numeric(df_num["F/K"], errors='coerce')
            df_num["PD/DD_num"] = pd.to_numeric(df_num["PD/DD"], errors='coerce')
            
            st.success(f"✅ {len(df)} hisse tarandı")
            
            # --- ÖZET KARTLAR ---
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                en_ucuz_fk = df_num[df_num["F/K_num"] > 0].nsmallest(1, "F/K_num")
                if len(en_ucuz_fk) > 0:
                    st.markdown(f"""<div class="tv-panel" style="text-align:center;">
                        <div style="color:#787b86;font-size:11px;">EN DÜŞÜK F/K</div>
                        <div style="color:#22ab94;font-size:20px;font-weight:700;">{en_ucuz_fk.iloc[0]['Hisse']}</div>
                        <div style="color:#d1d4dc;">F/K: {en_ucuz_fk.iloc[0]['F/K']}</div>
                    </div>""", unsafe_allow_html=True)
            
            with col2:
                en_ucuz_pddd = df_num[df_num["PD/DD_num"] > 0].nsmallest(1, "PD/DD_num")
                if len(en_ucuz_pddd) > 0:
                    st.markdown(f"""<div class="tv-panel" style="text-align:center;">
                        <div style="color:#787b86;font-size:11px;">EN DÜŞÜK PD/DD</div>
                        <div style="color:#22ab94;font-size:20px;font-weight:700;">{en_ucuz_pddd.iloc[0]['Hisse']}</div>
                        <div style="color:#d1d4dc;">PD/DD: {en_ucuz_pddd.iloc[0]['PD/DD']}</div>
                    </div>""", unsafe_allow_html=True)
            
            with col3:
                en_cok_yukselen = df.nlargest(1, "Değişim")
                if len(en_cok_yukselen) > 0:
                    st.markdown(f"""<div class="tv-panel" style="text-align:center;">
                        <div style="color:#787b86;font-size:11px;">EN ÇOK YÜKSELEN</div>
                        <div style="color:#22ab94;font-size:20px;font-weight:700;">{en_cok_yukselen.iloc[0]['Hisse']}</div>
                        <div style="color:#22ab94;">%{en_cok_yukselen.iloc[0]['Değişim']:+.1f}</div>
                    </div>""", unsafe_allow_html=True)
            
            with col4:
                en_cok_dusen = df.nsmallest(1, "Değişim")
                if len(en_cok_dusen) > 0:
                    st.markdown(f"""<div class="tv-panel" style="text-align:center;">
                        <div style="color:#787b86;font-size:11px;">EN ÇOK DÜŞEN</div>
                        <div style="color:#f23645;font-size:20px;font-weight:700;">{en_cok_dusen.iloc[0]['Hisse']}</div>
                        <div style="color:#f23645;">%{en_cok_dusen.iloc[0]['Değişim']:+.1f}</div>
                    </div>""", unsafe_allow_html=True)
            
            # --- FİLTRELER ---
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                fk_max = st.slider("Maksimum F/K", 1, 50, 20)
            with col2:
                pddd_max = st.slider("Maksimum PD/DD", 0.1, 10.0, 3.0)
            with col3:
                sec = st.selectbox("Sektör", ["Tümü", "Bankalar", "Sanayi", "Holding", "Telekom"])
            
            # Filtrele
            filtreli = df_num[(df_num["F/K_num"] > 0) & (df_num["F/K_num"] <= fk_max) & 
                              (df_num["PD/DD_num"] > 0) & (df_num["PD/DD_num"] <= pddd_max)]
            
            if sec == "Bankalar":
                bankalar = ["AKBNK", "GARAN", "HALKB", "ISCTR", "SKBNK", "TSKB", "VAKBN", "YKBNK", "ALBRK"]
                filtreli = filtreli[filtreli["Hisse"].isin(bankalar)]
            
            st.markdown(f"**🎯 F/K ≤ {fk_max}, PD/DD ≤ {pddd_max} → {len(filtreli)} hisse bulundu**")
            st.dataframe(filtreli[["Hisse", "Fiyat", "F/K", "PD/DD", "Değişim"]].sort_values("F/K_num"), 
                         use_container_width=True, hide_index=True)
            
            # DeepSeek için
            st.markdown("---")
            bist_ds = "BIST 100 ANALİZ:\n"
            for _, row in filtreli.iterrows():
                bist_ds += f"{row['Hisse']}: {row['Fiyat']:.2f} TL | F/K: {row['F/K']} | PD/DD: {row['PD/DD']} | Günlük: %{row['Değişim']:+.1f}\n"
            
            st.components.v1.html(f"""
                <textarea id="bistDs" style="display:none;">{bist_ds}</textarea>
                <button onclick="var t=document.getElementById('bistDs');t.style.display='block';t.select();navigator.clipboard.writeText(t.value);t.style.display='none';"
                style="width:100%;padding:8px;background:#1e222d;color:#787b86;border:1px solid #2a2e39;border-radius:4px;font-size:11px;cursor:pointer;">📋 BIST 100 VERİSİNİ KOPYALA</button>
            """, height=40)

# ============================================
# TAB 3: DEEPSEEK
# ============================================
with tab3:
    st.markdown("---")
    st.subheader("🤖 DeepSeek'e Gönder")
    
    ds_metin = f"BIST: {bist:,} | USD: {usd:.2f} | Alt
