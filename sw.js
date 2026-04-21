// PM OS Service Worker - 离线缓存支持
const CACHE_NAME = 'pmos-cache-v1';
const CACHE_ASSETS = [
  './',
  './index.html',
  './vue3.min.js',
  './lucide.min.js',
  './marked.min.js',
  './xlsx.full.min.js',
  './manifest.json'
];

// 安装事件 - 缓存核心资源
self.addEventListener('install', event => {
  console.log('[SW] 安装Service Worker');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] 缓存核心资源');
        return cache.addAll(CACHE_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', event => {
  console.log('[SW] 激活Service Worker');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// 请求拦截 - 缓存优先策略
self.addEventListener('fetch', event => {
  // 只处理GET请求
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    caches.match(event.request)
      .then(cached => {
        // 缓存命中则返回缓存
        if (cached) {
          console.log('[SW] 缓存命中:', event.request.url);
          return cached;
        }
        
        // 否则从网络获取
        console.log('[SW] 网络请求:', event.request.url);
        return fetch(event.request)
          .then(response => {
            // 只缓存成功的响应
            if (!response || response.status !== 200) {
              return response;
            }
            
            // 克隆响应并缓存
            const responseClone = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => cache.put(event.request, responseClone));
            
            return response;
          })
          .catch(err => {
            console.log('[SW] 网络请求失败:', err);
            // 离线时返回缓存首页
            if (event.request.mode === 'navigate') {
              return caches.match('./index.html');
            }
            return new Response('离线状态', { status: 503 });
          });
      })
  );
});

// 后台同步（可选）
self.addEventListener('sync', event => {
  console.log('[SW] 后台同步:', event.tag);
});

// 推送通知（可选）
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'PM OS有新消息',
    icon: './icon-192.png',
    badge: './icon-192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now()
    }
  };
  
  event.waitUntil(
    self.registration.showNotification('PM OS', options)
  );
});

console.log('[SW] Service Worker 已加载');
