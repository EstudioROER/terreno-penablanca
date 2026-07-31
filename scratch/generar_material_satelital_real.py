import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

base_dir = r"c:\Users\HP\Documents\antigravity\busy-brahmagupta"
sat_img_path = os.path.join(base_dir, "imagen_aerea_terreno.jpg")
logo_path = os.path.join(base_dir, "img", "logo_horizontal_white.png")
out_dir = os.path.join(base_dir, "material_grafico")

os.makedirs(out_dir, exist_ok=True)

# Cargar imagen satelital real
sat_orig = Image.open(sat_img_path).convert("RGBA")

# Cargar logo si existe
try:
    logo_img = Image.open(logo_path).convert("RGBA")
except Exception:
    logo_img = None

def get_font(size, bold=False):
    font_names = ["arialbd.ttf" if bold else "arial.ttf", "segoeui.ttf", "tahoma.ttf"]
    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue
    return ImageFont.load_default()

# -------------------------------------------------------------
# 1. GENERAR ANUNCIO FEED (1:1 - 1080x1080)
# -------------------------------------------------------------
w_1x1, h_1x1 = 1080, 1080
# Recortar y escalar imagen satelital real para llenar 1080x1080
aspect = sat_orig.width / sat_orig.height
target_aspect = w_1x1 / h_1x1

if aspect > target_aspect:
    new_h = h_1x1
    new_w = int(aspect * new_h)
else:
    new_w = w_1x1
    new_h = int(new_w / aspect)

sat_resized = sat_orig.resize((new_w, new_h), Image.Resampling.LANCZOS)
left = (new_w - w_1x1) // 2
top = (new_h - h_1x1) // 2
sat_cropped = sat_resized.crop((left, top, left + w_1x1, top + h_1x1))

# Crear overlay oscuro arriba y abajo
feed_img = sat_cropped.copy()
draw = ImageDraw.Draw(feed_img)

# Degradado superior e inferior
overlay = Image.new("RGBA", (w_1x1, h_1x1), (0, 0, 0, 0))
draw_ov = ImageDraw.Draw(overlay)
# Arriba
for y in range(350):
    alpha = int(220 * (1 - y / 350))
    draw_ov.line([(0, y), (w_1x1, y)], fill=(9, 13, 22, alpha))
# Abajo
for y in range(h_1x1 - 450, h_1x1):
    alpha = int(235 * ((y - (h_1x1 - 450)) / 450))
    draw_ov.line([(0, y), (w_1x1, y)], fill=(9, 13, 22, alpha))

feed_img = Image.alpha_composite(feed_img, overlay)
draw = ImageDraw.Draw(feed_img)

# Badge Superior
draw.rounded_rectangle([50, 40, 520, 90], radius=25, fill=(255, 179, 0, 240))
draw.text((70, 52), "🔥 VENTA DIRECTA OPORTUNIDAD", fill=(0, 0, 0), font=get_font(22, True))

# Titulo Principal
draw.text((50, 110), "FOTO SATELITAL REAL DEL TERRENO", fill=(248, 113, 113), font=get_font(20, True))
draw.text((50, 135), "TERRENO URBANO PEÑABLANCA", fill=(255, 255, 255), font=get_font(42, True))
draw.text((50, 185), "20.396 m² totales · Parcela N° 102 Fundo Los Almendros", fill=(203, 213, 225), font=get_font(22))

# Tarjeta de Precio (Abajo a la izquierda)
card_bg = (15, 23, 42, 230)
draw.rounded_rectangle([50, 680, 1030, 930], radius=20, fill=card_bg, outline=(0, 230, 118), width=3)

draw.text((80, 700), "PRECIO DE VENTA DIRECTA LIQUIDACIÓN:", fill=(148, 163, 184), font=get_font(22, True))
draw.text((80, 730), "$800.000.000 CLP", fill=(0, 230, 118), font=get_font(60, True))
draw.text((80, 810), "Tasación Comercial Oficial: $1.767.204.994 CLP", fill=(248, 113, 113), font=get_font(24, True))
draw.text((80, 845), "¡Adquiere al 45% de su valor comercial! (55% de Descuento)", fill=(255, 255, 255), font=get_font(22))
draw.text((80, 880), "💧 Factibilidad ESVAL Aprobada N° 147596 (Agua y Alcantarillado)", fill=(163, 255, 208), font=get_font(20, True))

