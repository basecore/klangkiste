// WICHTIG: Version erhöht auf v80, damit das Handy alles neu lädt!
const CACHE_NAME = 'klangkiste-v80-full';

// Da du bestätigt hast, dass diese Dateien existieren, 
// können wir sie sicher hier auflisten.
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

// --- 1. INSTALLIEREN (Dateien in den Speicher laden) ---
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installiere Version:', CACHE_NAME);
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching aller Dateien...');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .catch((err) => {
        console.error('[Service Worker] Fehler beim Cachen:', err);
        // Falls hier ein Fehler auftaucht, stimmt ein Pfad nicht!
      })
  );
  // Zwingt den neuen SW sofort aktiv zu werden
  self.skipWaiting();
});

// --- 2. AKTIVIEREN (Alte Caches löschen) ---
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Aktiviere...');
  
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        // Lösche alles, was nicht v80 ist
        if (key !== CACHE_NAME) {
          console.log('[Service Worker] Lösche alten Cache:', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});

// --- 3. FETCH (Offline Support) ---
self.addEventListener('fetch', (event) => {
  // Nur GET Requests cachen
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // A) Datei ist im Cache? Nimm sie! (Offline Modus)
      if (cachedResponse) {
        return cachedResponse;
      }

      // B) Nicht im Cache? Hol sie aus dem Internet.
      return fetch(event.request)
        .then((networkResponse) => {
          return networkResponse;
        })
        .catch(() => {
          // C) Offline und Datei fehlt?
          console.log("Offline und Datei nicht gefunden:", event.request.url);
        });
    })
  );
});
