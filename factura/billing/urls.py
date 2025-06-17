"""Route definitions for the billing API."""

from rest_framework import routers
from django.urls import path

from .views import ClientViewSet, ProductViewSet, InvoiceViewSet
from .auth_views import RegisterView, LoginView

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = router.urls + [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
