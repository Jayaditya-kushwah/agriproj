/* AgriDoc — Offline-First JavaScript */

'use strict';

// ── Offline Detection ──────────────────────────────────────
function updateOnlineStatus() {
  const banner = document.getElementById('offline-banner');
  const dot = document.getElementById('sync-indicator');
  if (!navigator.onLine) {
    if (banner) banner.style.display = 'flex';
    if (dot) { dot.className = 'sync-dot pending'; dot.title = 'Offline'; }
  } else {
    if (banner) banner.style.display = 'none';
    if (dot) { dot.className = 'sync-dot synced'; dot.title = 'Online'; }
  }
}
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
updateOnlineStatus();

// ── Service Worker Registration ─────────────────────────────
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/js/sw.js')
    .then(reg => console.log('[AgriDoc] SW registered', reg.scope))
    .catch(err => console.warn('[AgriDoc] SW failed', err));
}

// ── Mobile Nav Toggle ──────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks = document.querySelector('.nav-links');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
    navLinks.style.flexDirection = 'column';
    navLinks.style.position = 'absolute';
    navLinks.style.top = '64px';
    navLinks.style.right = '0';
    navLinks.style.background = '#1b4332';
    navLinks.style.padding = '1rem';
    navLinks.style.borderRadius = '0 0 12px 12px';
    navLinks.style.zIndex = '200';
    navLinks.style.minWidth = '200px';
  });
}

// ── Sync Trigger (background) ───────────────────────────────
function attemptSync() {
  if (!navigator.onLine) return;
  fetch('/api/sync', { method: 'POST' })
    .then(r => r.json())
    .then(() => {
      const dot = document.getElementById('sync-indicator');
      if (dot) dot.className = 'sync-dot synced';
    })
    .catch(() => {});
}
window.addEventListener('online', attemptSync);
setTimeout(attemptSync, 3000);

// ── Alert auto-dismiss ──────────────────────────────────────
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity .5s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  }, 5000);
});

// ── Form validation helper ──────────────────────────────────
document.querySelectorAll('form.upload-form').forEach(form => {
  form.addEventListener('submit', function (e) {
    const required = form.querySelectorAll('[required]');
    let ok = true;
    required.forEach(el => {
      if (!el.value.trim()) {
        el.style.borderColor = '#ef4444';
        ok = false;
      } else {
        el.style.borderColor = '';
      }
    });
    if (!ok) {
      e.preventDefault();
      alert('దయచేసి అన్ని అవసరమైన ఫీల్డ్‌లు పూరించండి | Please fill all required fields');
    }
  });
});