# Footer
draw.line([(50, 960), (1030, 960)], fill=(255, 255, 255, 50), width=2)
draw.text((50, 980), "📞 WhatsApp: +56 9 5019 6861  |  ✉️ contacto@pardearquitectos.com", fill=(255, 255, 255), font=get_font(24, True))
draw.text((50, 1015), "Parde Arquitectos · www.pardearquitectos.com", fill=(148, 163, 184), font=get_font(20))

feed_img.convert("RGB").save(os.path.join(out_dir, "anuncio_feed_oportunidad.jpg"), quality=95)


# -------------------------------------------------------------
# 2. GENERAR ANUNCIO STORY (9:16 - 1080x1920)
# -------------------------------------------------------------
w_st, h_st = 1080, 1920
if aspect > (w_st / h_st):
    new_h = h_st
    new_w = int(aspect * new_h)
else:
    new_w = w_st
    new_h = int(new_w / aspect)

sat_resized_st = sat_orig.resize((new_w, new_h), Image.Resampling.LANCZOS)
left = (new_w - w_st) // 2
top = (new_h - h_st) // 2
sat_cropped_st = sat_resized_st.crop((left, top, left + w_st, top + h_st))

story_img = sat_cropped_st.copy()
overlay_st = Image.new("RGBA", (w_st, h_st), (0, 0, 0, 0))
draw_st_ov = ImageDraw.Draw(overlay_st)

for y in range(500):
    alpha = int(230 * (1 - y / 500))
    draw_st_ov.line([(0, y), (w_st, y)], fill=(9, 13, 22, alpha))
for y in range(h_st - 750, h_st):
    alpha = int(240 * ((y - (h_st - 750)) / 750))
    draw_st_ov.line([(0, y), (w_st, y)], fill=(9, 13, 22, alpha))

story_img = Image.alpha_composite(story_img, overlay_st)
draw_st = ImageDraw.Draw(story_img)

# Contenidos Story
draw_st.rounded_rectangle([60, 80, 560, 135], radius=25, fill=(255, 179, 0, 240))
draw_st.text((80, 93), "🔥 FOTO SATELITAL REAL DEL TERRENO", fill=(0, 0, 0), font=get_font(20, True))

draw_st.text((60, 170), "TERRENO URBANO PEÑABLANCA", fill=(255, 255, 255), font=get_font(48, True))
draw_st.text((60, 230), "Parcela N° 102 · 20.396 m² Totales", fill=(0, 230, 118), font=get_font(30, True))
draw_st.text((60, 275), "Villa Alemana, Región de Valparaíso", fill=(203, 213, 225), font=get_font(24))

# Caja de Precio en Story
draw_st.rounded_rectangle([60, 1200, 1020, 1540], radius=25, fill=(15, 23, 42, 235), outline=(0, 230, 118), width=4)
draw_st.text((90, 1230), "PRECIO OFERTA DE LIQUIDACIÓN:", fill=(148, 163, 184), font=get_font(24, True))
draw_st.text((90, 1265), "$800.000.000 CLP", fill=(0, 230, 118), font=get_font(65, True))
draw_st.text((90, 1355), "Tasación Oficial: $1.767.204.994 CLP", fill=(248, 113, 113), font=get_font(26, True))
draw_st.text((90, 1395), "¡55% de descuento sobre valor comercial!", fill=(255, 255, 255), font=get_font(24, True))
draw_st.text((90, 1435), "💧 Con Factibilidad ESVAL Agua Potable y Alcantarillado", fill=(163, 255, 208), font=get_font(22))
draw_st.text((90, 1475), "📋 Títulos 100% limpios sin hipotecas ni prohibiciones", fill=(203, 213, 225), font=get_font(22))

# Boton CTA
draw_st.rounded_rectangle([60, 1600, 1020, 1720], radius=20, fill=(37, 211, 102, 240))
draw_st.text((160, 1635), "💬 TOCA PARA CONSULTAR POR WHATSAPP", fill=(0, 0, 0), font=get_font(30, True))

