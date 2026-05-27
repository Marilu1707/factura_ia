# Factura IA 🤖

> Sistema de facturación con reportes inteligentes generados por IA

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.x-A30000)](https://www.django-rest-framework.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai&logoColor=white)](https://openai.com)
[![pytest](https://img.shields.io/badge/pytest-passing-green?logo=pytest)](https://pytest.org)

API REST backend que gestiona facturación y usa **GPT-4 para convertir datos de ventas en reportes ejecutivos en lenguaje natural**.

---

## ¿Qué problema resuelve?

Las empresas generan decenas de facturas por mes y pierden tiempo interpretando tablas y exportando a Excel. Factura IA automatiza la gestión (clientes, productos, stock, PDFs) y genera reportes de ventas listos para presentar en reuniones — sin necesidad de un analista.

---

## Demo del reporte IA

**Input** — métricas del período enviadas al endpoint:
```json
{
  "period": "Abril 2026",
  "total_revenue": 158420.50,
  "top_product": "Laptop Pro X (32 unidades)",
  "invoices_count": 47
}
```

**Output** — reporte generado por GPT-4:
```
En abril de 2026 se registraron 47 facturas por un total de $158.420,50.
El producto estrella fue Laptop Pro X con 32 unidades despachadas,
representando el 34% de los ingresos del período. Se recomienda incrementar
el stock antes del cierre del trimestre dado el ritmo de ventas sostenido.
```

---

## Arquitectura

```
Cliente (frontend / Postman)
         │
         ▼
  ┌─────────────────────────────────┐
  │         API REST (DRF)          │
  │                                 │
  │  POST /api/register/  → Auth    │
  │  POST /api/login/     → Token   │
  │  CRUD /api/clients/             │
  │  CRUD /api/products/            │
  │  CRUD /api/invoices/            │
  │  GET  /api/invoices/{id}/pdf/   │
  └──────────────┬──────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
  Django ORM          OpenAI GPT-4
  (SQLite / PG)       analytics/ai.py
                      └─ predict_sales()
                      └─ detect_irregularities()
```

---

## Stack

| Tecnología | Uso |
|---|---|
| Python 3.11 | Lenguaje base |
| Django 4.2 + DRF | Framework web y API REST |
| OpenAI GPT-4 | Generación de reportes en lenguaje natural |
| SQLite | Base de datos (desarrollo) |
| pytest-django | Suite de tests con mocks |
| pandas + matplotlib | Análisis exploratorio (notebook) |

---

## Features

- Registro y login con autenticación por token
- CRUD completo de clientes y productos
- Gestión de facturas con **actualización automática de stock**
- Generación de PDF por factura
- 🤖 **Reportes de ventas generados con GPT-4** (`analytics/ai.py`)
- **Test suite completa** con mocks de OpenAI (sin consumir créditos)
- Notebook de análisis exploratorio con visualizaciones

---

## Instalación

```bash
git clone https://github.com/Marilu1707/factura_ia.git
cd factura_ia

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # Completar OPENAI_API_KEY en .env
python manage.py migrate
python manage.py runserver
```

---

## Variables de entorno

Copiar `.env.example` a `.env` y completar:

```env
SECRET_KEY=your-django-secret-key
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ El archivo `.env` está en `.gitignore`. Nunca se sube al repositorio.

---

## Endpoints

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/api/register/` | Registro de usuario → devuelve token | No |
| POST | `/api/login/` | Login → devuelve token | No |
| GET / POST | `/api/clients/` | Listar / crear clientes | Token |
| GET / PUT / DELETE | `/api/clients/{id}/` | Detalle de cliente | Token |
| GET / POST | `/api/products/` | Listar / crear productos | Token |
| GET / POST | `/api/invoices/` | Listar / crear facturas | Token |
| GET | `/api/invoices/{id}/pdf/` | Descargar factura en PDF | Token |

---

## Tests

```bash
pytest -v
```

Los tests de IA usan `unittest.mock` — no requieren API key ni créditos de OpenAI.

---

## Notebook de análisis

Ver [`notebooks/analisis_facturacion.ipynb`](notebooks/analisis_facturacion.ipynb) para:
- Análisis exploratorio de 50 facturas simuladas
- Visualizaciones: ventas mensuales, top productos, distribución de montos
- Demo del reporte generado por GPT-4
