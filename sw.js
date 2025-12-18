// sw.js - Ein minimaler Service Worker für PWA-Installation
self.addEventListener('install', (e) => {
  console.log('[Service Worker] Install');
});

self.addEventListener('fetch', (e) => {
  // Einfach alles durchleiten, wir brauchen kein Offline-Caching für diesen Zweck
  e.respondWith(fetch(e.request));
});