import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz

st.set_page_config(page_title="Portföy Asistanım", page_icon="📊", layout="wide")

# ============================================
# TEMA
# ============================================
st.markdown("""
<style>
    .stApp { background: #131722; }
    .main .block-container { padding: 1.5rem 2rem; max-width: 1000px; }
    
    .tv-panel {
        background: #1e222d; border: 1px solid #2a2e39;
        border-radius: 6px; padding: 16px; margin-bottom: 12px;
    }
    .tv-panel.sat { border-left: 3px solid #f23645; }
    
    .stButton > button {
        background: #2962ff !important; color: white !important;
        border: none !important; border-radius: 4px !important;
        padding: 8px 16px !important; font-weight: 500 !important; width: 100%;
    }
    
    h1, h2, h3 { color: #d1d4dc !important; }
    hr { border-color: #2a2e39 !important; }
    
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: #1e222d !important; color: #d1d4dc !important;
        border: 1px solid #2a2e39 !important; border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# VERİ ÇEKME
# ============================================
@st.cache_data(ttl=300)
def fiyat_cek(sembol):
    try:
        f = round(yf.Ticker(sembol).history(period="1d")['Close'].iloc[-1], 2)
        info = yf.Ticker(sembol).info
        return {"Fiyat": f, "F/K": info.get("trailingPE","-"), "PD/DD": info.get("priceToBook","-")}
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

bist = bist_cek()
usd = usd_cek()

# ============================================
# BAŞLIK
# ============================================
st.title("📊 Portföy Asistanım")
st.caption(f"BIST: {bist:,} | USD: {usd:.2f} | {datetime.now(pytz.timezone('Europe/Istanbul')).strftime('%H:%M')}")

# ============================================
# PORTFÖY GİRİŞİ
# ============================================
st.markdown("---")
st.subheader("💼 Portföyüm")

# Başlangıç portföyü
if "portfoy" not in st.session_state:
    st.session_state.portfoy = [
        {"Ad": "KARCL", "Lot": 47, "Alış": 35.00},
        {"Ad": "GARAN", "Lot": 72, "Alış": 127.90},
        {"Ad": "SISE", "Lot": 130, "Alış": 41.86},
        {"Ad": "AKBNK", "Lot": 110, "Alış": 66.45},
        {"Ad": "ISCTR", "Lot": 734, "Alış": 12.46},
        {"Ad": "NAKİT", "Lot": 2142, "Alış": 1.00},
    ]

# Düzenleme
with st.expander("✏️ Portföyü Düzenle"):
    yeni = st.text_area("Hisse, Lot, Alış (alt alta)", 
        value="KARCL,47,35.00\nGARAN,72,127.90\nSISE,130,41.86\nAKBNK,110,66.45\nISCTR,734,12.46\nNAKİT,2142,1.00",
        height=150)
    
    if st.button("💾 Kaydet", use_container_width=True):
        portfoy = []
        for satir in yeni.strip().split("\n"):
            parca = satir.strip().split(",")
            if len(parca) == 3:
                portfoy.append({"Ad": parca[0].strip().upper(), "Lot": float(parca[1]), "Alış": float(parca[2])})
        st.session_state.portfoy = portfoy
        st.success("✅ Kaydedildi!")
        st.rerun()

# ============================================
# HESAPLAMA
# ============================================
sinyaller = []
toplam = 0
toplam_maliyet = 0

for p in st.session_state.portfoy:
    if p["Ad"] == "NAKİT":
        p["Güncel"] = 1.00
    else:
        veri = fiyat_cek(f"{p['Ad']}.IS")
        p["Güncel"] = veri["Fiyat"] if veri else p["Alış"]
    
    p["Maliyet"] = p["Lot"] * p["Alış"]
    p["Değer"] = p["Lot"] * p["Güncel"]
    p["K/Z"] = p["Değer"] - p["Maliyet"]
    p["K/Z %"] = (p["K/Z"] / p["Maliyet"]) * 100 if p["Maliyet"] > 0 else 0
    toplam += p["Değer"]
    toplam_maliyet += p["Maliyet"]
    
    if p["Ad"] != "NAKİT" and p["K/Z %"] >= 20:
        sinyaller.append(f"🟢 {p['Ad']}: %{p['K/Z %']:.0f} kâr → KÂR AL!")
    elif p["Ad"] != "NAKİT" and p["K/Z %"] <= -7:
        sinyaller.append(f"🔴 {p['Ad']}: %{p['K/Z %']:.0f} zarar → STOP!")

kar_zarar = toplam - toplam_maliyet
getiri = (kar_zarar / toplam_maliyet) * 100 if toplam_maliyet > 0 else 0
renk = "#22ab94" if kar_zarar >= 0 else "#f23645"

# ============================================
# ÖZET KART
# ============================================
st.markdown(f"""
<div class="tv-panel" style="text-align:center;">
    <div style="color:#787b86;font-size:12px;">TOPLAM DEĞER</div>
    <div style="font-size:32px;font-weight:700;color:#d1d4dc;">{toplam:,.0f} TL</div>
    <div style="font-size:16px;color:{renk};">{kar_zarar:+,.0f} TL (%{getiri:+.1f})</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# PORTFÖY TABLOSU
# ============================================
st.subheader("📋 Detay")

for p in st.session_state.portfoy:
    kz_renk = "#22ab94" if p.get('K/Z', 0) >= 0 else "#f23645"
    emoji = "🔴" if p.get('K/Z %', 0) <= -7 else "🟢" if p.get('K/Z %', 0) >= 20 else "⚪"
    
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #2a2e39;">
        <div style="width:80px;"><span style="color:#d1d4dc;font-weight:600;">{emoji} {p['Ad']}</span></div>
        <div style="color:#787b86;font-size:12px;width:80px;">{p['Lot']:.0f} lot</div>
        <div style="color:#787b86;font-size:12px;width:80px;">Alış:{p['Alış']:.2f}</div>
        <div style="color:#d1d4dc;width:80px;">{p['Güncel']:.2f} TL</div>
        <div style="color:#d1d4dc;font-weight:500;width:100px;text-align:right;">{p['Değer']:,.0f} TL</div>
        <div style="color:{kz_renk};font-weight:500;width:100px;text-align:right;">%{p.get('K/Z %',0):+.1f}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SAT SİNYALLERİ
# ============================================
st.markdown("---")
st.subheader("⚠️ Sinyaller")

if sinyaller:
    for s in sinyaller:
        renk_s = "#f23645" if "🔴" in s else "#22ab94"
        st.markdown(f'<div class="tv-panel sat" style="border-left:3px solid {renk_s};"><span style="color:#d1d4dc;">{s}</span></div>', unsafe_allow_html=True)
else:
    st.success("✅ Tüm hisseler güvenli aralıkta.")

# ============================================
# DEEPSEEK VERİSİ
# ============================================
st.markdown("---")
st.subheader("🤖 DeepSeek'e Gönder")

ds_metin = f"BIST: {bist:,} | USD: {usd:.2f}\n"
for p in st.session_state.portfoy:
    ds_metin += f"{p['Ad']}: Lot={p['Lot']:.0f} Alış={p['Alış']:.2f} Güncel={p['Güncel']:.2f} K/Z=%{p.get('K/Z %',0):+.1f}\n"

st.code(ds_metin, language="")
st.download_button("📋 Veriyi İndir", ds_metin, "portfoy.txt")

st.markdown("---")
st.caption("⚠️ Yatırım tavsiyesi değildir.")
