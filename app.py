import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Borsa Asistanım", page_icon="📊", layout="wide")

# ------------------------------------------------------------
# LIDER MİNİ PANEL (En Üst - Sade)
# ------------------------------------------------------------
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

durum_emoji = "🔴" if lider_fiyat <= panik else "🟡" if lider_fiyat < maliyet else "🟢"
durum_yazi = "PANİK! SAT!" if lider_fiyat <= panik else "Zararda" if lider_fiyat < maliyet else "Kârda"

st.markdown(f"""
<div style="
    background: {'#dc3545' if lider_fiyat <= panik else '#ffc107' if lider_fiyat < maliyet else '#28a745'};
    color: {'white' if lider_fiyat <= panik else 'black'};
    padding: 10px 15px;
    border-radius: 8px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
">
    <span style="font-weight: bold; font-size: 18px;">{durum_emoji} LIDER</span>
    <span style="font-size: 20px; font-weight: bold;">{lider_fiyat:.2f} TL</span>
    <span>Maliyet: {maliyet:.2f}</span>
    <span style="color: {'#ffcccc' if lider_fiyat <= panik else '#990000'};">Zarar: {zarar:,.0f} TL (%{zarar_yuzde:.1f})</span>
    <span style="font-size: 12px;">🔴{panik:.2f} | 🟢{hedef:.2f}</span>
</div>
""", unsafe_allow_html=True)

# DeepSeek butonu
lider_veri = f"LIDER: {lider_fiyat:.2f} TL | Maliyet: {maliyet} | Zarar: {zarar:,.0f} TL (%{zarar_yuzde:.1f}) | Panik: {panik:.2f} | Hedef: {hedef:.2f}"

col1, col2 = st.columns([1, 4])
with col1:
    st.components.v1.html(f"""
        <textarea id="liderMini" style="display:none;">{lider_veri}</textarea>
        <button onclick="
            var t = document.getElementById('liderMini');
            t.style.display='block'; t.select();
            navigator.clipboard.writeText(t.value);
            t.style.display='none';
        " style="
            padding: 6px 12px; background: #2a5298; color: white;
            border: none; border-radius: 5px; cursor: pointer;
            font-size: 12px;
        ">📋 Kopyala</button>
    """, height=35)
with col2:
    st.caption("Her gün bu butonla veriyi DeepSeek'e gönder")

