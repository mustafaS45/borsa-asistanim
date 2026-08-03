import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import os

# Sayfa yapılandırması
st.set_page_config(
    page_title="Borsa Asistanım",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS ile mobil uyumlu tasarım
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #2a5298;
        margin: 5px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background: #2a5298;
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.5rem; }
        .metric-card { padding: 10px; }
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("""
<div class="main-header">
    <h1>📊 Borsa Asistanım</h1>
    <p>Canlı Portföy Takip ve Piyasa Verileri | 40.000 TL Portföy</p>
</div>
""", unsafe_allow_html=True)

# Yenileme butonu
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🔄 Verileri Güncelle", use_container_width=True):
        from data_fetcher import fetch_all_data
        with st.spinner("Veriler çekiliyor..."):
            fetch_all_data()
        st.success("✅ Güncellendi!")
        st.rerun()

# Verileri yükle
@st.cache_data(ttl=3600)
def load_data():
    try:
        if os.path.exists('piyasa_verileri.csv'):
            df = pd.read_csv('piyasa_verileri.csv')
            return df.iloc[-1].to_dict()
    except:
        pass
    return None

veri = load_data()

if veri is None or 'bist100' not in veri or veri.get('bist100') is None:
    st.warning("⏳ İlk veri çekiliyor, lütfen bekleyin...")
    from data_fetcher import fetch_all_data
    veri = fetch_all_data()
    st.rerun()

son_guncelleme = veri.get('son_guncelleme', 'Bilinmiyor')
st.markdown(f"🕐 **Son Güncelleme:** {son_guncelleme} | ⏱️ Her saat otomatik güncellenir")
st.markdown("---")

# === PİYASA ÖZETİ ===
st.subheader("📈 Temel Piyasa Verileri")

col1, col2, col3, col4 = st.columns(4)

with col1:
    bist = veri.get('bist100', 0)
    st.markdown(f"""
    <div class="metric-card">
        <small>BIST 100</small><br>
        <h3>{bist:,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    usd = veri.get('usd_try', 0)
    st.markdown(f"""
    <div class="metric-card">
        <small>USD/TRY</small><br>
        <h3>{usd:.2f} ₺</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    eur = veri.get('eur_try', 0) or 0
    st.markdown(f"""
    <div class="metric-card">
        <small>EUR/TRY</small><br>
        <h3>{eur:.2f} ₺</h3>
    </div>
    """, unsafe_allow_html=True)

with col4:
    altin = veri.get('gram_altin', 0) or 0
    st.markdown(f"""
    <div class="metric-card">
        <small>Gram Altın</small><br>
        <h3>{altin:,.0f} ₺</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# === PORTFÖY ÖZETİ ===
st.subheader("💼 Portföy Özeti (Başlangıç: 40.000 TL)")

from portfoy_takip import portfoy_hesapla

portfoy_list, toplam_deger, toplam_maliyet = portfoy_hesapla(veri)
portfoy_df = pd.DataFrame(portfoy_list)

# Büyük rakamlar
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Toplam Portföy Değeri", f"{toplam_deger:,.0f} TL")

with col2:
    kar_zarar = toplam_deger - toplam_maliyet
    st.metric("Toplam Kâr/Zarar", f"{kar_zarar:,.0f} TL")

with col3:
    getiri_orani = ((toplam_deger - toplam_maliyet) / toplam_maliyet) * 100
    st.metric("Getiri Oranı", f"%{getiri_orani:.2f}")

# Grafikler
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Varlık Dağılımı")
    fig = px.pie(portfoy_df, values='Güncel Değer (TL)', names='Varlık',
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400, margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Kâr/Zarar Durumu")
    fig = px.bar(portfoy_df, x='Varlık', y='Kâr/Zarar (TL)',
                 color='Kâr/Zarar (TL)',
                 color_continuous_scale=['red', 'lightgray', 'green'])
    fig.update_layout(height=400, margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

# Detaylı tablo
st.subheader("📋 Portföy Detayları")
st.dataframe(
    portfoy_df.style.format({
        'Alış Fiyatı': '{:.2f}',
        'Güncel Fiyat': '{:.2f}',
        'Maliyet (TL)': '{:,.2f}',
        'Güncel Değer (TL)': '{:,.2f}',
        'Kâr/Zarar (TL)': '{:,.2f}',
        'Kâr/Zarar (%)': '{:.2f}',
        'Ağırlık (%)': '{:.1f}'
    }),
    use_container_width=True,
    hide_index=True
)

# === HİSSE SENETLERİ ===
st.markdown("---")
st.subheader("📈 Seçili Hisse Senetleri")

hisse_listesi = ['ASELSAN', 'AKBNK', 'YKBNK', 'THYAO', 'TOASO', 'FROTO', 'SAHOL', 'TCELL']
hisse_map = {
    'ASELSAN': 'aselsan', 'AKBNK': 'akbnk', 'YKBNK': 'ykbnk',
    'THYAO': 'thy', 'TOASO': 'toaso', 'FROTO': 'froto',
    'SAHOL': 'sahol', 'TCELL': 'tcell'
}

cols = st.columns(4)
for i, hisse in enumerate(hisse_listesi):
    fiyat = veri.get(hisse_map[hisse])
    with cols[i % 4]:
        if fiyat:
            st.metric(hisse, f"{fiyat:.2f} TL")
        else:
            st.metric(hisse, "Veri yok")

# === UYARILAR ===
st.markdown("---")
st.subheader("⚠️ Risk Uyarıları")

uyarilar = []
for item in portfoy_list:
    if item['Varlık'] not in ['PPF', 'Altın Fonu']:
        kz_yuzde = item['Kâr/Zarar (%)']
        if kz_yuzde < -7:
            uyarilar.append(f"🔴 **{item['Varlık']}** stop-loss seviyesinde (%{kz_yuzde:.1f}). Satış yapmayı değerlendirin!")
        elif kz_yuzde < -5:
            uyarilar.append(f"🟡 **{item['Varlık']}** %{kz_yuzde:.1f} zararda. Yakından takip edin.")
        elif kz_yuzde > 15:
            uyarilar.append(f"🟢 **{item['Varlık']}** %{kz_yuzde:.1f} kârda. Kâr realizasyonu düşünebilirsiniz.")

if not uyarilar:
    uyarilar.append("✅ Şu an kritik bir uyarı yok. Portföyünüz hedef aralıklarda.")

for uyari in uyarilar:
    st.markdown(uyari)

# Alt bilgi
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>⚠️ Bu uygulama yatırım tavsiyesi vermez. Tüm yatırım kararları size aittir.</p>
    <p>Veri Kaynağı: Yahoo Finance | Otomatik Güncelleme: Her saat başı</p>
</div>
""", unsafe_allow_html=True)