draw_st.text((60, 1760), "📞 WhatsApp: +56 9 5019 6861", fill=(255, 255, 255), font=get_font(28, True))
draw_st.text((60, 1800), "✉️ contacto@pardearquitectos.com  ·  www.pardearquitectos.com", fill=(148, 163, 184), font=get_font(22))

story_img.convert("RGB").save(os.path.join(out_dir, "anuncio_story_penablanca.jpg"), quality=95)


# -------------------------------------------------------------
# 3. GENERAR BANNER LINKEDIN (16:9 - 1200x628)
# -------------------------------------------------------------
w_li, h_li = 1200, 628
if aspect > (w_li / h_li):
    new_h = h_li
    new_w = int(aspect * new_h)
else:
    new_w = w_li
    new_h = int(new_w / aspect)

sat_resized_li = sat_orig.resize((new_w, new_h), Image.Resampling.LANCZOS)
left = (new_w - w_li) // 2
top = (new_h - h_li) // 2
sat_cropped_li = sat_resized_li.crop((left, top, left + w_li, top + h_li))

li_img = sat_cropped_li.copy()
overlay_li = Image.new("RGBA", (w_li, h_li), (0, 0, 0, 0))
draw_li_ov = ImageDraw.Draw(overlay_li)

# Degradado lateral izquierdo mas fuerte para texto ejecutivo
for x in range(800):
    alpha = int(245 * (1 - x / 800))
    draw_li_ov.line([(x, 0), (x, h_li)], fill=(9, 13, 22, alpha))
for y in range(h_li - 150, h_li):
    alpha = int(200 * ((y - (h_li - 150)) / 150))
    draw_li_ov.line([(0, y), (w_li, y)], fill=(9, 13, 22, alpha))

li_img = Image.alpha_composite(li_img, overlay_li)
draw_li = ImageDraw.Draw(li_img)

draw_li.rounded_rectangle([40, 30, 520, 70], radius=15, fill=(255, 179, 0, 240))
draw_li.text((55, 40), "📍 FOTO SATELITAL REAL DEL PREDIO", fill=(0, 0, 0), font=get_font(18, True))

draw_li.text((40, 85), "OPORTUNIDAD INMOBILIARIA V REGIÓN", fill=(0, 230, 118), font=get_font(24, True))
draw_li.text((40, 115), "Terreno Urbano 20.396 m² Peñablanca", fill=(255, 255, 255), font=get_font(38, True))
draw_li.text((40, 165), "Apto Condominios de Casas o Departamentos (Normativa EX-H2)", fill=(203, 213, 225), font=get_font(20))

# Caja de Oferta
draw_li.rounded_rectangle([40, 220, 680, 480], radius=20, fill=(15, 23, 42, 230), outline=(0, 230, 118), width=3)
draw_li.text((65, 240), "PRECIO DE VENTA DIRECTA:", fill=(148, 163, 184), font=get_font(18, True))
draw_li.text((65, 265), "$800.000.000 CLP", fill=(0, 230, 118), font=get_font(50, True))
draw_li.text((65, 335), "Tasación Comercial Formal: $1.767.204.994 CLP", fill=(248, 113, 113), font=get_font(20, True))
draw_li.text((65, 370), "💧 Factibilidad ESVAL N° 147596 para Agua Potable y Alcantarillado", fill=(255, 255, 255), font=get_font(18))
draw_li.text((65, 400), "📋 Títulos al día, sin gravámenes · Comisión corretaje 3% + IVA", fill=(203, 213, 225), font=get_font(17))

draw_li.text((40, 520), "📞 Teléfono / WhatsApp: +56 9 5019 6861  |  ✉️ contacto@pardearquitectos.com", fill=(255, 255, 255), font=get_font(20, True))
draw_li.text((40, 555), "Parde Arquitectos · www.pardearquitectos.com", fill=(148, 163, 184), font=get_font(18))

li_img.convert("RGB").save(os.path.join(out_dir, "banner_linkedin_b2b.jpg"), quality=95)


# -------------------------------------------------------------
# 4. GENERAR INFOGRAFÍA RENTABILIDAD (3:4 - 1080x1440)
# -------------------------------------------------------------
w_info, h_info = 1080, 1440
if aspect > (w_info / h_info):
    new_h = h_info
    new_w = int(aspect * new_h)
else:
    new_w = w_info
    new_h = int(new_w / aspect)

