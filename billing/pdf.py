"""Utility for generating invoice PDFs."""

from datetime import datetime
from io import BytesIO

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:  # pragma: no cover
    letter = None
    canvas = None


def generate_invoice_pdf(invoice) -> bytes:
    """Return a PDF document for ``invoice`` as raw bytes.

    The implementation falls back to a simple text file if ``reportlab``
    is not installed.
    """
    buffer = BytesIO()
    if canvas is None:
        buffer.write(f'Invoice {invoice.id} - {datetime.now()}'.encode())
        return buffer.getvalue()

    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f'Invoice {invoice.id}')
    y = 720
    for item in invoice.items.all():
        c.drawString(100, y, f'{item.product.name}: {item.quantity} x {item.price}')
        y -= 20
    c.drawString(100, y - 20, f'Total: {invoice.total}')
    c.save()
    buffer.seek(0)
    return buffer.read()
