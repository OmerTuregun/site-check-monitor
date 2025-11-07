# checker/checker.py

import time
import requests
import os

# Şimdilik kontrol edilecek siteleri manuel olarak burada tanımlıyoruz.
# Docker-compose'a geçince bunu API'den veya DB'den alacağız.
SITELER_LISTESI = [
    "https://google.com",
    "https://github.com",
    "https://facebook.com",
    "https://asdfghjkl-bu-site-yok.com" # Hata alması gereken bir site
]

def check_site(url):
    """Belirtilen URL'ye bir HTTP GET isteği atar ve durumunu döndürür."""
    try:
        # 5 saniye içinde cevap gelmezse 'timeout' olarak kabul et
        response = requests.get(url, timeout=5)
        
        # 2xx (200, 201..) veya 3xx (301, 302..) HTTP kodları 'UP' (AYAKTA) demektir
        if response.status_code < 400:
            print(f"[OK] {url} AYAKTA. Durum Kodu: {response.status_code}")
            return "UP"
        else:
            # 4xx (404 Not Found) veya 5xx (500 Server Error) 'DOWN' (ÇÖKTÜ) demektir
            print(f"[HATA] {url} ÇÖKTÜ. Durum Kodu: {response.status_code}")
            return "DOWN"
            
    except requests.exceptions.Timeout:
        # 5 saniyede cevap gelmedi
        print(f"[HATA] {url} ZAMAN AŞIMI.")
        return "DOWN"
    except requests.exceptions.RequestException as e:
        # DNS hatası, bağlantı reddedildi vb.
        print(f"[HATA] {url} BAĞLANTI HATASI: {e}")
        return "DOWN"

def main_loop():
    """Ana döngü. Her 60 saniyede bir tüm siteleri kontrol eder."""
    print("Checker servisi başladı. Kontrol döngüsü başlıyor...")
    while True:
        print("\n--- Yeni Kontrol Döngüsü ---")
        for url in SITELER_LISTESI:
            check_site(url)
        
        print(f"--- Döngü tamamlandı. 60 saniye bekleniyor... ---")
        time.sleep(60) # 60 saniye bekle

if __name__ == "__main__":
    main_loop()