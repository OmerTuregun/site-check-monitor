# api/Dockerfile

# 1. Temel imaj olarak hafif bir Python 3.10 sürümü kullan
FROM python:3.10-slim

# 2. Konteyner içinde çalışacağımız klasörü ayarla
WORKDIR /app

# 3. Önce sadece 'requirements.txt' dosyasını kopyala
#    (Bu sayede kütüphaneler değişmediği sürece Docker bu adımı 
#    cache'ler ve her build'de kütüphaneleri tekrar indirmez)
COPY requirements.txt .

# 4. Kütüphaneleri kur
RUN pip install --no-cache-dir -r requirements.txt

# 5. Geri kalan tüm uygulama kodunu (app.py vb.) kopyala
COPY . .

# 6. Flask uygulamasının 5000 portunda çalışacağını belirt
EXPOSE 5000

# 7. Konteyner çalıştığında hangi komutun çalışacağını belirt
CMD ["python", "app.py"]