# Alke Wallet - Proyecto Django (Módulo 6)

Aplicación web básica de billetera digital desarrollada con **Django 6.0.3** para el módulo 6 del programa Alke Solutions.

## Requisitos

- Python 3.x
- Django 6.0.3

## Instalación y ejecución

```bash
# 1. Activar entorno virtual
venv\Scripts\activate        # Windows

# 2. Instalar dependencias
pip install django

# 3. Entrar al directorio del proyecto
cd alkewallet

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Iniciar servidor de desarrollo
python manage.py runserver
```

Abrir en el navegador: **http://127.0.0.1:8000/**

## Estructura del proyecto

```
Alke-Wallet/
├── venv/                          # Entorno virtual
├── README.md                      # Este archivo
└── alkewallet/                    # Proyecto Django
    ├── manage.py                  # Utilidad de administración
    ├── db.sqlite3                 # Base de datos SQLite
    ├── alkewallet/                # Configuración del proyecto
    │   ├── __init__.py
    │   ├── settings.py            # Configuración general
    │   ├── urls.py                # URLs del proyecto (include wallet)
    │   ├── wsgi.py
    │   └── asgi.py
    └── wallet/                    # Aplicación principal
        ├── __init__.py
        ├── apps.py                # Configuración de la app
        ├── admin.py               # Admin (por defecto)
        ├── models.py              # Modelos (por defecto)
        ├── views.py               # 5 vistas con lógica de negocio
        ├── urls.py                # 5 rutas con nombres
        ├── tests.py               # Tests (por defecto)
        ├── templates/wallet/      # Plantillas HTML
        │   ├── base.html          # Template base (herencia)
        │   ├── inicio.html        # Dashboard principal
        │   ├── depositar.html     # Formulario de depósito
        │   ├── transferir.html    # Transferencias con numpad
        │   ├── transacciones.html # Historial de movimientos
        │   └── perfil.html        # Perfil del usuario
        └── static/wallet/css/     # Archivos estáticos
            └── styles.css         # Estilos CSS premium
```

## Funcionalidades

| Página | URL | Descripción |
|--------|-----|-------------|
| Dashboard | `/` | Balance, acciones rápidas, últimos movimientos |
| Depositar | `/depositar/` | Formulario funcional de depósito (actualiza saldo) |
| Transferir | `/transferir/` | Numpad interactivo + selección de contacto |
| Transacciones | `/transacciones/` | Historial completo con gráfico visual |
| Perfil | `/perfil/` | Información del usuario y configuración |

## Conceptos Django aplicados

- **Proyecto y App**: Estructura `alkewallet/` (proyecto) + `wallet/` (aplicación)
- **INSTALLED_APPS**: App registrada en `settings.py`
- **URLs**: Configuración a nivel de proyecto (`include()`) y de aplicación (`app_name`)
- **Vistas**: Funciones que manejan GET y POST, con contexto dinámico
- **Templates**: Herencia con `{% extends %}`, tags `{% url %}`, `{% for %}`, `{% if %}`, `{% csrf_token %}`
- **Archivos estáticos**: CSS cargado con `{% load static %}` y `{% static %}`
- **Sesiones**: Persistencia de saldo y transacciones durante la sesión
- **Messages**: Framework de mensajes para feedback al usuario

## Autor

Proyecto desarrollado como parte del módulo 6 del programa Alke Solutions.
