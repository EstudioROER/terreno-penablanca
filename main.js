/* ============================================================
   MAIN.JS – Landing Page Parde Arquitectos
   ============================================================ */

// ── Navbar scroll effect ──────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

// ── Hamburger menu ────────────────────────────────────────────
const hamburgerBtn = document.getElementById('hamburgerBtn');
const navLinks = document.querySelector('.nav-links');

if (hamburgerBtn && navLinks) {
  hamburgerBtn.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    hamburgerBtn.setAttribute('aria-expanded', isOpen);
  });
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

// ── Smooth scroll ─────────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const href = anchor.getAttribute('href');
    if (href.startsWith('#') && href.length > 1) {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 80, behavior: 'smooth' });
      }
    }
  });
});

// ── Intersection Observer fade-in ─────────────────────────────
const fadeObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      fadeObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

['.feature-card', '.doc-card', '.acc-item', '.proj-stat', '.section-header',
 '.price-inner', '.aerial-frame', '.map-wrapper', '.project-card',
 '.contacto-left', '.contact-form', '.footer-top'
].forEach(selector => {
  document.querySelectorAll(selector).forEach((el, i) => {
    el.classList.add('fade-in');
    el.style.transitionDelay = `${i * 0.06}s`;
    fadeObserver.observe(el);
  });
});

// ── CLP Counter animation ──────────────────────────────────────
function animateCounter(el, target, duration = 1600) {
  const startTime = performance.now();
  function update(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 4);
    el.textContent = '$' + Math.floor(eased * target).toLocaleString('es-CL') + ' CLP';
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = '$' + target.toLocaleString('es-CL') + ' CLP';
  }
  requestAnimationFrame(update);
}
const priceUfEl = document.querySelector('.price-uf');
if (priceUfEl) {
  new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) { animateCounter(priceUfEl, 800000000); entries[0].target._obs?.disconnect(); }
  }, { threshold: 0.5 }).observe(priceUfEl);
}

console.log('🏛 Parde Arquitectos – Terreno Peñablanca listing loaded.');
