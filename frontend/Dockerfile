# frontend/Dockerfile

# --- 1. AŞAMA: Build Aşaması ---
# React uygulamasını build etmek için Node.js'in 'alpine' (hafif) sürümünü kullan
FROM node:18-alpine AS build

# Konteyner içinde çalışacağımız klasörü ayarla
WORKDIR /app

# Önce 'package.json' ve 'package-lock.json' dosyalarını kopyala
COPY package.json package-lock.json ./

# Sadece bu dosyalar değiştiyse kütüphaneleri yeniden kur (cache'leme için)
RUN npm install

# Geri kalan tüm kodları kopyala
COPY . .

# Uygulamayı 'build' klasörüne derle
RUN npm run build

# --- 2. AŞAMA: Yayın (Serve) Aşaması ---
# Uygulamayı sunmak için çok hafif bir web sunucusu olan Nginx kullan
FROM nginx:1.23-alpine

# 'build' aşamasında oluşturduğumuz statik dosyaları (/app/build) 
# Nginx'in yayın yapacağı varsayılan klasöre (/usr/share/nginx/html) kopyala
COPY --from=build /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Nginx'in 80 portundan yayın yapacağını belirt (varsayılan)
EXPOSE 80

# Nginx'i arka planda değil, ön planda çalıştır (konteynerin ana süreci olması için)
CMD ["nginx", "-g", "daemon off;"]