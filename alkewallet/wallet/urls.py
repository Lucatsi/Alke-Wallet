from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('depositar/', views.depositar, name='depositar'),
    path('transferir/', views.transferir, name='transferir'),
    path('transacciones/', views.transacciones, name='transacciones'),
    path('perfil/', views.perfil, name='perfil'),
]
