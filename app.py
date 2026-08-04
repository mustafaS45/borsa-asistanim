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

if "portfoy" not in st.session_state:
    st.session_state.portfoy = [
        {"Ad": "KARCL", "Lot": 47, "Alış": 35.00},
        {"Ad": "GARAN", "Lot": 72, "Alış": 127.90},
        {"Ad": "SISE", "Lot": 130, "Alış": 41.86},
        {"Ad": "AKBNK", "Lot": 110, "Alış": 66.45},
        {"Ad": "ISCTR", "Lot": 734, "Alış": 12.46},
        {"Ad": "NAKİT", "Lot": 2142, "Alış": 1.00},
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
        sil_btn = st.button("🗑️ Sil", use_container_width=True)
    
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
    
    if sil_btn and hisse_kod:
        st.session_state.portfoy = [p for p in st.session_state.portfoy if p["Ad"] != hisse_kod]
        st.warning(f"🗑️ {hisse_kod} silindi!")
        st.rerun()
    
    st.caption("Mevcut: " + ", ".join([f"{p['Ad']}({p['Lot']:.0f})" for p in st.session_state.portfoy]))

# ============================================
# HESAPLAMA
# ============================================
sinyaller_kar = []
sinyaller_zarar = []
toplam = 0
toplam_maliyet = 0

for p in st.session_state.portfoy:
    if p["Ad"] == "NAKİT":
        p["Güncel"] = 1.00
        p["F/K"] = "-"
        p["PD/DD"] = "-"
    else:
        veri = fiyat_cek(f"{p['Ad']}.IS")
        if veri:
            p["Güncel"] = veri["Fiyat"]
            p["F/K"] = veri["F/K"]
            p["PD/DD"] = veri["PD/DD"]
        else:
            p["Güncel"] = p["Alış"]
            p["F/K"] = "-"
            p["PD/DD"] = "-"
    
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
# SİNYALLER
# ============================================
if sinyaller_kar or sinyaller_zarar:
    st.markdown("---")
    st.subheader("⚠️ SİNYALLER")
    
    for p in sinyaller_kar:
        st.markdown(f"""
        <div class="tv-panel sinyal-kar" style="margin-bottom:6px;">
            <span style="color:#22ab94;font-weight:600;">🟢 {p['Ad']}</span> 
            <span style="color:#d1d4dc;">%{p['K/Z %']:.1f} kârda</span>
            <span style="color:#22ab94;font-weight:500;"> → KÂR AL!</span>
        </div>
        """, unsafe_allow_html=True)
    
    for p in sinyaller_zarar:
        st.markdown(f"""
        <div class="tv-panel sinyal-zarar" style="margin-bottom:6px;">
            <span style="color:#f23645;font-weight:600;">🔴 {p['Ad']}</span> 
            <span style="color:#d1d4dc;">%{p['K/Z %']:.1f} zararda</span>
            <span style="color:#f23645;font-weight:500;"> → STOP-LOSS!</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("✅ Tüm hisseler güvenli aralıkta.")

# ============================================
# PORTFÖY TABLOSU
# ============================================
st.markdown("---")
st.subheader("📋 Portföy Detay")

for p in st.session_state.portfoy:
    kz_renk = "#22ab94" if p.get('K/Z', 0) >= 0 else "#f23645"
    emoji = "🔴" if p in sinyaller_zarar else "🟢" if p in sinyaller_kar else "⚪"
    sinif = "sinyal-zarar" if p in sinyaller_zarar else "sinyal-kar" if p in sinyaller_kar else "sinyal-normal"
    
    st.markdown(f"""
    <div class="tv-panel {sinif}" style="margin-bottom:6px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
            <span style="color:#d1d4dc;font-weight:600;width:60px;">{emoji} {p['Ad']}</span>
            <span style="color:#787b86;font-size:12px;width:60px;">{p['Lot']:.0f} lot</span>
            <span style="color:#787b86;font-size:12px;width:75px;">Alış:{p['Alış']:.2f}</span>
            <span style="color:#d1d4dc;width:70px;">{p['Güncel']:.2f} TL</span>
            <span style="color:#d1d4dc;font-weight:500;width:90px;text-align:right;">{p['Değer']:,.0f} TL</span>
            <span style="color:{kz_renk};font-weight:600;width:80px;text-align:right;">%{p.get('K/Z %',0):+.1f}</span>
            <span style="color:#787b86;font-size:11px;">F/K:{p.get('F/K','-')}</span>
            <span style="color:#787b86;font-size:11px;">PD/DD:{p.get('PD/DD','-')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DEEPSEEK VERİSİ
# ============================================
st.markdown("---")
st.subheader("🤖 DeepSeek'e Gönder")

ds_metin = f"BIST: {bist:,} | USD: {usd:.2f}\n"
for p in st.session_state.portfoy:
    if p["Ad"] != "NAKİT":
        ds_metin += f"{p['Ad']}: Lot={p['Lot']:.0f} Alış={p['Alış']:.2f} Güncel={p['Güncel']:.2f} K/Z=%{p.get('K/Z %',0):+.1f} F/K={p.get('F/K','-')} PD/DD={p.get('PD/DD','-')}\n"
    else:
        ds_metin += f"{p['Ad']}: {p['Lot']:,.0f} TL\n"

st.code(ds_metin, language="")

st.components.v1.html(f"""
    <textarea id="dsText" style="display:none;">{ds_metin}</textarea>
    <button onclick="
        var t = document.getElementById('dsText');
        t.style.display='block'; t.select();
        navigator.clipboard.writeText(t.value);
        t.style.display='none';
    " style="width:100%;padding:10px;background:#2962ff;color:white;border:none;border-radius:4px;font-size:14px;font-weight:500;cursor:pointer;">
    📋 PANOYA KOPYALA
    </button>
""", height=50)

st.caption("👆 Tıkla, DeepSeek sohbetine yapıştır (Ctrl+V)")

st.markdown("---")
st.caption("⚠️ Yatırım tavsiyesi değildir.")
