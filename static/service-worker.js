self.addEventListener('install', function(event) {
    self.skipWaiting();
});

self.addEventListener('activate', function(event) {
    event.waitUntil(clients.claim());
});

self.addEventListener('push', function(event) {
    const data = event.data ? event.data.json() : {};

    const titre = data.title || "Halé Bou Rér";
    const options = {
        body: data.body || "Nouveau signalement disponible",
        icon: "/static/images/logo.png"
    };

    event.waitUntil(
        self.registration.showNotification(titre, options)
    );
});
