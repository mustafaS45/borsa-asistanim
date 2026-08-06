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

bist = bist_cek()
usd = usd_cek()
altin = altin_cek()
petrol = petrol_cek()
vix = vix_cek()

if vix["Fiyat"] < 15:
    vix_seviye = "🟢 Sakin"
elif vix["Fiyat"] < 25:
    vix_seviye = "⚪ Normal"
elif vix["Fiyat"] < 35:
    vix_seviye = "🟡 Tedirgin"
else:
    vix_seviye = "🔴 Korku"

# ============================================
# ÜST BAR
# ============================================
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    st.markdown(f'<div class="ust-metric"><div class="label">BIST 100</div><div class="value">{bist:,}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="ust-metric"><div class="label">USD/TRY</div><div class="value">{usd:.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="ust-metric"><div class="label">GRAM ALTIN</div><div class="value">{altin["Gram"]:,.0f}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="ust-metric"><div class="label">ONS</div><div class="value">${altin["Ons"]:,.0f}</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="ust-metric"><div class="label">BRENT</div><div class="value">${petrol["Fiyat"]:,.1f}</div></div>', unsafe_allow_html=True)
with col6:
    st.markdown(f'<div class="ust-metric"><div class="label">VIX</div><div class="value">{vix["Fiyat"]:.1f}</div></div>', unsafe_allow_html=True)
with col7:
    st.markdown(f'<div class="ust-metric"><div class="label">SAAT</div><div class="value" style="font-size:14px;">{datetime.now(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")}</div></div>', unsafe_allow_html=True)

# ============================================
# SEKMELER
# ============================================
st.title("📊 Portföy Asistanım")

tab1, tab2, tab3, tab4 = st.tabs(["💼 Portföyüm", "⭐ Takip Listem", "🔍 BIST 100 Analiz", "🤖 DeepSeek"])

