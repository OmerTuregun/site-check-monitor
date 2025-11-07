# checker/checker.py

import time
import requests
import os
import psycopg2 # Veritabanı bağlantısı için eklendi
from datetime import datetime # Zaman damgası için

def get_db_connection():
    """Veritabanı bağlantısını kurar ve döner."""
    
    # docker-compose.yml'de tanımladığımız ortam değişkenlerini çek
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASSWORD')
    
    conn = None
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_pass
            )
            print("Checker: Veritabanı bağlantısı başarılı!")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Checker: Veritabanına bağlanılamadı: {e}")
            retries -= 1
            print(f"Checker: Tekrar denemek için 5 saniye bekleniyor... ({retries} deneme kaldı)")
            time.sleep(5)
            
    if conn is None:
        print("Checker: Veritabanına bağlanılamadı. Servis durduruluyor.")
        raise Exception("Veritabanı bağlantısı kurulamadı.")


def check_site(url):
    """Belirtilen URL'ye bir HTTP GET isteği atar ve durumunu döndürür."""
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code < 400:
            print(f"[OK] {url} AYAKTA. Durum Kodu: {response.status_code}")
            return "UP"
        else:
            print(f"[HATA] {url} ÇÖKTÜ. Durum Kodu: {response.status_code}")
            return "DOWN"
            
    except requests.exceptions.Timeout:
        print(f"[HATA] {url} ZAMAN AŞIMI.")
        return "DOWN"
    except requests.exceptions.RequestException:
        # DNS hatası, bağlantı reddedildi vb.
        print(f"[HATA] {url} BAĞLANTI HATASI.")
        return "DOWN"

def main_loop():
    """Ana döngü. Artık sahte liste yerine VERİTABANINDAN siteleri çeker."""
    print("Checker servisi başladı. Veritabanından siteler çekiliyor...")
    
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # 1. Veritabanından siteleri ÇEK (SELECT)
            cur.execute("SELECT id, url FROM sites;")
            siteler_listesi = cur.fetchall() # (id, url) çiftlerini al
            
            print(f"\n--- Yeni Kontrol Döngüsü: {len(siteler_listesi)} site kontrol edilecek ---")

            for site in siteler_listesi:
                site_id, site_url = site[0], site[1]
                
                # 2. Siteyi KONTROL ET
                status = check_site(site_url)
                
                # 3. Sonucu veritabanına YAZ (UPDATE)
                cur.execute(
                    "UPDATE sites SET status = %s, last_checked = %s WHERE id = %s",
                    (status, datetime.now(), site_id)
                )
            
            # Tüm 'UPDATE' işlemlerini onayla
            conn.commit()
            
            cur.close()
            print(f"--- Döngü tamamlandı. 60 saniye bekleniyor... ---")

        except (Exception, psycopg2.Error) as error:
            print(f"Checker döngüsünde hata: {error}")
        finally:
            # Bağlantıyı her döngü sonunda kapat (iyi bir pratiktir)
            if conn:
                conn.close()
                
        time.sleep(60) # 60 saniye bekle

if __name__ == "__main__":
    main_loop()