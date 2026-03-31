from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Moneda, Cuenta, Transaccion
from decimal import Decimal


def inicio(request):
    """Vista principal - Dashboard."""
    cuentas = Cuenta.objects.filter(activa=True)
    transacciones_recientes = Transaccion.objects.all()[:5]

    # Calcular saldo total
    saldo_total = sum(c.saldo for c in cuentas)

    # Formatear transacciones para el template
    tx_list = []
    for tx in transacciones_recientes:
        if tx.tipo == 'deposito':
            tipo_css = 'income'
            clase = 'positive'
            monto_fmt = f'+{tx.cuenta.moneda.simbolo}{tx.monto:,.0f}'.replace(',', '.')
        elif tx.tipo == 'retiro':
            tipo_css = 'expense'
            clase = 'negative'
            monto_fmt = f'-{tx.cuenta.moneda.simbolo}{tx.monto:,.0f}'.replace(',', '.')
        else:
            tipo_css = 'transfer'
            clase = 'negative'
            monto_fmt = f'-{tx.cuenta.moneda.simbolo}{tx.monto:,.0f}'.replace(',', '.')

        tx_list.append({
            'tipo': tipo_css,
            'titulo': tx.descripcion or tx.get_tipo_display(),
            'fecha': tx.fecha.strftime('%d %b %Y'),
            'monto': monto_fmt,
            'clase': clase,
        })

    contexto = {
        'titulo': 'Dashboard',
        'saldo': f'${saldo_total:,.0f}'.replace(',', '.') if cuentas else '$0',
        'usuario': cuentas.first().nombre if cuentas.exists() else 'Usuario',
        'transacciones': tx_list,
        'num_cuentas': cuentas.count(),
    }
    return render(request, 'wallet/inicio.html', contexto)


def depositar(request):
    """Vista de depósito de dinero - CRUD: Create (Transacción) + Update (Saldo)."""
    cuentas = Cuenta.objects.filter(activa=True)

    if request.method == 'POST':
        try:
            cuenta_id = request.POST.get('cuenta')
            monto = Decimal(request.POST.get('monto', '0'))
            metodo = request.POST.get('metodo', '')
            descripcion = request.POST.get('descripcion', '')

            if monto <= 0:
                messages.error(request, 'El monto debe ser mayor a $0.')
                return redirect('wallet:depositar')
            if not metodo:
                messages.error(request, 'Selecciona un método de depósito.')
                return redirect('wallet:depositar')
            if not cuenta_id:
                messages.error(request, 'Selecciona una cuenta.')
                return redirect('wallet:depositar')

            cuenta = get_object_or_404(Cuenta, pk=cuenta_id, activa=True)

            # Crear transacción en la base de datos (CREATE)
            Transaccion.objects.create(
                cuenta=cuenta,
                tipo='deposito',
                monto=monto,
                descripcion=descripcion if descripcion else f'Depósito vía {metodo}',
            )

            # Actualizar saldo de la cuenta (UPDATE)
            cuenta.saldo += monto
            cuenta.save()

            messages.success(request,
                f'¡Depósito de {cuenta.moneda.simbolo}{monto:,.0f} realizado con éxito!'.replace(',', '.'))
            return redirect('wallet:depositar')

        except (ValueError, TypeError):
            messages.error(request, 'Monto inválido.')
            return redirect('wallet:depositar')

    cuenta_principal = cuentas.first()
    contexto = {
        'titulo': 'Depositar',
        'saldo': f'{cuenta_principal.moneda.simbolo}{cuenta_principal.saldo:,.0f}'.replace(',', '.') if cuenta_principal else '$0',
        'cuentas': cuentas,
    }
    return render(request, 'wallet/depositar.html', contexto)


