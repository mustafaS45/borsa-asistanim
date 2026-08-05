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
    .main .block-container { padding: 1.5rem 2rem; max-width: 1100px; }
    
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
    """VIX - Korku Endeksi"""
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

# VIX seviye yorumu
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
# ÜST BAR - 7'Lİ PİYASA ÖZETİ
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
# BAŞLIK
# ============================================
st.title("📊 Portföy Asistanım")
st.caption(f"{datetime.now(pytz.timezone('Europe/Istanbul')).strftime('%H:%M')} | Altın: {altin['Gram']:,.0f} TL/g | Petrol: ${petrol['Fiyat']:,.1f} | VIX: {vix['Fiyat']:.1f} ({vix_seviye})")

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
            <span style="color:#787b86;font-size:11px;float:right;">Hedef: {p.get('Hedef','-')} TL | 52H: {p.get('Konum','-')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    for p in sinyaller_zarar:
        st.markdown(f"""
        <div class="tv-panel sinyal-zarar" style="margin-bottom:6px;">
            <span style="color:#f23645;font-weight:600;">🔴 {p['Ad']}</span> 
            <span style="color:#d1d4dc;">%{p['K/Z %']:.1f} zararda</span>
            <span style="color:#f23645;font-weight:500;"> → STOP-LOSS!</span>
            <span style="color:#787b86;font-size:11px;float:right;">Hedef: {p.get('Hedef','-')} TL | 52H: {p.get('Konum','-')}</span>
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
    
    hacim = p.get('Hacim', '-')
    if isinstance(hacim, (int, float)) and hacim != '-':
        if hacim > 1_000_000_000:
            hacim = f"{hacim/1_000_000_000:.1f}B"
        elif hacim > 1_000_000:
            hacim = f"{hacim/1_000_000:.1f}M"
        elif hacim > 1_000:
            hacim = f"{hacim/1_000:.0f}B"
    
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

# ============================================
# PİYASA ETKİ ANALİZİ
# ============================================
st.markdown("---")
st.subheader("🌍 Piyasa Etki Analizi")

col1, col2, col3 = st.columns(3)

with col1:
    if altin["Ons Değişim"] > 1:
        altin_yorum = "🟡 Altın yükseliyor → Risk iştahı azalabilir, banka hisseleri baskılanabilir."
    elif altin["Ons Değişim"] < -1:
        altin_yorum = "🟢 Altın düşüyor → Risk iştahı artıyor, bankalar için olumlu."
    else:
        altin_yorum = "⚪ Altın yatay → Piyasa dengeli."
    
    st.markdown(f"""
    <div class="tv-panel">
        <div style="color:#ff9800;font-weight:600;">🥇 Altın</div>
        <div style="color:#d1d4dc;margin-top:4px;">{altin['Gram']:,.0f} TL/g | %{altin['Ons Değişim']:+.1f}</div>
        <div style="color:#787b86;font-size:12px;margin-top:6px;">{altin_yorum}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if petrol["Değişim"] > 2:
        petrol_yorum = "🔴 Petrol yükseliyor → Enerji maliyetleri artar."
    elif petrol["Değişim"] < -2:
        petrol_yorum = "🟢 Petrol düşüyor → Maliyetler azalır."
    else:
        petrol_yorum = "⚪ Petrol yatay."
    
    st.markdown(f"""
    <div class="tv-panel">
        <div style="color:#ff9800;font-weight:600;">🛢️ Petrol</div>
        <div style="color:#d1d4dc;margin-top:4px;">${petrol['Fiyat']:,.1f} | %{petrol['Değişim']:+.1f}</div>
        <div style="color:#787b86;font-size:12px;margin-top:6px;">{petrol_yorum}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if vix["Fiyat"] < 15:
        vix_yorum = "🟢 Piyasa sakin → Hisseler için ideal ortam."
    elif vix["Fiyat"] < 25:
        vix_yorum = "⚪ Normal seviye → Korku yok."
    elif vix["Fiyat"] < 35:
        vix_yorum = "🟡 Piyasa tedirgin → Temkinli ol, stop-loss'ları kontrol et."
    else:
        vix_yorum = "🔴 YÜKSEK KORKU → Nakitini artır, hisse alımını durdur!"
    
    st.markdown(f"""
    <div class="tv-panel">
        <div style="color:#ff9800;font-weight:600;">😱 VIX Korku</div>
        <div style="color:#d1d4dc;margin-top:4px;">{vix['Fiyat']:.1f} ({vix_seviye})</div>
        <div style="color:#787b86;font-size:12px;margin-top:6px;">{vix_yorum}</div>
    </div>
    """, unsafe_allow_html=True)

# VIX uyarısı
if vix["Fiyat"] >= 35:
    st.error("🚨 VIX 35 üzerinde! Piyasada korku hâkim. Yeni alım yapma, nakit oranını artır, stop-loss'ları sıkılaştır!")
elif vix["Fiyat"] >= 25:
    st.warning("⚠️ VIX 25 üzerinde. Piyasa tedirgin. Stop-loss seviyelerini kontrol et.")

# ============================================
# GÜN SONU RAPORU
# ============================================
st.markdown("---")
st.subheader("📊 Gün Sonu Raporu")

tz = pytz.timezone('Europe/Istanbul')
ts = datetime.now(tz)

if ts.hour >= 18:
    st.markdown('<h3 class="rapor-baslik">🔔 GÜN SONU ÖZETİ</h3>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="tv-panel">
        <div style="display:flex;justify-content:space-between;">
            <span style="color:#d1d4dc;">Toplam Portföy:</span>
            <span style="color:#d1d4dc;font-weight:700;">{toplam:,.0f} TL</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:4px;">
            <span style="color:#d1d4dc;">Günlük Değişim:</span>
            <span style="color:{renk};font-weight:600;">{kar_zarar:+,.0f} TL</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:4px;">
            <span style="color:#787b86;">Piyasa:</span>
            <span style="color:#d1d4dc;">BIST {bist:,} | Altın {altin['Gram']:,.0f} | Petrol ${petrol['Fiyat']:,.1f} | VIX {vix['Fiyat']:.1f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    kazanan = max([p for p in st.session_state.portfoy if p['Ad'] != 'NAKİT'], key=lambda x: x.get('Değişim', 0)) if len([p for p in st.session_state.portfoy if p['Ad'] != 'NAKİT']) > 0 else None
    kaybeden = min([p for p in st.session_state.portfoy if p['Ad'] != 'NAKİT'], key=lambda x: x.get('Değişim', 0)) if len([p for p in st.session_state.portfoy if p['Ad'] != 'NAKİT']) > 0 else None
    
    if kazanan and kaybeden:
        st.markdown(f"""
        <div class="tv-panel">
            <div style="display:flex;justify-content:space-between;">
                <span style="color:#22ab94;">🟢 En çok yükselen: {kazanan['Ad']} (%{kazanan.get('Değişim',0):+.1f})</span>
                <span style="color:#f23645;">🔴 En çok düşen: {kaybeden['Ad']} (%{kaybeden.get('Değişim',0):+.1f})</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    hedef_yakin = [p for p in st.session_state.portfoy if p['Ad'] != 'NAKİT' and isinstance(p.get('Hedef'), (int, float)) and p['Güncel'] >= p['Hedef'] * 0.95]
    if hedef_yakin:
        st.markdown("**🎯 Hedefe Yakın Hisseler:**")
        for p in hedef_yakin:
            st.markdown(f"• {p['Ad']}: {p['Güncel']:.2f} TL → Hedef: {p['Hedef']:.2f} TL")
else:
    kalan_dk = 30 - ts.minute if ts.minute <= 30 else 90 - ts.minute
    kalan_saat = 17 - ts.hour if ts.minute <= 30 else 18 - ts.hour
    st.info(f"⏳ Gün sonu raporu saat 18:00'de. Kalan: {kalan_saat}s {kalan_dk}dk")

# ============================================
# DEEPSEEK VERİSİ
# ============================================
st.markdown("---")
st.subheader("🤖 DeepSeek'e Gönder")

ds_metin = f"BIST: {bist:,} | USD: {usd:.2f} | Altın: {altin['Gram']:,.0f} TL/g | Petrol: ${petrol['Fiyat']:,.1f} | VIX: {vix['Fiyat']:.1f} ({vix_seviye})\n"
for p in st.session_state.portfoy:
    if p["Ad"] != "NAKİT":
        ds_metin += f"{p['Ad']}: Lot={p['Lot']:.0f} Alış={p['Alış']:.2f} Güncel={p['Güncel']:.2f} K/Z=%{p.get('K/Z %',0):+.1f} F/K={p.get('F/K','-')} PD/DD={p.get('PD/DD','-')} Günlük=%{p.get('Değişim',0):+.1f} Beta={p.get('Beta','-')} 52H={p.get('52H Dip','-')}-{p.get('52H Zirve','-')} Konum={p.get('Konum','-')} Hedef={p.get('Hedef','-')}\n"
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
