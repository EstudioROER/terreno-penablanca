import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

base_dir = r"c:\Users\HP\Documents\antigravity\busy-brahmagupta"
sat_img_path = os.path.join(base_dir, "imagen_aerea_terreno.jpg")
logo_path = os.path.join(base_dir, "img", "logo_horizontal.png")
out_dir = os.path.join(base_dir, "material_grafico")
os.makedirs(out_dir, exist_ok=True)

pdf_file = os.path.join(out_dir, "Carpeta_Ejecutiva_Terreno_Penablanca.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Linea superior de encabezado (paginas 2+)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 750, 558, 750)
            self.drawString(54, 758, "PARDE ARQUITECTOS · DOSSIER DE INVERSIÓN TERRENO PEÑABLANCA")
            self.drawRightString(558, 758, "+56 9 5019 6861")

        # Pie de página (todas las paginas)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 30, "Parde Arquitectos · www.pardearquitectos.com · contacto@pardearquitectos.com")
        self.drawRightString(558, 30, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_file,
    pagesize=letter,
    leftMargin=54,
    rightMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()

# Estilos personalizados
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    textColor=colors.HexColor('#0F172A'),
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    textColor=colors.HexColor('#059669'),
    spaceAfter=15
)

h2_style = ParagraphStyle(
    'Heading2Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor('#0F172A'),
    spaceBefore=12,
    spaceAfter=8
)

body_style = ParagraphStyle(
    'BodyCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#334155'),
    spaceAfter=8
)

body_bold = ParagraphStyle(
    'BodyBoldCustom',
    parent=body_style,
    fontName='Helvetica-Bold',
    textColor=colors.HexColor('#0F172A')
)

highlight_box_style = ParagraphStyle(
    'HighlightBox',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#065F46')
)

story = []

# =============================================================
# PÁGINA 1: PORTADA Y RESUMEN EJECUTIVO
# =============================================================

# Logo y Tagline Top
if os.path.exists(logo_path):
    logo_img = RLImage(logo_path, width=160, height=36)
    story.append(logo_img)
    story.append(Spacer(1, 10))

