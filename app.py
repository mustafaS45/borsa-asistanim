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
# BIST TÜM HİSSELERİ (İŞ YATIRIM API)
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
    
    # Yedek liste
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
        "ADEL": "ADEL.IS", "AFYON": "AFYON.IS", "AKCNS": "AKCNS.IS",
        "AKENR": "AKENR.IS", "AKGRT": "AKGRT.IS", "ALGYO": "ALGYO.IS",
        "ANHYT": "ANHYT.IS", "ANSGR": "ANSGR.IS", "ARENA": "ARENA.IS",
        "AVGYO": "AVGYO.IS", "BANVT": "BANVT.IS", "BIZIM": "BIZIM.IS",
        "BJKAS": "BJKAS.IS", "BRISA": "BRISA.IS", "CLEBI": "CLEBI.IS",
        "DAGI": "DAGI.IS", "DESA": "DESA.IS", "DYOBY": "DYOBY.IS",
        "EGEEN": "EGEEN.IS", "ERBOS": "ERBOS.IS", "FMIZP": "FMIZP.IS",
        "GEDIK": "GEDIK.IS", "GSDHO": "GSDHO.IS", "GSRAY": "GSRAY.IS",
        "HURGZ": "HURGZ.IS", "INDES": "INDES.IS", "JANTS": "JANTS.IS",
        "KAREL": "KAREL.IS", "KARTN": "KARTN.IS", "KLNMA": "KLNMA.IS",
        "KNFRT": "KNFRT.IS", "KRPLS": "KRPLS.IS", "LIDER": "LIDER.IS",
        "LOGO": "LOGO.IS", "MAKTK": "MAKTK.IS", "MARTI": "MARTI.IS",
        "MEDTR": "MEDTR.IS", "MEGAP": "MEGAP.IS", "METRO": "METRO.IS",
        "MHRGY": "MHRGY.IS", "MNDRS": "MNDRS.IS", "MOBTL": "MOBTL.IS",
        "MPARK": "MPARK.IS", "NETAS": "NETAS.IS", "NTHOL": "NTHOL.IS",
        "OBAMS": "OBAMS.IS", "ORCAY": "ORCAY.IS", "OSTIM": "OSTIM.IS",
        "PARSN": "PARSN.IS", "PENGD": "PENGD.IS", "POLHO": "POLHO.IS",
        "PRKME": "PRKME.IS", "PRZMA": "PRZMA.IS", "RALYH": "RALYH.IS",
        "RODRG": "RODRG.IS", "RTALB": "RTALB.IS", "RUBNS": "RUBNS.IS",
        "SAMAT": "SAMAT.IS", "SARKY": "SARKY.IS", "SELEC": "SELEC.IS",
        "SILVR": "SILVR.IS", "SNGYO": "SNGYO.IS", "SUMAS": "SUMAS.IS",
        "TABGD": "TABGD.IS", "TARKM": "TARKM.IS", "TBORG": "TBORG.IS",
        "TEKTU": "TEKTU.IS", "TGSAS": "TGSAS.IS", "TMSN": "TMSN.IS",
        "TRCAS": "TRCAS.IS", "TSPOR": "TSPOR.IS", "TUCLK": "TUCLK.IS",
        "TUREX": "TUREX.IS", "UFUK": "UFUK.IS", "ULAS": "ULAS.IS",
        "UNLU": "UNLU.IS", "UZERB": "UZERB.IS", "VAKFN": "VAKFN.IS",
        "VANGD": "VANGD.IS", "VERTU": "VERTU.IS", "YAPRK": "YAPRK.IS",
        "YAYLA": "YAYLA.IS", "YEOTK": "YEOTK.IS", "YESIL": "YESIL.IS",
        "YGYO": "YGYO.IS", "YONGA": "YONGA.IS", "YUNSA": "YUNSA.IS",
    }

BIST_SEMBOLLER = tum_hisseleri_cek()

