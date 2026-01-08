document.addEventListener('DOMContentLoaded', function () {
  const path = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav-link').forEach(a => {
    const href = a.getAttribute('href');
    if (!href) return;
    try {
      const url = new URL(href, location.origin);
      const linkPath = url.pathname.replace(/\/$/, '') || '/';
      if (linkPath === path || (linkPath !== '/' && path.startsWith(linkPath))) {
        a.classList.add('active');
        a.setAttribute('aria-current', 'page');
      }
    } catch (e) {
      // ignore malformed hrefs (anchors, external links)
      if (href === location.hash) {
        a.classList.add('active');
      }
    }
  });
});
