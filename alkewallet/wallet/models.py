from django.db import models


class Moneda(models.Model):
    """Modelo para representar las monedas disponibles."""
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=5, unique=True)
    simbolo = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'

    def __str__(self):
        return f'{self.nombre} ({self.codigo})'


class Cuenta(models.Model):
    """Modelo para representar las cuentas de los usuarios."""
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, related_name='cuentas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.nombre} - {self.moneda.simbolo}{self.saldo}'


class Transaccion(models.Model):
    """Modelo para registrar todas las transacciones."""
    TIPO_CHOICES = [
        ('deposito', 'Depósito'),
        ('retiro', 'Retiro'),
        ('transferencia', 'Transferencia'),
    ]

    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='transacciones')
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.CharField(max_length=200, blank=True)
    cuenta_destino = models.ForeignKey(
        Cuenta, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='transferencias_recibidas'
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.cuenta.moneda.simbolo}{self.monto} ({self.cuenta.nombre})'
