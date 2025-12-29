const CACHE_NAME = 'klangkiste-v66-stable'; // WICHTIG: Version hochgezählt für das finale Update
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './assets/limit.mp3',
  './assets/img/hintergrund.jpg',
  './assets/icons/icon.png',
  './assets/icons/icon512_maskable.png',
  './assets/icons/icon512_rounded.png'
];

// 1. Installieren: Dateien in den Cache laden
self.addEventListener('install', (e) => {
  console.log('[Service Worker] Installiere & Cache Dateien...');
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  // Zwingt den wartenden Service Worker sofort aktiv zu werden
  self.skipWaiting(); 
});

// 2. Abrufen (Fetch): Erst Cache, dann Netzwerk
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      // Wenn im Cache, nimm das. Sonst lade aus dem Netz.
      return cachedResponse || fetch(e.request);
    })
  );
});

// 3. Aktivieren: Alte Caches löschen (Aufräumen beim Update)
self.addEventListener('activate', (e) => {
  console.log('[Service Worker] Aktiviere Version:', CACHE_NAME);
  e.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        // Lösche alle Caches, die nicht der aktuellen Version entsprechen
        if (key !== CACHE_NAME) {
          console.log('[Service Worker] Entferne alten Cache:', key);
          return caches.delete(key);
        }
      }));
    })
  );
  // Übernimmt sofort die Kontrolle über alle offenen Tabs
  return self.clients.claim();
});
