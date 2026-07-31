import os
from PIL import Image

base_dir = r"c:\Users\HP\Documents\antigravity\busy-brahmagupta"
img_path = os.path.join(base_dir, "imagen_aerea_terreno.jpg")
backup_path = os.path.join(base_dir, "imagen_aerea_terreno_orig_backup.jpg")

img = Image.open(img_path)
w, h = img.size

# Si la imagen aun no ha sido recortada y tiene resolucion 720x1600
if not os.path.exists(backup_path):
    img.save(backup_path)

# Recortar bordes del pantallazo (quitar barra de estado superior e interfaz inferior)
# Para 720x1600: recortamos desde y=140 hasta y=1260
top_crop = int(h * 0.11)  # ~176px
bottom_crop = int(h * 0.78) # ~1248px
left_crop = int(w * 0.02)
right_crop = int(w * 0.98)

cropped_img = img.crop((left_crop, top_crop, right_crop, bottom_crop))
cropped_img.save(img_path, quality=98)

print(f"Imagen recortada exitosamente de ({w}x{h}) a ({cropped_img.width}x{cropped_img.height}) enfocando solo el sitio.")
