/* ============================================================
   MAIN.JS – Landing Page Parde Arquitectos
   Formulario integrado con Formspree (AJAX/fetch)
   ============================================================ */

// ── CONFIGURACIÓN ─────────────────────────────────────────────
// Reemplaza este ID con el que obtengas en formspree.io
// Formato: https://formspree.io/f/XXXXXXXX
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/XXXXXXXX';

// ── Navbar scroll effect ──────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

// ── Hamburger menu ────────────────────────────────────────────
const hamburgerBtn = document.getElementById('hamburgerBtn');
const navLinks = document.querySelector('.nav-links');

hamburgerBtn.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  hamburgerBtn.setAttribute('aria-expanded', isOpen);
});
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

// ── Smooth scroll ─────────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 80, behavior: 'smooth' });
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

// ── UF Counter animation ──────────────────────────────────────
function animateCounter(el, target, duration = 1600) {
  const startTime = performance.now();
  function update(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 4);
    el.textContent = 'UF ' + Math.floor(eased * target).toLocaleString('es-CL');
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = 'UF ' + target.toLocaleString('es-CL');
  }
  requestAnimationFrame(update);
}
const priceUfEl = document.querySelector('.price-uf');
if (priceUfEl) {
  new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) { animateCounter(priceUfEl, 48098); entries[0].target._obs?.disconnect(); }
  }, { threshold: 0.5 }).observe(priceUfEl);
}

// ── Shake keyframe ────────────────────────────────────────────
const style = document.createElement('style');
style.textContent = `
  @keyframes shake { 0%,100%{transform:translateX(0)} 20%{transform:translateX(-8px)} 40%{transform:translateX(8px)} 60%{transform:translateX(-6px)} 80%{transform:translateX(6px)} }
  .sending-spinner { display:inline-block; animation:spin 0.8s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
`;
document.head.appendChild(style);

// ── Formulario Formspree (AJAX) ───────────────────────────────
const form     = document.getElementById('contactoForm');
const success  = document.getElementById('formSuccess');
const btnEnviar = document.getElementById('btnEnviar');

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validación local
    const nombre  = document.getElementById('nombre').value.trim();
    const email   = document.getElementById('email').value.trim();
    const mensaje = document.getElementById('mensaje').value.trim();

    if (!nombre || !email || !mensaje) {
      form.style.animation = 'shake 0.4s ease';
      setTimeout(() => { form.style.animation = ''; }, 400);
      ['nombre', 'email', 'mensaje'].forEach(id => {
        const el = document.getElementById(id);
        if (el && !el.value.trim()) {
          el.style.borderColor = '#e05c5c';
          el.addEventListener('input', () => { el.style.borderColor = ''; }, { once: true });
        }
      });
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      const el = document.getElementById('email');
      el.style.borderColor = '#e05c5c';
      el.addEventListener('input', () => { el.style.borderColor = ''; }, { once: true });
      return;
    }

    // Deshabilitar botón
    const originalHTML = btnEnviar.innerHTML;
    btnEnviar.disabled = true;
    btnEnviar.innerHTML = '<span>Enviando</span><span class="sending-spinner">⏳</span>';

    try {
      // ── Verificar si el endpoint está configurado ──
      if (FORMSPREE_ENDPOINT.includes('XXXXXXXX')) {
        // Modo demo: simular envío exitoso
        await new Promise(r => setTimeout(r, 1200));
        showSuccess();
        return;
      }

      // ── Envío real a Formspree ──
      const data = new FormData(form);
      const response = await fetch(FORMSPREE_ENDPOINT, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      });

      if (response.ok) {
        showSuccess();
      } else {
        const json = await response.json();
        const errorMsg = json?.errors?.map(e => e.message).join(', ') || 'Error al enviar. Intenta de nuevo.';
        throw new Error(errorMsg);
      }

    } catch (err) {
      console.error('Error Formspree:', err);
      btnEnviar.disabled = false;
      btnEnviar.innerHTML = originalHTML;
      // Mostrar error inline
      let errEl = form.querySelector('.form-error-msg');
      if (!errEl) {
        errEl = document.createElement('p');
        errEl.className = 'form-error-msg';
        errEl.style.cssText = 'color:#e05c5c;font-size:0.85rem;text-align:center;margin-top:-8px';
        form.appendChild(errEl);
      }
      errEl.textContent = '⚠️ ' + (err.message || 'Hubo un problema. Por favor intenta nuevamente.');
    }
  });
}

function showSuccess() {
  form.classList.add('hidden');
  success.classList.remove('hidden');
  success.classList.add('fade-in', 'visible');
  success.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

console.log('🏛 Parde Arquitectos – Terreno Peñablanca listing loaded.');
