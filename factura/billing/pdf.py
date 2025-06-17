"""Simple PDF generation placeholder."""
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:  # pragma: no cover
    letter = None
    canvas = None


def generate_invoice_pdf(invoice, path: str):
    """Generate a PDF for the given invoice."""
    if canvas is None:
        with open(path, 'w') as f:
            f.write(f'Invoice {invoice.id} - {datetime.now()}')
        return
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f'Invoice {invoice.id}')
    y = 720
    for item in invoice.items.all():
        c.drawString(100, y, f'{item.product.name}: {item.quantity} x {item.price}')
        y -= 20
    c.drawString(100, y - 20, f'Total: {invoice.total}')
    c.save()
