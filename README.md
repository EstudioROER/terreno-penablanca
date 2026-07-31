# 🏛 Terreno Peñablanca – Landing Page

Landing page de venta de terreno en sector Peñablanca, Villa Alemana.  
Desarrollada por **Parde Arquitectos** · [www.pardearquitectos.com](https://www.pardearquitectos.com)

---

## ⚡ Pasos para publicar con HTTPS (GitHub Pages + Formspree)

### 1. Obtener tu Form ID de Formspree

1. Ve a [formspree.io](https://formspree.io) y crea una cuenta gratuita
2. Haz clic en **"New Form"**
3. Nombre: `Consultas Terreno Peñablanca`
4. Email: `contacto@pardearquitectos.com`
5. Copia tu **Form ID** (tiene formato: `abcd1234`)

### 2. Actualizar `main.js`

Abre `main.js` y reemplaza la línea:
```js
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/XXXXXXXX';
```
Por tu ID real:
```js
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/abcd1234';
```

### 3. Subir a GitHub

```bash
# Desde la carpeta del proyecto
git init
git add .
git commit -m "Landing page terreno Peñablanca"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### 4. Activar GitHub Pages

1. En GitHub: ve a **Settings → Pages**
2. Source: **Deploy from a branch** → `main` → `/ (root)`
3. Guarda. En 1-2 minutos la página estará en `https://TU_USUARIO.github.io/TU_REPO`

### 5. Conectar dominio www.pardearquitectos.com (cuando esté listo)

En tu proveedor de dominio, agrega estos DNS:

| Tipo | Host | Valor |
|------|------|-------|
| CNAME | `www` | `TU_USUARIO.github.io` |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

Luego en GitHub Pages → Custom domain: escribe `www.pardearquitectos.com` → Save.  
GitHub genera el certificado HTTPS automáticamente (puede tardar hasta 24h en propagarse).

---

## 📁 Estructura del proyecto

```
/
├── index.html          ← Landing page principal
├── style.css           ← Estilos premium dark mode
├── main.js             ← Interactividad + Formspree AJAX
├── imagen_aerea_terreno.jpg  ← Foto aérea del terreno
├── CNAME               ← Dominio para GitHub Pages
└── README.md           ← Este archivo
```

---

## 📧 Formulario

- Servicio: [Formspree](https://formspree.io) (gratis hasta 50 envíos/mes)  
- Destino: `contacto@pardearquitectos.com`  
- Al recibir una consulta, puedes responder directo al email del interesado
