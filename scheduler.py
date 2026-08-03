import schedule
import time
from data_fetcher import fetch_all_data
from datetime import datetime

def job():
    """Saat başı çalışacak görev"""
    print(f"\n{'='*50}")
    print(f"[{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}] Zamanlanmış görev başladı")
    try:
        fetch_all_data()
        print("✅ Veri çekme başarılı!")
    except Exception as e:
        print(f"❌ Hata: {e}")
    print(f"{'='*50}\n")

# Her saat başı çalıştır
schedule.every().hour.at(":00").do(job)

print("🕐 Zamanlayıcı başlatıldı. Saat başı veri çekilecek.")
print("Çıkmak için Ctrl+C'ye basın.")

# İlk çalıştırmada hemen çek
job()

# Sonsuz döngü
while True:
    schedule.run_pending()
    time.sleep(30)
