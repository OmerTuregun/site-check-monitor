# api/app.py

from flask import Flask, jsonify

app = Flask(__name__)

# Örnek (sahte) site verisi
# Gerçek veritabanı bağlandığında bu değişecek
DUMMY_SITES = [
    {"id": 1, "url": "https://google.com", "status": "UP"},
    {"id": 2, "url": "https://bing.com", "status": "UP"},
    {"id": 3, "url": "https://bu-site-yok.com", "status": "DOWN"},
]

@app.route('/api/health')
def health_check():
    """Kubernetes gibi sistemlerin servisin ayakta olup olmadığını 
       kontrol etmesi için basit bir 'health check' endpoint'i."""
    return jsonify({"durum": "calisiyor"}), 200

@app.route('/api/sites')
def get_sites():
    """Tüm siteleri listeleyen ana endpoint'imiz."""
    # Şimdilik sahte veriyi dönüyoruz
    return jsonify(DUMMY_SITES), 200

if __name__ == '__main__':
    # 'host=0.0.0.0' ayarı, konteynerin dışarıdan gelen isteklere 
    # cevap verebilmesi için KRİTİKTİR.
    app.run(host='0.0.0.0', port=5000, debug=True)