# ============================================
# HİSSE ADLARI (KOD -> İSİM)
# ============================================
HISSE_ADLARI = {
    "AEFES": "Anadolu Efes", "AGHOL": "Agrotech", "AKBNK": "Akbank",
    "AKFGY": "Akfen GMYO", "AKSA": "Aksa", "ALARK": "Alarko Holding",
    "ALBRK": "Albaraka Türk", "ALFAS": "Alfa Solar", "ARCLK": "Arçelik",
    "ASELS": "Aselsan", "ASTOR": "Astor Enerji", "ASUZU": "Anadolu Isuzu",
    "AYGAZ": "Aygaz", "BAGFS": "Bağfaş", "BERA": "Bera Holding",
    "BIMAS": "Bim", "BRSAN": "Borusan", "BRYAT": "Borusan Yatırım",
    "BUCIM": "Bursa Çimento", "CANTE": "Can2 Termik", "CCOLA": "Coca Cola İçecek",
    "CIMSA": "Çimsa", "CWENE": "CW Enerji", "DOHOL": "Doğan Holding",
    "ECILC": "Eczacıbaşı İlaç", "ECZYT": "Eczacıbaşı Yatırım", "EGGUB": "Ege Gübre",
    "EKGYO": "Emlak Konut GMYO", "ENJSA": "Enerjisa", "ENKAI": "Enka İnşaat",
    "EREGL": "Ereğli Demir Çelik", "EUPWR": "Europower", "FENER": "Fenerbahçe",
    "FROTO": "Ford Otosan", "GARAN": "Garanti Bankası", "GESAN": "Gesan",
    "GOLTS": "Göltaş", "GUBRF": "Gübre Fabrikası", "HALKB": "Halkbank",
    "HEKTS": "Hektaş", "IPEKE": "İpek Enerji", "ISCTR": "İş Bankası (C)",
    "ISGYO": "İş GMYO", "ISMEN": "İş Menkul", "IZENR": "İz Enerji",
    "KAYSE": "Kayseri Şeker", "KCAER": "Kocaer", "KCHOL": "Koç Holding",
    "KLSER": "Kaleseramik", "KONTR": "Kontrolmatik", "KONYA": "Konya Çimento",
    "KOZAA": "Koza Altın", "KOZAL": "Koza Madencilik", "KRDMD": "Kardemir",
    "MAVI": "Mavi Giyim", "MGROS": "Migros", "MIATK": "Mia Teknoloji",
    "ODAS": "Odaş", "OTKAR": "Otokar", "OYAKC": "Oyak Çimento",
    "PETKM": "Petkim", "PGSUS": "Pegasus", "QUAGR": "Qua Granite",
    "SAHOL": "Sabancı Holding", "SASA": "Sasa", "SISE": "Şişe Cam",
    "SKBNK": "Şekerbank", "SMRTG": "Smart Güneş", "SOKM": "Şok Market",
    "TATEN": "Tat Enerji", "TAVHL": "Tav Havalimanları", "TCELL": "Turkcell",
    "THYAO": "THY", "TKFEN": "Tekfen", "TOASO": "Tofaş Oto",
    "TSKB": "TSKB", "TTKOM": "Türk Telekom", "TTRAK": "Türk Traktör",
    "TUKAS": "Tukaş", "TUPRS": "Tüpraş", "ULKER": "Ülker",
    "VAKBN": "Vakıfbank", "VESTL": "Vestel", "YATAS": "Yataş",
    "YGGYO": "Yeni Gimat GMYO", "YKBNK": "Yapı Kredi", "ZOREN": "Zorlu Enerji",
    "ADEL": "Adel Kalem", "AFYON": "Afyon Çimento", "AKCNS": "Akçansa",
    "AKENR": "Ak Enerji", "AKGRT": "Aksigorta", "ALGYO": "Alarko GMYO",
    "ANHYT": "Anadolu Hayat", "ANSGR": "Anadolu Sigorta", "ARENA": "Arena Bilgisayar",
    "BANVT": "Banvit", "BIZIM": "Bizim Mağazaları", "BJKAS": "Beşiktaş",
    "BRISA": "Brisa", "CLEBI": "Çelebi", "DAGI": "Dağıtım",
    "DESA": "Desa Deri", "DYOBY": "Dyo Boya", "EGEEN": "Ege Endüstri",
    "ERBOS": "Erbosan", "FMIZP": "F-M İzmit Piston", "GEDIK": "Gedik Yatırım",
    "GSDHO": "GSD Holding", "GSRAY": "Galatasaray", "HURGZ": "Hürriyet",
    "INDES": "İndeks Bilgisayar", "JANTS": "Jantsa", "KAREL": "Karel",
    "KARTN": "Kartonsan", "KLNMA": "Klimasan", "KNFRT": "Konfrut",
    "KRPLS": "Koroplast", "LIDER": "Lider Turizm", "LOGO": "Logo Yazılım",
    "MAKTK": "Makina Takım", "MARTI": "Martı Otel", "MEDTR": "Meditera",
    "MEGAP": "Mega Polietilen", "METRO": "Metro Holding", "MHRGY": "MHR GMYO",
    "MNDRS": "Menderes", "MOBTL": "Mobiltel", "MPARK": "Medical Park",
    "NETAS": "Netaş", "NTHOL": "Net Holding", "OBAMS": "Obam",
    "ORCAY": "Orçay", "OSTIM": "Ostim", "PARSN": "Parsan",
    "PENGD": "Pengd", "POLHO": "Polisan Holding", "PRKME": "Park Elek.",
    "PRZMA": "Prizma", "RALYH": "Ral Yatırım", "RODRG": "Rodrigo",
    "RTALB": "RTA Laboratuvar", "RUBNS": "Rubenis", "SAMAT": "Samat",
    "SARKY": "Sarkuysan", "SELEC": "Selçuk Ecza", "SILVR": "Silverline",
    "SNGYO": "Sönmez GMYO", "SUMAS": "Sumaş", "TABGD": "Tab Gıda",
    "TARKM": "Tarkim", "TBORG": "Türk Traktör Borç", "TEKTU": "Tek-Art Turizm",
    "TGSAS": "TGS", "TMSN": "Tümosan", "TRCAS": "Türk Traktör",
    "TSPOR": "Trabzonspor", "TUCLK": "Tuğçelik", "TUREX": "Tureks",
    "UFUK": "Ufuk Yatırım", "ULAS": "Ulaşlar", "UNLU": "Ünlü Yatırım",
    "UZERB": "Uzertaş", "VAKFN": "Vakıf Finans", "VANGD": "Van Gıda",
    "VERTU": "Vertu", "YAPRK": "Yaprak", "YAYLA": "Yayla",
    "YEOTK": "Yeo Teknoloji", "YESIL": "Yeşil GMYO", "YGYO": "Y GMYO",
    "YONGA": "Yonga", "YUNSA": "Yünsa",
}

