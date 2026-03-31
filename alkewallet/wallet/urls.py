from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    # Páginas principales
    path('', views.inicio, name='inicio'),
    path('depositar/', views.depositar, name='depositar'),
    path('transferir/', views.transferir, name='transferir'),
    path('transacciones/', views.transacciones, name='transacciones'),
    path('perfil/', views.perfil, name='perfil'),

    # CRUD de Cuentas
    path('cuentas/', views.cuentas_lista, name='cuentas_lista'),
    path('cuentas/nueva/', views.cuenta_crear, name='cuenta_crear'),
    path('cuentas/<int:pk>/editar/', views.cuenta_editar, name='cuenta_editar'),
    path('cuentas/<int:pk>/eliminar/', views.cuenta_eliminar, name='cuenta_eliminar'),

    # Eliminar transacción
    path('transacciones/<int:pk>/eliminar/', views.transaccion_eliminar, name='transaccion_eliminar'),
]
