from django.contrib import admin
from .models import Moneda, Cuenta, Transaccion


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'simbolo')
    search_fields = ('nombre', 'codigo')


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'saldo', 'moneda', 'activa', 'fecha_creacion')
    list_filter = ('moneda', 'activa')
    search_fields = ('nombre', 'email')


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('cuenta', 'tipo', 'monto', 'descripcion', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('descripcion', 'cuenta__nombre')
