/* オフライン対応のサービスワーカー（ネットワーク優先で常に最新を取得） */
const CACHE = "parfait-curling-v14";
const ASSETS = [
  "./", "./index.html", "./manifest.json", "./title-bg.jpg", "./assets/bgm.mp3", "./assets/bgm_title.mp3",
  "./icon-192.png", "./icon-512.png", "./icon-180.png",
  "https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js",
];
for (let i = 0; i <= 10; i++) ASSETS.push("./assets/item" + i + ".png");

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
// ネットワーク優先：オンライン時は常に最新を取得しキャッシュ更新、失敗時のみキャッシュ
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  // Firestore等のAPIはSWを通さずネットワーク直通（ランキング通信に干渉しない）
  if (/googleapis\.com|firebaseio\.com|firestore|googlesyndication\.com|doubleclick\.net|adservice\.google/.test(e.request.url)) return;
  e.respondWith(
    fetch(e.request).then((res) => {
      const copy = res.clone();
      caches.open(CACHE).then((c) => c.put(e.request, copy)).catch(() => {});
      return res;
    }).catch(() => caches.match(e.request))
  );
});
