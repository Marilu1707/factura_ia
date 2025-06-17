"""REST API views for the billing application."""

from rest_framework import viewsets, decorators, response

from .models import Client, Product, Invoice
from .serializers import ClientSerializer, ProductSerializer, InvoiceSerializer
from .pdf import generate_invoice_pdf

class ClientViewSet(viewsets.ModelViewSet):
    """CRUD operations for :class:`Client` objects."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """CRUD operations for :class:`Product` objects."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    """Manage invoices and provide PDF exports."""

    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @decorators.action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """Return the invoice PDF."""

        invoice = self.get_object()
        data = generate_invoice_pdf(invoice)
        return response.Response(data, content_type='application/pdf')
