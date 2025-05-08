from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from config import PDF_OUTPUT

def generate_pdf(devices):
    """
    Генерирует простой PDF-отчёт об устройствах в сети.
    """
    try:
        c = canvas.Canvas(PDF_OUTPUT, pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Отчёт о сети")
        y -= 30

        c.setFont("Helvetica", 11)
        for device in devices:
            line = f"{device['ip']} ({device['type']}) - {device['hostname']} - {device['mac']}"
            c.drawString(50, y, line)
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50

        c.save()
        print(f"[PDF] PDF-отчёт сохранён: {PDF_OUTPUT}")
    except Exception as e:
        print(f"[PDF] Ошибка генерации PDF: {e}")