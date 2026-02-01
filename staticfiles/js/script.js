document.addEventListener('DOMContentLoaded', function () {
  const path = window.location.pathname.replace(/\/$/, '') || '/';
  // Gather links once
  const links = Array.from(document.querySelectorAll('.nav-link'));

  // First pass: prefer an exact-match link if present (most specific)
  for (const a of links) {
    const href = a.getAttribute('href');
    if (!href) continue;
    try {
      const url = new URL(href, location.origin);
      const linkPath = url.pathname.replace(/\/$/, '') || '/';
      if (linkPath === path) {
        a.classList.add('active');
        a.setAttribute('aria-current', 'page');
        return; // stop — exact match found, don't mark parents
      }
    } catch (e) {
      if (href === location.hash) {
        a.classList.add('active');
        return;
      }
    }
  }

  // Second pass: fall back to parent-aware matches
  for (const a of links) {
    const href = a.getAttribute('href');
    if (!href) continue;
    try {
      const url = new URL(href, location.origin);
      const linkPath = url.pathname.replace(/\/$/, '') || '/';
      const activeForChildren = a.dataset.activeForChildren === 'true';
      if (linkPath === path || (activeForChildren && linkPath !== '/' && path.startsWith(linkPath + '/'))) {
        a.classList.add('active');
        a.setAttribute('aria-current', 'page');
      }
    } catch (e) {
      if (href === location.hash) {
        a.classList.add('active');
      }
    }
  }
});
