from django.shortcuts import render, redirect
from django.contrib import messages


def inicio(request):
    """Vista principal - Dashboard con balance y acciones rápidas."""
    # Obtener saldo de la sesión (o valor inicial)
    if 'saldo' not in request.session:
        request.session['saldo'] = 60000

    # Obtener historial de transacciones de la sesión
    if 'historial' not in request.session:
        request.session['historial'] = [
            {'tipo': 'income', 'titulo': 'Depósito recibido', 'fecha': '28 Mar 2026', 'monto': '+$15.000', 'clase': 'positive'},
            {'tipo': 'expense', 'titulo': 'Pago de servicios', 'fecha': '27 Mar 2026', 'monto': '-$8.500', 'clase': 'negative'},
            {'tipo': 'transfer', 'titulo': 'Transferencia a María', 'fecha': '26 Mar 2026', 'monto': '-$12.000', 'clase': 'negative'},
            {'tipo': 'income', 'titulo': 'Sueldo mensual', 'fecha': '25 Mar 2026', 'monto': '+$450.000', 'clase': 'positive'},
        ]

    saldo = request.session['saldo']
    contexto = {
        'titulo': 'Dashboard',
        'saldo': f'${saldo:,.0f}'.replace(',', '.'),
        'usuario': 'Usuario',
        'transacciones': request.session['historial'][:5],
    }
    return render(request, 'wallet/inicio.html', contexto)


def depositar(request):
    """Vista de depósito de dinero."""
    if 'saldo' not in request.session:
        request.session['saldo'] = 60000

    if request.method == 'POST':
        try:
            monto = int(request.POST.get('monto', 0))
            metodo = request.POST.get('metodo', '')
            descripcion = request.POST.get('descripcion', 'Depósito')

            if monto <= 0:
                messages.error(request, 'El monto debe ser mayor a $0.')
                return redirect('wallet:depositar')

            if not metodo:
                messages.error(request, 'Selecciona un método de depósito.')
                return redirect('wallet:depositar')

            # Actualizar saldo
            request.session['saldo'] = request.session.get('saldo', 60000) + monto

            # Agregar al historial
            historial = request.session.get('historial', [])
            historial.insert(0, {
                'tipo': 'income',
                'titulo': descripcion if descripcion else 'Depósito recibido',
                'fecha': '30 Mar 2026',
                'monto': f'+${monto:,.0f}'.replace(',', '.'),
                'clase': 'positive',
            })
            request.session['historial'] = historial
            request.session.modified = True

            messages.success(request, f'¡Depósito de ${monto:,.0f} realizado con éxito!'.replace(',', '.'))
            return redirect('wallet:depositar')

        except (ValueError, TypeError):
            messages.error(request, 'Monto inválido.')
            return redirect('wallet:depositar')

    saldo = request.session['saldo']
    contexto = {
        'titulo': 'Depositar',
        'saldo': f'${saldo:,.0f}'.replace(',', '.'),
    }
    return render(request, 'wallet/depositar.html', contexto)


def transferir(request):
    """Vista de transferencia de dinero."""
    if 'saldo' not in request.session:
        request.session['saldo'] = 60000

    contactos = [
        {'iniciales': 'MG', 'nombre': 'María García', 'email': 'maria@correo.com', 'color': 'green'},
        {'iniciales': 'JP', 'nombre': 'Juan Pérez', 'email': 'juan@correo.com', 'color': 'blue'},
        {'iniciales': 'AL', 'nombre': 'Ana López', 'email': 'ana@correo.com', 'color': 'orange'},
        {'iniciales': 'CR', 'nombre': 'Carlos Ruiz', 'email': 'carlos@correo.com', 'color': 'pink'},
    ]

    if request.method == 'POST':
        try:
            monto = int(request.POST.get('monto', 0))
            contacto = request.POST.get('contacto', '')

            if monto <= 0:
                messages.error(request, 'Ingresa un monto válido.')
                return redirect('wallet:transferir')

            if not contacto:
                messages.error(request, 'Selecciona un destinatario.')
                return redirect('wallet:transferir')

            saldo_actual = request.session.get('saldo', 60000)
            if monto > saldo_actual:
                messages.error(request, 'Saldo insuficiente para esta transferencia.')
                return redirect('wallet:transferir')

            # Descontar saldo
            request.session['saldo'] = saldo_actual - monto

            # Agregar al historial
            historial = request.session.get('historial', [])
            historial.insert(0, {
                'tipo': 'transfer',
                'titulo': f'Transferencia a {contacto}',
                'fecha': '30 Mar 2026',
                'monto': f'-${monto:,.0f}'.replace(',', '.'),
                'clase': 'negative',
            })
            request.session['historial'] = historial
            request.session.modified = True

            messages.success(request, f'¡Transferencia de ${monto:,.0f} a {contacto} realizada con éxito!'.replace(',', '.'))
            return redirect('wallet:transferir')

        except (ValueError, TypeError):
            messages.error(request, 'Error en la transferencia.')
            return redirect('wallet:transferir')

    saldo = request.session['saldo']
    contexto = {
        'titulo': 'Transferir',
        'saldo': f'${saldo:,.0f}'.replace(',', '.'),
        'contactos': contactos,
    }
    return render(request, 'wallet/transferir.html', contexto)


def transacciones(request):
    """Vista del historial de transacciones."""
    if 'historial' not in request.session:
        request.session['historial'] = [
            {'tipo': 'income', 'titulo': 'Depósito recibido', 'fecha': '28 Mar 2026', 'monto': '+$15.000', 'clase': 'positive'},
            {'tipo': 'expense', 'titulo': 'Pago de servicios', 'fecha': '27 Mar 2026', 'monto': '-$8.500', 'clase': 'negative'},
            {'tipo': 'transfer', 'titulo': 'Transferencia a María', 'fecha': '26 Mar 2026', 'monto': '-$12.000', 'clase': 'negative'},
            {'tipo': 'income', 'titulo': 'Sueldo mensual', 'fecha': '25 Mar 2026', 'monto': '+$450.000', 'clase': 'positive'},
            {'tipo': 'expense', 'titulo': 'Compra online', 'fecha': '24 Mar 2026', 'monto': '-$22.990', 'clase': 'negative'},
            {'tipo': 'transfer', 'titulo': 'Transferencia de Pedro', 'fecha': '23 Mar 2026', 'monto': '+$5.000', 'clase': 'positive'},
        ]

    contexto = {
        'titulo': 'Transacciones',
        'transacciones': request.session['historial'],
    }
    return render(request, 'wallet/transacciones.html', contexto)


def perfil(request):
    """Vista del perfil del usuario."""
    contexto = {
        'titulo': 'Mi Perfil',
        'usuario': {
            'nombre': 'Usuario Demo',
            'email': 'usuario@alkewallet.com',
            'telefono': '+56 9 1234 5678',
            'miembro_desde': 'Enero 2026',
        },
    }
    return render(request, 'wallet/perfil.html', contexto)