st.title("📊 Borsa Asistanım")
st.caption(f"Son güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

st.markdown("---")

# ============================================
# ÜÇ SÜTUNLU ANA EKRAN
# ============================================
sol, orta, sag = st.columns([1, 1, 1])

# -------------------- SOL SÜTUN: DeepSeek --------------------
with sol:
    st.subheader("🤖 DeepSeek")
    
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
        📋 Panoya Kopyala
        </button>
    """, height=50)
    
    st.caption("👆 DeepSeek sohbetine yapıştır")
    
    st.markdown("---")
    st.subheader("📈 Piyasa")
    c1, c2 = st.columns(2)
    c1.metric("BIST", f"{v['bist']:,.0f}")
    c2.metric("USD", f"{v['usd']:.2f}")
    c1.metric("Altın", f"{altin_manual:,.0f}")
    c2.metric("Faiz", f"%{faiz_manual:.1f}")

# -------------------- ORTA SÜTUN: BIST Tarama --------------------
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
            toplam = len(bist50)
            
            for i, (isim, sembol) in enumerate(bist50.items()):
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

# -------------------- SAĞ SÜTUN: Portföy --------------------
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
    
    st.dataframe(pd.DataFrame(portfoy)[["Ad", "Lot", "Fiyat" if "Fiyat" in portfoy[0] else "Alış", "Değer", "K/Z %"]], use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📈 Hisseler")
    c1, c2 = st.columns(2)
    c1.metric("GARAN", f"{v['garan']:.2f}")
    c2.metric("ISCTR", f"{v['isctr']:.2f}")
    c1.metric("SISE", f"{v['sise']:.2f}")
    c2.metric("TTKOM", f"{v['ttkom']:.2f}")

st.markdown("---")

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
# LIDER TAKİP PANELİ
# ------------------------------------------------------------
st.divider()
st.subheader("🚨 LIDER Acil Takip Paneli")

# LIDER verisini çek
try:
    lider = yf.Ticker("LIDER.IS")
    lider_fiyat = round(lider.history(period="1d")['Close'].iloc[-1], 2)
    lider_info = lider.info
    lider_yuksek = lider_info.get('fiftyTwoWeekHigh', 154)
    lider_dusuk = lider_info.get('fiftyTwoWeekLow', 39)
except:
    lider_fiyat = 87.70
    lider_yuksek = 154
    lider_dusuk = 39

# Kullanıcı girişleri
st.write("#### Yatırım Bilgileriniz")
col1, col2 = st.columns(2)
with col1:
    maliyet = st.number_input("Maliyet Fiyatı (TL)", value=98.90, step=0.01)
with col2:
    lot = st.number_input("Lot Adedi", value=342, step=1)

# Hesaplamalar
toplam_yatirim = maliyet * lot
guncel_deger = lider_fiyat * lot
kar_zarar = guncel_deger - toplam_yatirim
kar_zarar_yuzde = (kar_zarar / toplam_yatirim) * 100

# Kritik seviyeler
panik_fiyat = maliyet * 0.90
hedef_fiyat = maliyet * 1.10

# Gösterge paneli
st.write("---")
st.write("#### 📊 Anlık Durum")

col1, col2, col3, col4 = st.columns(4)
col1.metric("LIDER Fiyat", f"{lider_fiyat:.2f} TL")
col2.metric("Güncel Değer", f"{guncel_deger:,.0f} TL")
col3.metric("Kâr/Zarar", f"{kar_zarar:,.0f} TL", delta=f"%{kar_zarar_yuzde:.1f}")
col4.metric("Maliyet", f"{maliyet:.2f} TL")

st.write("---")
st.write("#### 🎯 Kritik Seviyeler")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔴 Panik Satış", f"{panik_fiyat:.2f} TL", delta=f"-{maliyet - panik_fiyat:.2f} TL")
    if lider_fiyat <= panik_fiyat:
        st.error("🚨 PANİK SEVİYESİNDE! HEMEN SAT!")
    else:
        st.info(f"Kalan: {lider_fiyat - panik_fiyat:.2f} TL")

with col2:
    st.metric("🟡 Maliyet", f"{maliyet:.2f} TL", delta="Başabaş")
    if lider_fiyat >= maliyet:
        st.success("✅ Kâra geçtin!")
    else:
        st.warning(f"Zarardasın: -{maliyet - lider_fiyat:.2f} TL")

with col3:
    st.metric("🟢 Hedef Satış", f"{hedef_fiyat:.2f} TL", delta=f"+{hedef_fiyat - maliyet:.2f} TL")
    if lider_fiyat >= hedef_fiyat:
        st.success("🎯 HEDEFTE! KÂRLA SAT!")
    else:
        st.info(f"Kalan: {hedef_fiyat - lider_fiyat:.2f} TL")

# İlerleme çubuğu
st.write("---")
st.write("#### 📈 Fiyat Aralığı")

aralik_yuzde = (lider_fiyat - lider_dusuk) / (lider_yuksek - lider_dusuk)
st.progress(aralik_yuzde)
st.caption(f"52 Hafta: {lider_dusuk:.0f} TL ────────────── {lider_yuksek:.0f} TL")

# Aksiyon butonu
st.write("---")
st.write("#### ⚡ Aksiyon")

col1, col2, col3 = st.columns(3)

with col1:
    if lider_fiyat <= panik_fiyat:
        st.button("🔴 ACİL SATIŞ YAP!", type="primary", use_container_width=True)
    else:
        st.button("🟢 Bekle (Panik Yok)", disabled=True, use_container_width=True)

with col2:
    if lider_fiyat >= hedef_fiyat:
        st.button("🟢 KÂRLA SAT!", type="primary", use_container_width=True)
    else:
        st.button("🟡 Bekle (Hedefte Değil)", disabled=True, use_container_width=True)

with col3:
    st.info(f"Pazartesiye kalan gün: {7 - datetime.now().weekday()}")


st.caption("⚠️ Yatırım tavsiyesi değildir. Veri: Yahoo Finance + Investing.com")
