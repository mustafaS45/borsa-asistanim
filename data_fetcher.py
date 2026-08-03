import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def fetch_all_data():
    """Tüm piyasa verilerini çeker ve CSV'ye kaydeder"""
    
    veriler = {}
    hatalar = []
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Veri çekme başladı...")
    
    # BIST 100
    try:
        bist = yf.Ticker("XU100.IS")
        veriler['bist100'] = round(float(bist.history(period="1d")['Close'].iloc[-1]), 0)
        print(f"✓ BIST 100: {veriler['bist100']}")
    except Exception as e:
        hatalar.append(f"BIST 100: {str(e)[:50]}")
        veriler['bist100'] = None
    
    # USD/TRY
    try:
        usd = yf.Ticker("USDTRY=X")
        veriler['usd_try'] = round(float(usd.history(period="1d")['Close'].iloc[-1]), 2)
        print(f"✓ USD/TRY: {veriler['usd_try']}")
    except Exception as e:
        hatalar.append(f"USD/TRY: {str(e)[:50]}")
        veriler['usd_try'] = None
    
    # EUR/TRY
    try:
        eur = yf.Ticker("EURTRY=X")
        veriler['eur_try'] = round(float(eur.history(period="1d")['Close'].iloc[-1]), 2)
        print(f"✓ EUR/TRY: {veriler['eur_try']}")
    except:
        veriler['eur_try'] = None
    
    # Altın
    try:
        ons = yf.Ticker("GC=F")
        ons_fiyat = float(ons.history(period="1d")['Close'].iloc[-1])
        veriler['ons_altin'] = round(ons_fiyat, 0)
        if veriler['usd_try']:
            veriler['gram_altin'] = round((ons_fiyat * veriler['usd_try']) / 31.1, 0)
        else:
            veriler['gram_altin'] = None
        print(f"✓ Ons Altın: ${veriler['ons_altin']}, Gram: {veriler['gram_altin']} TL")
    except Exception as e:
        hatalar.append(f"Altın: {str(e)[:50]}")
        veriler['gram_altin'] = None
        veriler['ons_altin'] = None
    
    # Hisseler
    hisseler = {
        'aselsan': 'ASELS.IS',
        'akbnk': 'AKBNK.IS',
        'thy': 'THYAO.IS',
        'toaso': 'TOASO.IS',
        'froto': 'FROTO.IS',
        'ykbnk': 'YKBNK.IS',
        'sahol': 'SAHOL.IS',
        'tcell': 'TCELL.IS'
    }
    
    for isim, sembol in hisseler.items():
        try:
            hisse = yf.Ticker(sembol)
            veriler[isim] = round(float(hisse.history(period="1d")['Close'].iloc[-1]), 2)
            print(f"✓ {isim.upper()}: {veriler[isim]}")
        except Exception as e:
            hatalar.append(f"{isim}: {str(e)[:50]}")
            veriler[isim] = None
    
    veriler['son_guncelleme'] = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    veriler['hatalar'] = ','.join(hatalar) if hatalar else ''
    
    # CSV'ye kaydet
    df = pd.DataFrame([veriler])
    df.to_csv('piyasa_verileri.csv', index=False)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Tamamlandı. Hata: {len(hatalar)}")
    return veriler

if __name__ == "__main__":
    fetch_all_data()
