self.addEventListener('install', e => {
  e.waitUntil(caches.open('v1').then(cache => cache.addAll(['/', '/static/manifest.json'])));
});
self.addEventListener('fetch', e => {
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});\n