def transferir(request):
    """Vista de transferencia - CRUD: Create (Transacción) + Update (Saldos)."""
    cuentas = Cuenta.objects.filter(activa=True)

    if request.method == 'POST':
        try:
            cuenta_origen_id = request.POST.get('cuenta_origen')
            cuenta_destino_id = request.POST.get('contacto')
            monto = Decimal(request.POST.get('monto', '0'))

            if monto <= 0:
                messages.error(request, 'Ingresa un monto válido.')
                return redirect('wallet:transferir')

            cuenta_origen = get_object_or_404(Cuenta, pk=cuenta_origen_id, activa=True)

            if not cuenta_destino_id:
                messages.error(request, 'Selecciona un destinatario.')
                return redirect('wallet:transferir')

            cuenta_destino = get_object_or_404(Cuenta, pk=cuenta_destino_id, activa=True)

            if cuenta_origen.pk == cuenta_destino.pk:
                messages.error(request, 'No puedes transferir a la misma cuenta.')
                return redirect('wallet:transferir')

            if monto > cuenta_origen.saldo:
                messages.error(request, 'Saldo insuficiente para esta transferencia.')
                return redirect('wallet:transferir')

            # Crear transacción de envío (CREATE)
            Transaccion.objects.create(
                cuenta=cuenta_origen,
                tipo='transferencia',
                monto=monto,
                descripcion=f'Transferencia a {cuenta_destino.nombre}',
                cuenta_destino=cuenta_destino,
            )

            # Crear transacción de recepción (CREATE)
            Transaccion.objects.create(
                cuenta=cuenta_destino,
                tipo='deposito',
                monto=monto,
                descripcion=f'Transferencia de {cuenta_origen.nombre}',
            )

            # Actualizar saldos (UPDATE)
            cuenta_origen.saldo -= monto
            cuenta_origen.save()
            cuenta_destino.saldo += monto
            cuenta_destino.save()

            messages.success(request,
                f'¡Transferencia de {cuenta_origen.moneda.simbolo}{monto:,.0f} a {cuenta_destino.nombre} realizada!'.replace(',', '.'))
            return redirect('wallet:transferir')

        except (ValueError, TypeError):
            messages.error(request, 'Error en la transferencia.')
            return redirect('wallet:transferir')

    cuenta_principal = cuentas.first()
    otras_cuentas = cuentas.exclude(pk=cuenta_principal.pk) if cuenta_principal else cuentas

    # Preparar contactos desde la base de datos
    contactos = []
    colores = ['green', 'blue', 'orange', 'pink', 'purple']
    for i, cuenta in enumerate(otras_cuentas):
        iniciales = ''.join([p[0].upper() for p in cuenta.nombre.split()[:2]])
        contactos.append({
            'id': cuenta.pk,
            'iniciales': iniciales,
            'nombre': cuenta.nombre,
            'email': cuenta.email,
            'color': colores[i % len(colores)],
        })

    contexto = {
        'titulo': 'Transferir',
        'saldo': f'{cuenta_principal.moneda.simbolo}{cuenta_principal.saldo:,.0f}'.replace(',', '.') if cuenta_principal else '$0',
        'contactos': contactos,
        'cuenta_principal': cuenta_principal,
    }
    return render(request, 'wallet/transferir.html', contexto)


def transacciones(request):
    """Vista del historial - CRUD: Read (listar transacciones)."""
    todas = Transaccion.objects.select_related('cuenta', 'cuenta__moneda').all()

    tx_list = []
    for tx in todas:
        if tx.tipo == 'deposito':
            tipo_css = 'income'
            clase = 'positive'
            monto_fmt = f'+{tx.cuenta.moneda.simbolo}{tx.monto:,.0f}'.replace(',', '.')
        elif tx.tipo == 'retiro':
            tipo_css = 'expense'
            clase = 'negative'
            monto_fmt = f'-{tx.cuenta.moneda.simbolo}{tx.monto:,.0f}'.replace(',', '.')
        else:
            tipo_css = 'transfer'
            clase = 'negative'
            monto_fmt = f'-{tx.cuenta.moneda.simbolo}{tx.monto:,.0f}'.replace(',', '.')

        tx_list.append({
            'id': tx.pk,
            'tipo': tipo_css,
            'titulo': tx.descripcion or tx.get_tipo_display(),
            'fecha': tx.fecha.strftime('%d %b %Y'),
            'monto': monto_fmt,
            'clase': clase,
        })

    contexto = {
        'titulo': 'Transacciones',
        'transacciones': tx_list,
    }
    return render(request, 'wallet/transacciones.html', contexto)


