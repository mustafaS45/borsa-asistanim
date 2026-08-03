def portfoy_hesapla(piyasa_verileri):
    """Güncel fiyatlarla portföy değerini hesaplar"""
    
    portfoy = {
        'PPF': {'miktar': 12000, 'alis_fiyat': 1, 'tip': 'nakit'},
        'Altın Fonu': {'miktar': 6000, 'alis_fiyat': 1, 'tip': 'altin', 'alis_gram': 6170},
        'AKBNK': {'miktar': 121, 'alis_fiyat': 66.00, 'tip': 'hisse'},
        'ASELSAN': {'miktar': 18, 'alis_fiyat': 336.25, 'tip': 'hisse'},
        'YKBNK': {'miktar': 118, 'alis_fiyat': 34.00, 'tip': 'hisse'},
        'THYAO': {'miktar': 13, 'alis_fiyat': 317.00, 'tip': 'hisse'}
    }
    
    fiyat_map = {
        'AKBNK': piyasa_verileri.get('akbnk'),
        'ASELSAN': piyasa_verileri.get('aselsan'),
        'YKBNK': piyasa_verileri.get('ykbnk'),
        'THYAO': piyasa_verileri.get('thy')
    }
    
    sonuc = []
    toplam_deger = 0
    toplam_maliyet = 40000
    
    for varlik, detay in portfoy.items():
        if detay['tip'] == 'nakit':
            guncel_deger = detay['miktar']
            alis_fiyat = 1
            guncel_fiyat = 1
        elif detay['tip'] == 'altin':
            gram_altin = piyasa_verileri.get('gram_altin', 6170)
            if gram_altin is None:
                gram_altin = 6170
            alis_fiyat = detay['alis_gram']
            guncel_fiyat = gram_altin
            guncel_deger = detay['miktar'] * (gram_altin / alis_fiyat)
        else:
            guncel_fiyat = fiyat_map.get(varlik)
            alis_fiyat = detay['alis_fiyat']
            if guncel_fiyat:
                guncel_deger = detay['miktar'] * guncel_fiyat
            else:
                guncel_deger = detay['miktar'] * alis_fiyat
        
        maliyet = detay['miktar'] * alis_fiyat if detay['tip'] == 'hisse' else detay['miktar']
        if detay['tip'] == 'altin':
            maliyet = detay['miktar']
        
        kar_zarar = guncel_deger - maliyet
        kar_zarar_yuzde = (kar_zarar / maliyet) * 100 if maliyet > 0 else 0
        
        sonuc.append({
            'Varlık': varlik,
            'Miktar': detay['miktar'],
            'Alış Fiyatı': round(alis_fiyat, 2),
            'Güncel Fiyat': round(guncel_fiyat, 2) if guncel_fiyat else None,
            'Maliyet (TL)': round(maliyet, 2),
            'Güncel Değer (TL)': round(guncel_deger, 2),
            'Kâr/Zarar (TL)': round(kar_zarar, 2),
            'Kâr/Zarar (%)': round(kar_zarar_yuzde, 2),
            'Ağırlık (%)': 0
        })
        
        toplam_deger += guncel_deger
    
    for item in sonuc:
        item['Ağırlık (%)'] = round((item['Güncel Değer (TL)'] / toplam_deger) * 100, 1) if toplam_deger > 0 else 0
    
    return sonuc, round(toplam_deger, 2), toplam_maliyet