sat_resized_info = sat_orig.resize((new_w, new_h), Image.Resampling.LANCZOS)
left = (new_w - w_info) // 2
top = (new_h - h_info) // 2
sat_cropped_info = sat_resized_info.crop((left, top, left + w_info, top + h_info))

info_img = sat_cropped_info.copy()
overlay_info = Image.new("RGBA", (w_info, h_info), (0, 0, 0, 0))
draw_info_ov = ImageDraw.Draw(overlay_info)

for y in range(400):
    alpha = int(230 * (1 - y / 400))
    draw_info_ov.line([(0, y), (w_info, y)], fill=(9, 13, 22, alpha))
for y in range(h_info - 550, h_info):
    alpha = int(240 * ((y - (h_info - (h_info - 550))) / 550))
    draw_info_ov.line([(0, y), (w_info, y)], fill=(9, 13, 22, alpha))

info_img = Image.alpha_composite(info_img, overlay_info)
draw_info = ImageDraw.Draw(info_img)

draw_info.rounded_rectangle([50, 50, 520, 100], radius=20, fill=(255, 179, 0, 240))
draw_info.text((65, 62), "📍 FOTO SATELITAL REAL TERRENO", fill=(0, 0, 0), font=get_font(20, True))

draw_info.text((50, 130), "FICHA DE OPORTUNIDAD INMOBILIARIA", fill=(0, 230, 118), font=get_font(28, True))
draw_info.text((50, 170), "Terreno Peñablanca 20.396 m²", fill=(255, 255, 255), font=get_font(48, True))

# Grilla de métricas
draw_info.rounded_rectangle([50, 750, 1030, 1260], radius=24, fill=(15, 23, 42, 235), outline=(0, 230, 118), width=3)

draw_info.text((80, 780), "METRICAS CLAVE DE LA PROPIEDAD:", fill=(148, 163, 184), font=get_font(22, True))

draw_info.text((80, 830), "• Precio de Liquidación:", fill=(255, 255, 255), font=get_font(24, True))
draw_info.text((450, 830), "$800.000.000 CLP", fill=(0, 230, 118), font=get_font(28, True))

draw_info.text((80, 880), "• Tasación Oficial Comercial:", fill=(255, 255, 255), font=get_font(24, True))
draw_info.text((450, 880), "$1.767.204.994 CLP", fill=(248, 113, 113), font=get_font(26, True))

draw_info.text((80, 930), "• Descuento sobre Tasación:", fill=(255, 255, 255), font=get_font(24, True))
draw_info.text((450, 930), "55% OFF (Compras al 45%)", fill=(255, 179, 0), font=get_font(24, True))

draw_info.text((80, 980), "• Factibilidad Agua y Alc.:", fill=(255, 255, 255), font=get_font(24, True))
draw_info.text((450, 980), "ESVAL Aprobado N° 147596", fill=(163, 255, 208), font=get_font(24, True))

draw_info.text((80, 1030), "• Normativa Urbana:", fill=(255, 255, 255), font=get_font(24, True))
draw_info.text((450, 1030), "EX-H2 (Alta Densidad)", fill=(203, 213, 225), font=get_font(24, True))

draw_info.text((80, 1080), "• Ubicación Exacta:", fill=(255, 255, 255), font=get_font(24, True))
draw_info.text((450, 1080), "Los Coigüés N° 150, Peñablanca", fill=(203, 213, 225), font=get_font(24, True))

draw_info.text((80, 1130), "• Retorno Proyectado (TIR):", fill=(255, 255, 255), font=get_font(24, True))
draw_info.text((450, 1130), "16.0% Anual (326 Deptos)", fill=(0, 230, 118), font=get_font(24, True))

# Footer
draw_info.text((50, 1310), "📞 WhatsApp: +56 9 5019 6861  |  ✉️ contacto@pardearquitectos.com", fill=(255, 255, 255), font=get_font(24, True))
draw_info.text((50, 1350), "Parde Arquitectos · www.pardearquitectos.com", fill=(148, 163, 184), font=get_font(20))

info_img.convert("RGB").save(os.path.join(out_dir, "infografia_rentabilidad.jpg"), quality=95)

print("¡Todas las imagenes compuestas 100% con la FOTO SATELITAL REAL se han generado correctamente!")