def perfil(request):
    """Vista del perfil del usuario."""
    cuenta = Cuenta.objects.filter(activa=True).first()
    contexto = {
        'titulo': 'Mi Perfil',
        'usuario': {
            'nombre': cuenta.nombre if cuenta else 'Usuario Demo',
            'email': cuenta.email if cuenta else 'usuario@alkewallet.com',
            'telefono': cuenta.telefono if cuenta else '+56 9 1234 5678',
            'miembro_desde': cuenta.fecha_creacion.strftime('%B %Y') if cuenta else 'Enero 2026',
        },
    }
    return render(request, 'wallet/perfil.html', contexto)


# ============================
# CRUD de Cuentas
# ============================

def cuentas_lista(request):
    """READ - Listar todas las cuentas."""
    cuentas = Cuenta.objects.select_related('moneda').all()
    contexto = {
        'titulo': 'Cuentas',
        'cuentas': cuentas,
    }
    return render(request, 'wallet/cuentas_lista.html', contexto)


def cuenta_crear(request):
    """CREATE - Crear una nueva cuenta."""
    monedas = Moneda.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        moneda_id = request.POST.get('moneda')
        saldo = request.POST.get('saldo', '0')

        if not nombre or not email or not moneda_id:
            messages.error(request, 'Completa todos los campos obligatorios.')
            return redirect('wallet:cuenta_crear')

        # Verificar que no exista el email
        if Cuenta.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe una cuenta con ese email.')
            return redirect('wallet:cuenta_crear')

        moneda = get_object_or_404(Moneda, pk=moneda_id)

        Cuenta.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            moneda=moneda,
            saldo=Decimal(saldo) if saldo else 0,
        )
        messages.success(request, f'¡Cuenta de {nombre} creada con éxito!')
        return redirect('wallet:cuentas_lista')

    contexto = {
        'titulo': 'Nueva Cuenta',
        'monedas': monedas,
    }
    return render(request, 'wallet/cuenta_form.html', contexto)


def cuenta_editar(request, pk):
    """UPDATE - Editar una cuenta existente."""
    cuenta = get_object_or_404(Cuenta, pk=pk)
    monedas = Moneda.objects.all()

    if request.method == 'POST':
        cuenta.nombre = request.POST.get('nombre', cuenta.nombre).strip()
        cuenta.email = request.POST.get('email', cuenta.email).strip()
        cuenta.telefono = request.POST.get('telefono', '').strip()
        moneda_id = request.POST.get('moneda')
        if moneda_id:
            cuenta.moneda = get_object_or_404(Moneda, pk=moneda_id)

        cuenta.save()
        messages.success(request, f'Cuenta de {cuenta.nombre} actualizada.')
        return redirect('wallet:cuentas_lista')

    contexto = {
        'titulo': 'Editar Cuenta',
        'cuenta': cuenta,
        'monedas': monedas,
    }
    return render(request, 'wallet/cuenta_form.html', contexto)


def cuenta_eliminar(request, pk):
    """DELETE - Eliminar una cuenta."""
    cuenta = get_object_or_404(Cuenta, pk=pk)

    if request.method == 'POST':
        nombre = cuenta.nombre
        cuenta.delete()
        messages.success(request, f'Cuenta de {nombre} eliminada.')
        return redirect('wallet:cuentas_lista')

    contexto = {
        'titulo': 'Eliminar Cuenta',
        'cuenta': cuenta,
    }
    return render(request, 'wallet/cuenta_confirmar_eliminar.html', contexto)


def transaccion_eliminar(request, pk):
    """DELETE - Eliminar una transacción."""
    tx = get_object_or_404(Transaccion, pk=pk)

    if request.method == 'POST':
        tx.delete()
        messages.success(request, 'Transacción eliminada.')
        return redirect('wallet:transacciones')

    contexto = {
        'titulo': 'Eliminar Transacción',
        'transaccion': tx,
    }
    return render(request, 'wallet/transaccion_confirmar_eliminar.html', contexto)
