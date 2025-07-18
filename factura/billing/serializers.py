"""Serializers translating billing models to JSON and back."""

from rest_framework import serializers

from .models import Client, Product, Invoice, InvoiceItem

class ClientSerializer(serializers.ModelSerializer):
    """Serializer for :class:`Client` instances."""

    class Meta:
        model = Client
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for :class:`Product` instances."""

    class Meta:
        model = Product
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    """Serializer for invoice line items."""

    class Meta:
        model = InvoiceItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for invoices including related items."""

    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'client', 'created_at', 'total', 'items']

    def create(self, validated_data):
        """Create an invoice along with its items and update stock."""

        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)

        total = 0
        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            price = product.price * quantity
            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity,
                price=price,
            )
            total += price
            # Reduce stock but never go negative
            product.stock = max(product.stock - quantity, 0)
            product.save()

        invoice.total = total
        invoice.save()
        return invoice
