# api/app.py

from flask import Flask, jsonify
import psycopg2 # Veritabanı bağlantısı için ekledik
import os # Ortam değişkenlerini okumak için ekledik
import time # DB bağlantısını beklemek için

app = Flask(__name__)

def get_db_connection():
    """Veritabanı bağlantısını kurar ve döner."""
    
    # docker-compose.yml'de tanımladığımız ortam değişkenlerini çek
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASSWORD')
    
    # Veritabanı (db servisi) ayağa kalkana kadar bekleyebiliriz
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_pass
            )
            print("Veritabanı bağlantısı başarılı!")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Veritabanına bağlanılamadı: {e}")
            retries -= 1
            print(f"Tekrar denemek için 5 saniye bekleniyor... ({retries} deneme kaldı)")
            time.sleep(5)
            
    print("Veritabanına bağlanılamadı. Servis durduruluyor.")
    # Bağlantı kurulamazsa uygulamayı sonlandır
    raise Exception("Veritabanı bağlantısı kurulamadı.")


def init_db():
    """Veritabanında 'sites' tablosunun var olup olmadığını kontrol eder,
       yoksa oluşturur ve içine örnek veri ekler."""
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 'sites' tablosu var mı diye kontrol et
    cur.execute("SELECT to_regclass('public.sites');")
    table_exists = cur.fetchone()[0]
    
    if not table_exists:
        print("'sites' tablosu bulunamadı. Oluşturuluyor...")
        # Tabloyu oluştur
        cur.execute("""
            CREATE TABLE sites (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                status VARCHAR(10) DEFAULT 'PENDING',
                last_checked TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # İçine 'DUMMY_SITES' yerine 'gerçek' örnek verileri ekle
        # Checker bu verileri alıp 'status' alanını güncelleyecek
        sample_data = [
            ("https://google.com", "PENDING"),
            ("https://bing.com", "PENDING"),
            ("https://bu-site-yok-tur.com", "PENDING")
        ]
        cur.executemany("INSERT INTO sites (url, status) VALUES (%s, %s)", sample_data)
        
        conn.commit() # Değişiklikleri kaydet
        print("Tablo oluşturuldu ve örnek veriler eklendi.")
    else:
        print("'sites' tablosu zaten mevcut.")
        
    cur.close()
    conn.close()


@app.route('/api/health')
def health_check():
    """Sağlık kontrolü endpoint'i."""
    return jsonify({"durum": "calisiyor"}), 200

@app.route('/api/sites')
def get_sites():
    """Artık sahte veri değil, VERİTABANINDAN gelen gerçek veriyi döner."""
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Veritabanından tüm siteleri çek
    cur.execute("SELECT id, url, status, last_checked FROM sites ORDER BY id ASC;")
    # Veriyi fetchone() ile değil, fetchall() ile al
    sites_data = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Veritabanından gelen (id, url, status, last_checked) formatındaki
    # veriyi JSON'a uygun bir liste/dictionary formatına çevir
    sites_list = []
    for row in sites_data:
        sites_list.append({
            "id": row[0],
            "url": row[1],
            "status": row[2],
            "last_checked": row[3]
        })
        
    return jsonify(sites_list), 200

if __name__ == '__main__':
    # Uygulama başlamadan önce veritabanını kontrol et/oluştur
    init_db()
    
    app.run(host='0.0.0.0', port=5000, debug=True)