// frontend/src/App.js

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [sites, setSites] = useState([]); // Siteleri tutacağımız state
  const [loading, setLoading] = useState(true); // Yüklenme durumu

  useEffect(() => {
    // Bileşen ilk yüklendiğinde veriyi çek
    fetch('/api/sites') // API endpoint'imize istek at
      .then(response => response.json())
      .then(data => {
        setSites(data); // Gelen veriyi state'e ata
        setLoading(false); // Yüklemeyi bitir
      })
      .catch(error => {
        console.error("API'den veri çekerken hata oluştu:", error);
        setLoading(false);
      });
  }, []); // [] -> Bu effect'in sadece bir kez çalışmasını sağlar

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 Site-Check Uptime Monitor</h1>
        
        <h2>İzlenen Siteler</h2>
        {loading ? (
          <p>Veriler yükleniyor...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Site URL</th>
                <th>Durum</th>
              </tr>
            </thead>
            <tbody>
              {sites.map(site => (
                <tr key={site.id}>
                  <td>{site.url}</td>
                  <td style={{ color: site.status === 'UP' ? 'green' : 'red' }}>
                    {site.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </header>
    </div>
  );
}

export default App;