story.append(Paragraph("DOSSIER DE OPORTUNIDAD INMOBILIARIA", ParagraphStyle('Tagline', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#D97706'), spaceAfter=4)))
story.append(Paragraph("Terreno Urbano de 20.396 m² en Peñablanca", title_style))
story.append(Paragraph("📍 Los Coigüés N° 150 · Villa Alemana · Región de Valparaíso", subtitle_style))

# Cuadro Destacado de Precio y Liquidación
price_data = [
    [
        Paragraph("<b>PRECIO DE VENTA DIRECTA:</b>", ParagraphStyle('P1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#475569'))),
        Paragraph("<font color='#059669' size=16><b>$800.000.000 CLP</b></font>", ParagraphStyle('P2', alignment=2))
    ],
    [
        Paragraph("<b>Tasación Comercial Oficial:</b>", ParagraphStyle('P3', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#475569'))),
        Paragraph("<font color='#DC2626'><b>$1.767.204.994 CLP</b> (48.098 UF)</font>", ParagraphStyle('P4', alignment=2))
    ],
    [
        Paragraph("<b>Descuento sobre Tasación:</b>", ParagraphStyle('P5', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#0F172A'))),
        Paragraph("<b><font color='#D97706'>55% OFF</font> (Compras al 45% del valor real)</b>", ParagraphStyle('P6', alignment=2))
    ]
]
price_table = Table(price_data, colWidths=[240, 264])
price_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0FDF4')),
    ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#059669')),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#A7F3D0')),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
]))
story.append(price_table)
story.append(Spacer(1, 15))

# Foto Satelital Real Incorporada
if os.path.exists(sat_img_path):
    sat_img = RLImage(sat_img_path, width=504, height=250)
    story.append(sat_img)
    story.append(Paragraph("<font size=8 color='#64748B'><i>📷 Fotografía aérea y satelital oficial del predio (Parcela N° 102, Fundo Los Almendros, Peñablanca).</i></font>", ParagraphStyle('Caption', alignment=1, spaceBefore=4)))
    story.append(Spacer(1, 12))

# Resumen Ejecutivo
story.append(Paragraph("Resumen Ejecutivo", h2_style))
story.append(Paragraph(
    "Parde Arquitectos presenta la comercialización exclusiva y directa de un paño urbano estratégico de <b>20.396 m²</b> en la comuna de Villa Alemana. La propiedad posee una excelente aptitud para el desarrollo de condominios habitacionales de casas o edificios de departamentos de baja altura, contando con <b>factibilidad aprobada por ESVAL para agua potable y alcantarillado</b>.",
    body_style
))
story.append(Paragraph(
    "Por razones de oportuna liquidez de los propietarios, el terreno se ofrece a solo <b>$800.000.000 CLP</b> (~2,36 UF/m² útil), lo que representa un descuento real del <b>55% por debajo del informe formal de tasación comercial</b> elaborado por el tasador Claudio Reyes Stevens.",
    body_style
))

story.append(PageBreak())

# =============================================================
# PÁGINA 2: ANÁLISIS TÉCNICO, NORMATIVO Y LEGAL
# =============================================================

story.append(Paragraph("Ficha Técnica y Normativa Urbana (EX-H2)", h2_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#059669'), spaceBefore=2, spaceAfter=12))

tech_data = [
    [Paragraph("<b>Parámetro</b>", body_bold), Paragraph("<b>Detalle Oficial</b>", body_bold)],
    [Paragraph("Superficie Total", body_style), Paragraph("<b>20.396 m²</b> (Más de 2 Hectáreas)", body_style)],
    [Paragraph("Zonificación PRC", body_style), Paragraph("<b>EX-H2</b> (Zona Habitacional de Alta Densidad)", body_style)],
    [Paragraph("Coef. Constructibilidad", body_style), Paragraph("<b>1,60</b>", body_style)],
    [Paragraph("Coef. Ocupación Suelo", body_style), Paragraph("<b>0,40</b>", body_style)],
    [Paragraph("Densidad Máxima", body_style), Paragraph("<b>160 Viviendas / Hectárea</b>", body_style)],
    [Paragraph("Subdivisión Mínima", body_style), Paragraph("750 m² (para viviendas individuales)", body_style)],
    [Paragraph("Factibilidad Sanitaria", body_style), Paragraph("<b>ESVAL N° 147596</b> (Agua Potable y Alcantarillado)", body_style)],
    [Paragraph("Afectación Vial", body_style), Paragraph("Aprox. 4.800 m² afecto a utilidad pública por futura Av. Las Palmas (divide el terreno en 2 macro-lotes independientes ideales para proyecto por etapas).", body_style)],
]

tech_table = Table(tech_data, colWidths=[150, 354])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(tech_table)
story.append(Spacer(1, 15))

# Potencial de Negocio Inmobiliario
story.append(Paragraph("Evaluación Preliminar de Anteproyecto (Condominio)", h2_style))
story.append(Paragraph(
    "De acuerdo a la cabida preliminar desarrollada sobre el terreno, el activo ofrece métricas de rentabilidad sumamente atractivas para desarrolladores:",
    body_style
))

proj_data = [
    [Paragraph("<b>Cabida Departamentos Estimada:</b>", body_style), Paragraph("<b>326 Unidades</b> (62,5 m² promedio útil)", body_style)],
    [Paragraph("<b>Ventas Totales Proyectadas:</b>", body_style), Paragraph("<b>UF 806.850</b> (≈ $30.000 Millones CLP)", ParagraphStyle('Green', parent=body_style, textColor=colors.HexColor('#059669'), fontName='Helvetica-Bold'))],
    [Paragraph("<b>Costo Total del Proyecto:</b>", body_style), Paragraph("UF 695.560", body_style)],
    [Paragraph("<b>TIR Estimada Proyecto:</b>", body_style), Paragraph("<b>16,0% Anual</b>", ParagraphStyle('Gold', parent=body_style, textColor=colors.HexColor('#D97706'), fontName='Helvetica-Bold'))],
    [Paragraph("<b>Margen Neto sobre Ventas:</b>", body_style), Paragraph("<b>13,79% Utilidad Neta</b>", body_style)],
]
proj_table = Table(proj_data, colWidths=[180, 324])
proj_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAF5FF')),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#9333EA')),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E9D5FF')),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(proj_table)
story.append(Spacer(1, 15))

# Respaldo Legal
story.append(Paragraph("Carpeta de Antecedentes Legales Disponibles", h2_style))
legal_text = """
✓ <b>Certificado de Dominio Vigente:</b> CBR Villa Alemana (Folio 12139 · Mayo 2025).<br/>
✓ <b>Certificado de Hipotecas y Gravámenes:</b> Limpio, sin inscripciones vigentes ni prohibiciones en los últimos 30 años.<br/>
✓ <b>Certificado de Avalúo Fiscal:</b> ROL SII 00866-00175 ($575.085.118 CLP).<br/>
✓ <b>Certificado de Informes Previos (CIP):</b> DOM Villa Alemana.<br/>
✓ <b>Informe Formal de Tasación Comercial:</b> 48.098 UF ($1.767M) firmado por Claudio Reyes Stevens.
"""
story.append(Paragraph(legal_text, body_style))

story.append(PageBreak())

# =============================================================
# PÁGINA 3: UBICACIÓN Y CONTACTO DIRECTO
# =============================================================

story.append(Paragraph("Ubicación Estratégica y Accesibilidad", h2_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#059669'), spaceBefore=2, spaceAfter=12))

story.append(Paragraph(
    "El predio se ubica en el <b>Fundo Los Almendros de Peñablanca (Los Coigüés N° 150)</b>, en la comuna de Villa Alemana, a solo metros de Av. Vicepresidente Bernardo Leighton, una de las arterias estructurantes con conectividad directa al Troncal Sur, Viña del Mar y Valparaíso.",
    body_style
))

loc_data = [
    [Paragraph("<b>Dirección Exacta:</b>", body_style), Paragraph("Los Coigüés N° 150, Sector Peñablanca, Villa Alemana", body_style)],
    [Paragraph("<b>Coordenadas GPS:</b>", body_style), Paragraph("33°03'34.7\"S 71°21'08.4\"W", body_style)],
    [Paragraph("<b>ROL SII:</b>", body_style), Paragraph("00866-00175 · Comuna de Villa Alemana", body_style)],
    [Paragraph("<b>Entorno:</b>", body_style), Paragraph("Sector residencial consolidado en alta expansión inmobiliaria.", body_style)],
]
loc_table = Table(loc_data, colWidths=[140, 364])
loc_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(loc_table)
story.append(Spacer(1, 25))

# Caja de Contacto Directo Mesa de Negocios
contact_content = [
    [Paragraph("<font color='#FFFFFF' size=14><b>MESA DE NEGOCIOS · VENTA DIRECTA</b></font>", ParagraphStyle('CHead', alignment=1))],
    [Paragraph("<font color='#A7F3D0' size=11><b>PARDE ARQUITECTOS</b></font>", ParagraphStyle('CSub', alignment=1))],
    [Paragraph("<font color='#FFFFFF' size=10>Para agendar una visita a terreno o solicitar la carpeta legal en PDF:</font>", ParagraphStyle('CText', alignment=1))],
    [Paragraph("<font color='#FBBF24' size=14><b>📞 Teléfono / WhatsApp: +56 9 5019 6861</b></font>", ParagraphStyle('CPhone', alignment=1))],
    [Paragraph("<font color='#FFFFFF' size=11>✉️ Correo: <u>contacto@pardearquitectos.com</u></font>", ParagraphStyle('CMail', alignment=1))],
    [Paragraph("<font color='#CBD5E1' size=10>🌐 Sitio Web: <u>https://estudioroer.github.io/terreno-penablanca/</u></font>", ParagraphStyle('CWeb', alignment=1))],
]

contact_table = Table(contact_content, colWidths=[504])
contact_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F172A')),
    ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#059669')),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
]))

story.append(contact_table)
story.append(Spacer(1, 20))

disclaimer_text = """
<font size=7 color='#94A3B8'>
<b>Nota de Transparencia Comercial:</b> Los valores de tasación mostrados corresponden al informe técnico comercial emitido en mayo de 2025. El precio de venta directa de $800.000.000 CLP es exclusivo por razones de oportunidad de liquidez. La adquisición de esta propiedad está sujeta a los honorarios de gestión de corretaje del 3% + IVA a beneficio de Parde Arquitectos.
</font>
"""
story.append(Paragraph(disclaimer_text, body_style))

# Construir PDF
doc.build(story, canvasmaker=NumberedCanvas)
print("¡PDF generado exitosamente!")