# ============================================
# TAB 1: PORTFÖY
# ============================================
with tab1:
    if "portfoy" not in st.session_state:
        st.session_state.portfoy = [
            {"Ad": "GARAN", "Lot": 72, "Alış": 127.90},
            {"Ad": "SISE", "Lot": 130, "Alış": 41.86},
            {"Ad": "AKBNK", "Lot": 110, "Alış": 66.45},
            {"Ad": "ISCTR", "Lot": 907, "Alış": 12.39},
            {"Ad": "NAKİT", "Lot": 5, "Alış": 1.00},
        ]
    
    with st.expander("✏️ Hisse Ekle / Düzenle", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            hisse_kod = st.text_input("Hisse", placeholder="GARAN").upper()
        with col2:
            hisse_lot = st.number_input("Lot", value=1, step=1)
        with col3:
            hisse_alis = st.number_input("Alış Fiyatı", value=1.0, step=0.01)
        
        if st.button("✅ Ekle / Güncelle", use_container_width=True) and hisse_kod:
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
            p["Hedef"] = "-"
            p["Konum"] = "-"
        else:
            veri = fiyat_cek(f"{p['Ad']}.IS")
            if veri:
                p["Güncel"] = veri["Fiyat"]
                p["F/K"] = veri["F/K"]
                p["PD/DD"] = veri["PD/DD"]
                p["Değişim"] = veri["Değişim"]
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
                p["Hedef"] = "-"
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
    
    st.markdown(f"""<div class="tv-panel" style="text-align:center;">
        <div style="color:#787b86;font-size:12px;">TOPLAM DEĞER</div>
        <div style="font-size:32px;font-weight:700;color:#d1d4dc;">{toplam:,.0f} TL</div>
        <div style="font-size:16px;color:{renk};">{kar_zarar:+,.0f} TL (%{getiri:+.1f})</div>
    </div>""", unsafe_allow_html=True)
    
    if sinyaller_kar:
        for p in sinyaller_kar:
            st.markdown(f"""<div class="tv-panel sinyal-kar"><span style="color:#22ab94;">🟢 {p['Ad']}: %{p['K/Z %']:.1f} → KÂR AL!</span></div>""", unsafe_allow_html=True)
    if sinyaller_zarar:
        for p in sinyaller_zarar:
            st.markdown(f"""<div class="tv-panel sinyal-zarar"><span style="color:#f23645;">🔴 {p['Ad']}: %{p['K/Z %']:.1f} → STOP!</span></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    for i, p in enumerate(st.session_state.portfoy):
        kz_renk = "#22ab94" if p.get('K/Z', 0) >= 0 else "#f23645"
        emoji = "🔴" if p in sinyaller_zarar else "🟢" if p in sinyaller_kar else "⚪"
        sinif = "sinyal-zarar" if p in sinyaller_zarar else "sinyal-kar" if p in sinyaller_kar else "sinyal-normal"
        
        st.markdown(f"""<div class="tv-panel {sinif}" style="margin-bottom:6px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:#d1d4dc;font-weight:600;">{emoji} {p['Ad']}</span>
                <span>{p['Lot']:.0f} lot</span>
                <span>Alış:{p['Alış']:.2f}</span>
                <span>{p['Güncel']:.2f} TL</span>
                <span style="color:{kz_renk};">%{p.get('K/Z %',0):+.1f}</span>
                <span style="font-size:10px;">Hedef:{p.get('Hedef','-')}</span>
                <span style="font-size:10px;">F/K:{p.get('F/K','-')}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:4px;font-size:10px;color:#787b86;">
                <span>Konum: {p.get('Konum','-')}</span>
                <span>Günlük: %{p.get('Değişim',0):+.1f}</span>
            </div>
        </div>""", unsafe_allow_html=True)
        
        if p["Ad"] != "NAKİT":
            if st.button(f"🗑️ {p['Ad']} kaldır", key=f"sil_{i}"):
                st.session_state.portfoy = [x for x in st.session_state.portfoy if x["Ad"] != p["Ad"]]
                st.rerun()

# ============================================
# TAB 2: TAKİP LİSTEM
# ============================================
with tab2:
    st.markdown("---")
    st.subheader("⭐ Takip Listem")
    st.caption("Henüz almadığın ama takip ettiğin hisseler")
    
    if "takip" not in st.session_state:
        st.session_state.takip = []
    
    # Ekleme formu
    with st.expander("➕ Hisse Ekle"):
        takip_kod = st.text_input("Hisse Kodu", placeholder="THYAO", key="takip_input").upper()
        if st.button("✅ Takibe Ekle") and takip_kod:
            if takip_kod not in st.session_state.takip:
                st.session_state.takip.append(takip_kod)
                st.success(f"✅ {takip_kod} takibe eklendi!")
                st.rerun()
            else:
                st.warning("Bu hisse zaten listede!")
    
    if st.session_state.takip:
        st.markdown("---")
        st.markdown(f"**📋 {len(st.session_state.takip)} hisse takip ediliyor**")
        
        takip_verileri = []
        for hisse in st.session_state.takip:
            veri = fiyat_cek(f"{hisse}.IS")
            if veri:
                takip_verileri.append({
                    "Hisse": hisse,
                    "Fiyat": veri["Fiyat"],
                    "F/K": veri["F/K"],
                    "PD/DD": veri["PD/DD"],
                    "Günlük": veri["Değişim"],
                    "52H": f"{veri.get('52H Dip','-')}-{veri.get('52H Zirve','-')}"
                })
        
        if takip_verileri:
            df_takip = pd.DataFrame(takip_verileri)
            
            for i, row in df_takip.iterrows():
                renk = "#22ab94" if row["Günlük"] >= 0 else "#f23645"
                st.markdown(f"""<div class="tv-panel sinyal-normal" style="margin-bottom:4px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#d1d4dc;font-weight:600;">⭐ {row['Hisse']}</span>
                        <span style="color:#d1d4dc;">{row['Fiyat']:.2f} TL</span>
                        <span style="color:{renk};">%{row['Günlük']:+.1f}</span>
                        <span style="font-size:11px;">F/K:{row['F/K']}</span>
                        <span style="font-size:11px;">PD/DD:{row['PD/DD']}</span>
                    </div>
                    <div style="font-size:10px;color:#787b86;">52H: {row['52H']}</div>
                </div>""", unsafe_allow_html=True)
                
                # Kaldır butonu
                if st.button(f"🗑️ {row['Hisse']} listeden çıkar", key=f"takip_sil_{i}"):
                    st.session_state.takip.remove(row['Hisse'])
                    st.rerun()
    else:
        st.info("Henüz takip listesi boş. Yukarıdan hisse ekleyebilirsin.")

# ============================================
# TAB 3: BIST 100 ANALİZ
# ============================================
with tab3:
    st.markdown("---")
    st.subheader("🔍 BIST 100 Analiz")
    
    if st.button("📡 TARA", use_container_width=True):
        with st.spinner("Taranıyor..."):
            bist100_list = {
                "AEFES": "AEFES.IS", "AGHOL": "AGHOL.IS", "AKBNK": "AKBNK.IS",
                "ASELS": "ASELS.IS", "BIMAS": "BIMAS.IS", "DOHOL": "DOHOL.IS",
                "EKGYO": "EKGYO.IS", "ENKAI": "ENKAI.IS", "EREGL": "EREGL.IS",
                "FROTO": "FROTO.IS", "GARAN": "GARAN.IS", "HALKB": "HALKB.IS",
                "ISCTR": "ISCTR.IS", "KCHOL": "KCHOL.IS", "KRDMD": "KRDMD.IS",
                "MAVI": "MAVI.IS", "MGROS": "MGROS.IS", "ODAS": "ODAS.IS",
                "PETKM": "PETKM.IS", "PGSUS": "PGSUS.IS", "SAHOL": "SAHOL.IS",
                "SASA": "SASA.IS", "SISE": "SISE.IS", "TCELL": "TCELL.IS",
                "THYAO": "THYAO.IS", "TOASO": "TOASO.IS", "TSKB": "TSKB.IS",
                "TTKOM": "TTKOM.IS", "TUPRS": "TUPRS.IS", "ULKER": "ULKER.IS",
                "VAKBN": "VAKBN.IS", "VESTL": "VESTL.IS", "YKBNK": "YKBNK.IS",
                "ZOREN": "ZOREN.IS", "ARCLK": "ARCLK.IS", "CCOLA": "CCOLA.IS",
                "CIMSA": "CIMSA.IS", "ECZYT": "ECZYT.IS", "GUBRF": "GUBRF.IS",
                "HEKTS": "HEKTS.IS", "OTKAR": "OTKAR.IS", "TAVHL": "TAVHL.IS",
                "TTRAK": "TTRAK.IS", "YATAS": "YATAS.IS", "ALARK": "ALARK.IS",
                "ASTOR": "ASTOR.IS", "AYGAZ": "AYGAZ.IS", "BRSAN": "BRSAN.IS",
            }
            
            sonuclar = []
            for isim, sembol in bist100_list.items():
                veri = fiyat_cek(sembol)
                if veri:
                    sonuclar.append({
                        "Hisse": isim, "Fiyat": veri["Fiyat"],
                        "F/K": veri["F/K"], "PD/DD": veri["PD/DD"],
                        "Günlük": veri["Değişim"]
                    })
            
            df = pd.DataFrame(sonuclar)
            df["F/K_num"] = pd.to_numeric(df["F/K"], errors='coerce')
            df["PD/DD_num"] = pd.to_numeric(df["PD/DD"], errors='coerce')
            
            st.success(f"✅ {len(df)} hisse tarandı")
            
            # Enler
            c1, c2 = st.columns(2)
            with c1:
                en_ucuz_fk = df[df["F/K_num"] > 0].nsmallest(1, "F/K_num")
                if len(en_ucuz_fk) > 0:
                    st.metric("En Düşük F/K", f"{en_ucuz_fk.iloc[0]['Hisse']} ({en_ucuz_fk.iloc[0]['F/K']})")
            with c2:
                en_ucuz_pddd = df[df["PD/DD_num"] > 0].nsmallest(1, "PD/DD_num")
                if len(en_ucuz_pddd) > 0:
                    st.metric("En Düşük PD/DD", f"{en_ucuz_pddd.iloc[0]['Hisse']} ({en_ucuz_pddd.iloc[0]['PD/DD']})")
            
            # Filtre
            fk_max = st.slider("Maks F/K", 1, 30, 15)
            filtreli = df[(df["F/K_num"] > 0) & (df["F/K_num"] <= fk_max)]
            filtreli = filtreli.sort_values("F/K_num")
            
            st.dataframe(filtreli[["Hisse", "Fiyat", "F/K", "PD/DD", "Günlük"]], use_container_width=True, hide_index=True)

# ============================================
# TAB 4: DEEPSEEK
# ============================================
with tab4:
    st.markdown("---")
    st.subheader("🤖 DeepSeek'e Gönder")
    
    ds_metin = f"BIST: {bist:,} | USD: {usd:.2f} | Altın: {altin['Gram']:,.0f} TL/g | Petrol: ${petrol['Fiyat']:,.1f} | VIX: {vix['Fiyat']:.1f}\n"
    for p in st.session_state.portfoy:
        if p["Ad"] != "NAKİT":
            ds_metin += f"{p['Ad']}: Lot={p['Lot']:.0f} Alış={p['Alış']:.2f} Güncel={p['Güncel']:.2f} K/Z=%{p.get('K/Z %',0):+.1f} F/K={p.get('F/K','-')} PD/DD={p.get('PD/DD','-')}\n"
        else:
            ds_metin += f"{p['Ad']}: {p['Lot']:,.0f} TL\n"
    
    st.code(ds_metin, language="")
    
    st.components.v1.html(f"""
        <textarea id="dsText" style="display:none;">{ds_metin}</textarea>
        <button onclick="var t=document.getElementById('dsText');t.style.display='block';t.select();navigator.clipboard.writeText(t.value);t.style.display='none';"
        style="width:100%;padding:10px;background:#2962ff;color:white;border:none;border-radius:4px;font-size:14px;font-weight:500;cursor:pointer;">📋 PANOYA KOPYALA</button>
    """, height=50)

st.markdown("---")
st.caption("⚠️ Yatırım tavsiyesi değildir.")
