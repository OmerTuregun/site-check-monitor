# checker/Dockerfile

# 1. Temel imaj olarak hafif bir Python 3.10 sürümü kullan
FROM python:3.10-slim

# 2. Konteyner içinde çalışacağımız klasörü ayarla
WORKDIR /app

# 3. Önce sadece 'requirements.txt' dosyasını kopyala (Cache'leme için)
COPY requirements.txt .

# 4. Kütüphaneleri kur
RUN pip install --no-cache-dir -r requirements.txt

# 5. Geri kalan tüm uygulama kodunu (checker.py vb.) kopyala
COPY . .

# 7. Konteyner çalıştığında hangi komutun çalışacağını belirt
#    (app.py'den farklı olarak bu bir sunucu değil, bir script)
CMD ["python", "checker.py"]