import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from billing.models import Client, Product, Invoice, InvoiceItem


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(db):
    user = User.objects.create_user(username="testuser", password="testpass123")
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def sample_client(db):
    return Client.objects.create(name="Ana García", email="ana@test.com")


@pytest.fixture
def sample_product(db):
    return Product.objects.create(name="Laptop Pro X", price=1299.99, stock=10)


# --- Auth ---

@pytest.mark.django_db
def test_registro_usuario(api_client):
    response = api_client.post(
        "/api/register/",
        {"username": "nuevo", "password": "pass123"},
        format="json",
    )
    assert response.status_code == 200
    assert "token" in response.data


@pytest.mark.django_db
def test_login_usuario(api_client):
    User.objects.create_user(username="existing", password="pass123")
    response = api_client.post(
        "/api/login/",
        {"username": "existing", "password": "pass123"},
        format="json",
    )
    assert response.status_code == 200
    assert "token" in response.data


@pytest.mark.django_db
def test_login_credenciales_invalidas(api_client):
    response = api_client.post(
        "/api/login/",
        {"username": "nadie", "password": "wrong"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_endpoints_requieren_auth(api_client):
    for url in ["/api/clients/", "/api/products/", "/api/invoices/"]:
        response = api_client.get(url)
        assert response.status_code in [401, 403], f"{url} debería requerir autenticación"


# --- Clientes ---

@pytest.mark.django_db
def test_crear_cliente(auth_client):
    response = auth_client.post(
        "/api/clients/",
        {"name": "Juan Pérez", "email": "juan@test.com"},
        format="json",
    )
    assert response.status_code == 201
    assert Client.objects.filter(email="juan@test.com").exists()


@pytest.mark.django_db
def test_listar_clientes(auth_client, sample_client):
    response = auth_client.get("/api/clients/")
    assert response.status_code == 200
    assert len(response.data) >= 1


# --- Productos ---

@pytest.mark.django_db
def test_crear_producto(auth_client):
    response = auth_client.post(
        "/api/products/",
        {"name": "Monitor 4K", "price": "449.99", "stock": 5},
        format="json",
    )
    assert response.status_code == 201
    assert Product.objects.filter(name="Monitor 4K").exists()


# --- Facturas y stock ---

@pytest.mark.django_db
def test_crear_factura_descuenta_stock(auth_client, sample_client, sample_product):
    payload = {
        "client": sample_client.id,
        "total": "1299.99",
        "items": [
            {
                "product": sample_product.id,
                "quantity": 3,
                "price": "1299.99",
            }
        ],
    }
    response = auth_client.post("/api/invoices/", payload, format="json")
    assert response.status_code == 201

    sample_product.refresh_from_db()
    assert sample_product.stock == 7  # 10 - 3


@pytest.mark.django_db
def test_stock_no_queda_negativo(auth_client, sample_client, sample_product):
    payload = {
        "client": sample_client.id,
        "total": "12999.90",
        "items": [
            {
                "product": sample_product.id,
                "quantity": 999,
                "price": "1299.99",
            }
        ],
    }
    auth_client.post("/api/invoices/", payload, format="json")
    sample_product.refresh_from_db()
    assert sample_product.stock >= 0
