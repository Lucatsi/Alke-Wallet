import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'alkewallet.settings'
django.setup()

from wallet.models import Moneda, Cuenta

# Crear monedas
clp, _ = Moneda.objects.get_or_create(codigo='CLP', defaults={'nombre': 'Peso Chileno', 'simbolo': '$'})
usd, _ = Moneda.objects.get_or_create(codigo='USD', defaults={'nombre': 'Dolar Estadounidense', 'simbolo': 'US$'})
eur, _ = Moneda.objects.get_or_create(codigo='EUR', defaults={'nombre': 'Euro', 'simbolo': 'E'})

# Crear cuentas
if not Cuenta.objects.exists():
    Cuenta.objects.create(nombre='Usuario Demo', email='usuario@alkewallet.com', telefono='+56 9 1234 5678', saldo=60000, moneda=clp)
    Cuenta.objects.create(nombre='Maria Garcia', email='maria@correo.com', telefono='+56 9 8765 4321', saldo=45000, moneda=clp)
    Cuenta.objects.create(nombre='Juan Perez', email='juan@correo.com', telefono='+56 9 5555 1234', saldo=120000, moneda=clp)
    Cuenta.objects.create(nombre='Ana Lopez', email='ana@correo.com', telefono='+56 9 3333 4444', saldo=30000, moneda=clp)
    print('Datos iniciales creados!')
else:
    print('Ya existen cuentas.')

print(f'Monedas: {Moneda.objects.count()}')
print(f'Cuentas: {Cuenta.objects.count()}')
