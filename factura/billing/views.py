from rest_framework import viewsets, decorators, response
from .models import Client, Product, Invoice
from .serializers import ClientSerializer, ProductSerializer, InvoiceSerializer
from .pdf import generate_invoice_pdf

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @decorators.action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        invoice = self.get_object()
        path = f'invoice_{invoice.id}.pdf'
        generate_invoice_pdf(invoice, path)
        with open(path, 'rb') as f:
            data = f.read()
        return response.Response(data, content_type='application/pdf')
