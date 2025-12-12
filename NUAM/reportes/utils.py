from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generar_pdf(path, titulo, lineas):
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    story = [Paragraph(titulo, styles["Title"])]

    for linea in lineas:
        story.append(Paragraph(linea, styles["Normal"]))

    doc.build(story)

from openpyxl import Workbook


def generar_excel(path, encabezados, filas):
    wb = Workbook()
    ws = wb.active
    ws.append(encabezados)

    for fila in filas:
        ws.append(fila)

    wb.save(path)
