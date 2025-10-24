# Factura IA

Sistema de facturación inteligente construido con Django y Django REST Framework.

## Características

- Autenticación de usuarios.
- CRUD de clientes y productos.
- Gestión de facturas y actualización de stock.
- Generación de predicciones y análisis mediante OpenAI.
- API REST para integración con frontends.

Este repositorio solo incluye el backend; se puede conectar con
cualquier frontend profesional que consuma la API.

## Instalación

1. Crear un entorno virtual y activar.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```
4. Iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

Este proyecto usa SQLite por defecto para facilitar pruebas locales.