# ============================================
# VERİ ÇEKME FONKSİYONLARI
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

# --- SOL: DeepSeek + Hisse Arama ---
with sol:
    st.markdown('<h3>🤖 DEEPSEEK</h3>', unsafe_allow_html=True)
    
    deepseek_metni = f"""BIST: {pv['bist']:,} | USD: {pv['usd']:.2f} | Altın: 6170 | Faiz: %37"""
    
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

# --- ORTA: BIST 100 + Portföy ---
with orta:
    st.markdown('<h3>🔍 BIST 100 TARAMA</h3>', unsafe_allow_html=True)
    
    if st.button("📡 BIST TÜM HİSSELERİ TARA", use_container_width=True):
        with st.spinner("Taranıyor..."):
            sonuclar = []
            progress = st.progress(0)
            toplam = len(BIST_SEMBOLLER)
            
            for i, (isim, sembol) in enumerate(BIST_SEMBOLLER.items()):
                veri = fiyat_cek(sembol)
                if veri:
                    sonuclar.append({
                        "Hisse": isim, "Fiyat": veri['Fiyat'],
                        "F/K": veri['F/K'], "PD/DD": veri['PD/DD']
                    })
                progress.progress((i + 1) / toplam)
            
            progress.empty()
            st.success(f"✅ {len(sonuclar)} hisse tarandı")
            st.dataframe(pd.DataFrame(sonuclar), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            bist_deepseek = "BIST TÜM HİSSELER:\n"
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
                📋 TÜM VERİYİ KOPYALA</button>
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
                    st.caption("🔍 Bulunan hisseler:")
                    for o in oneriler[:8]:
                        st.caption(f"  • {o}")
            
            col1, col2 = st.columns(2)
            with col1: h_lot = st.number_input("Lot", value=1, step=1)
            with col2: h_alis = st.number_input("Alış Fiyatı", value=1.0, step=0.01)
            
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
                    st.success(f"✅ {gercek_kod} eklendi! (Nakitten {maliyet:,.0f} TL düşüldü)")
                    st.rerun()
                else:
                    st.error(f"❌ '{h_ad}' BIST'te bulunamadı!")
    
    toplam = 0
    toplam_maliyet = 0
    sat_sinyalleri = []
    
    for p in st.session_state.portfoy:
        if p["Ad"] == "NAKİT":
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
        
        if p["Ad"] != "NAKİT" and p["K/Z %"] <= -7:
            sat_sinyalleri.append(f"🔴 {p['Ad']}: %{p['K/Z %']:.1f} zarar - STOP-LOSS!")
        elif p["Ad"] != "NAKİT" and p["K/Z %"] >= 20:
            sat_sinyalleri.append(f"🟢 {p['Ad']}: %{p['K/Z %']:.1f} kâr - KÂR AL!")
    
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
    
    for p in st.session_state.portfoy:
        if p["Ad"] not in BIST_SEMBOLLER and p["Ad"] != "NAKİT":
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
    
    if st.button("🔄 Portföyü Sıfırla", use_container_width=True):
        st.session_state.portfoy = [{"Ad": "NAKİT", "Lot": 36500, "Alış": 1.00}]
        st.rerun()

# --- SAĞ: Gün Sonu Raporu ---
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
        kalan_dk = 30 - dakika if dakika <= 30 else 90 - dakika
        kalan_saat = 17 - saat if dakika <= 30 else 18 - saat
        st.info(f"⏳ Gün sonu raporu saat 18:30'da.\nKalan: {kalan_saat}s {kalan_dk}dk")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance")
