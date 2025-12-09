// ========================================
// WALLET APP - JavaScript con jQuery
// ========================================

// Lista de transacciones para filtrar
const listaTransacciones = [
  { tipo: 'compra', descripcion: 'Compra en linea', monto: 50, fecha: '08/12/2024' },
  { tipo: 'deposito', descripcion: 'Deposito', monto: 100, fecha: '07/12/2024' },
  { tipo: 'transferencia', descripcion: 'Transferencia recibida', monto: 75, fecha: '06/12/2024' },
  { tipo: 'compra', descripcion: 'Compra tienda', monto: 5550, fecha: '05/12/2024' },
  { tipo: 'deposito', descripcion: 'Deposito misma cuenta', monto: 10500, fecha: '04/12/2024' },
  { tipo: 'transferencia', descripcion: 'Transferencia recibida', monto: 7575, fecha: '03/12/2024' }
];

// Inicializar datos en localStorage
function inicializarDatos() {
  if (!localStorage.getItem('walletSaldo')) {
    localStorage.setItem('walletSaldo', '60000');
  }
  if (!localStorage.getItem('walletMovimientos')) {
    localStorage.setItem('walletMovimientos', JSON.stringify(listaTransacciones));
  }
  if (!localStorage.getItem('walletContactos')) {
    const contactosIniciales = [
      { nombre: 'John Doe', cbu: '1234567890123456789012', alias: 'john.doe', banco: 'ABC Bank' },
      { nombre: 'Jane Smith', cbu: '9876543210987654321098', alias: 'jane.smith', banco: 'XYZ Bank' }
    ];
    localStorage.setItem('walletContactos', JSON.stringify(contactosIniciales));
  }
}

// Funciones de localStorage
function getSaldo() {
  return parseFloat(localStorage.getItem('walletSaldo')) || 60000;
}

function setSaldo(saldo) {
  localStorage.setItem('walletSaldo', saldo.toString());
}

function formatearMonto(monto) {
  return '$' + monto.toLocaleString('es-CL');
}

function getMovimientos() {
  const data = localStorage.getItem('walletMovimientos');
  return data ? JSON.parse(data) : [];
}

function agregarMovimiento(tipo, descripcion, monto) {
  const movimientos = getMovimientos();
  const fecha = new Date().toLocaleDateString('es-CL');
  movimientos.unshift({ tipo, descripcion, monto, fecha });
  localStorage.setItem('walletMovimientos', JSON.stringify(movimientos));
}

function getContactos() {
  const data = localStorage.getItem('walletContactos');
  return data ? JSON.parse(data) : [];
}

function agregarContacto(nombre, cbu, alias, banco) {
  const contactos = getContactos();
  contactos.push({ nombre, cbu, alias, banco });
  localStorage.setItem('walletContactos', JSON.stringify(contactos));
}

// Obtener tipo de transaccion legible
function getTipoTransaccion(tipo) {
  const tipos = {
    'compra': 'Compra',
    'deposito': 'Deposito',
    'transferencia': 'Transferencia recibida'
  };
  return tipos[tipo] || tipo;
}

// Mostrar alerta Bootstrap con jQuery
function mostrarAlertaBootstrap(contenedor, tipo, mensaje) {
  const alertClass = tipo === 'success' ? 'alert-success' : 'alert-danger';
  const alerta = $('<div class="alert ' + alertClass + ' alert-dismissible fade show" role="alert">' +
    mensaje +
    '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
    '</div>');
  $(contenedor).html(alerta);
}

// ========================================
// DOCUMENT READY - jQuery
// ========================================
$(document).ready(function() {
  inicializarDatos();
  
  // ========================================
  // LOGIN - Selectores jQuery
  // ========================================
  $('#loginForm').submit(function(e) {
    e.preventDefault();
    
    // Uso de selectores jQuery para obtener valores
    const email = $('#email').val();
    const password = $('#password').val();
    
    // Validar campos vacios
    if (!email || !password) {
      mostrarAlertaBootstrap('#alert-container', 'error', 'Por favor complete todos los campos');
      return false;
    }
    
    // Validar formato email
    if (!email.includes('@')) {
      mostrarAlertaBootstrap('#alert-container', 'error', 'Por favor ingrese un email valido');
      return false;
    }
    
    // Validar contrasena minimo 4 caracteres
    if (password.length < 4) {
      mostrarAlertaBootstrap('#alert-container', 'error', 'La contrasena debe tener al menos 4 caracteres');
      return false;
    }
    
    // Login exitoso - Alerta Bootstrap
    mostrarAlertaBootstrap('#alert-container', 'success', 'Inicio de sesion exitoso! Redirigiendo...');
    
    // Redirigir con jQuery
    setTimeout(function() {
      window.location.href = 'menu.html';
    }, 1500);
    
    return false;
  });
  
  // ========================================
  // MENU PRINCIPAL - Actualizar saldo
  // ========================================
  if ($('#saldo-actual').length) {
    $('#saldo-actual').text(formatearMonto(getSaldo()));
  }
  
  // Actualizar stats total
  if ($('#stats-total').length) {
    $('#stats-total').text(formatearMonto(getSaldo()));
  }
  
  // Cargar ultimos movimientos en dashboard
  if ($('#ultimos-movimientos').length) {
    mostrarMovimientosDashboard();
  }
  
  // ========================================
  // DEPOSITO - Mostrar saldo y procesar
  // ========================================
  if ($('#saldo-deposito').length) {
    $('#saldo-deposito').text(formatearMonto(getSaldo()));
  }
  
  $('#formDeposito').submit(function(e) {
    e.preventDefault();
    
    const monto = parseFloat($('#monto-deposito').val());
    
    if (isNaN(monto) || monto <= 0) {
      mostrarAlertaBootstrap('#alert-container', 'error', 'Por favor ingrese un monto valido mayor a 0');
      return false;
    }
    
    // Actualizar saldo
    const nuevoSaldo = getSaldo() + monto;
    setSaldo(nuevoSaldo);
    
    // Agregar movimiento
    agregarMovimiento('deposito', 'Deposito', monto);
    
    // Mostrar leyenda con monto depositado usando jQuery
    $('#leyenda-deposito').html('<strong>✓ Monto depositado:</strong> ' + formatearMonto(monto)).fadeIn();
    
    // Actualizar display del saldo
    $('#saldo-deposito').text(formatearMonto(nuevoSaldo));
    
    // Mostrar alerta Bootstrap de exito
    mostrarAlertaBootstrap('#alert-container', 'success', 
      'Deposito de ' + formatearMonto(monto) + ' realizado con exito!');
    
    $('#monto-deposito').val('');
    if (typeof clearAmount === 'function') {
      clearAmount();
    }
    
    // Redirigir despues de 2 segundos
    setTimeout(function() {
      window.location.href = 'menu.html';
    }, 2000);
    
    return false;
  });
  
  // ========================================
  // ENVIAR DINERO
  // ========================================
  // Cargar contactos
  cargarContactosJQuery();
  
  // Mostrar saldo
  if ($('#saldo-envio').length) {
    const saldo = getSaldo();
    $('#saldo-envio').text(saldo.toLocaleString('es-CL'));
  }
  
  // Busqueda en agenda de transferencias
  $('#btnBuscar').click(function() {
    const busqueda = $('#buscar-contacto').val().toLowerCase();
    
    $('.contacto-item').each(function() {
      const texto = $(this).text().toLowerCase();
      if (texto.includes(busqueda)) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  });
  
  // Formulario nuevo contacto con validacion
  $('#formNuevoContacto').submit(function(e) {
    e.preventDefault();
    
    const nombre = $('#nuevo-nombre').val().trim();
    const cbu = $('#nuevo-cbu').val().trim();
    const alias = $('#nuevo-alias').val().trim();
    const banco = $('#nuevo-banco').val().trim();
    
    // Validar campos obligatorios
    if (!nombre || !cbu || !alias || !banco) {
      mostrarAlertaBootstrap('#modal-alert', 'error', 'Por favor complete todos los campos');
      return false;
    }
    
    // Validar formato CBU (22 digitos)
    if (!/^\d{22}$/.test(cbu)) {
      mostrarAlertaBootstrap('#modal-alert', 'error', 'El CBU debe tener 22 digitos numericos');
      return false;
    }
    
    // Agregar contacto
    agregarContacto(nombre, cbu, alias, banco);
    
    // Cerrar modal con jQuery/Bootstrap
    $('#modalNuevoContacto').modal('hide');
    
    // Limpiar formulario
    $('#formNuevoContacto')[0].reset();
    $('#modal-alert').html('');
    
    // Recargar contactos
    cargarContactosJQuery();
    
    mostrarAlertaBootstrap('#alert-container', 'success', 'Contacto agregado exitosamente');
    
    return false;
  });
  
  // Boton enviar dinero
  $('#btnEnviarDinero').click(function() {
    const monto = parseFloat($('#monto-envio').val());
    const contacto = $('#contacto-seleccionado').text();
    
    if (!contacto) {
      mostrarAlertaBootstrap('#alert-container', 'error', 'Por favor seleccione un contacto');
      return;
    }
    
    if (isNaN(monto) || monto <= 0) {
      mostrarAlertaBootstrap('#alert-container', 'error', 'Por favor ingrese un monto valido');
      return;
    }
    
    if (monto > getSaldo()) {
      mostrarAlertaBootstrap('#alert-container', 'error', 'Saldo insuficiente');
      return;
    }
    
    // Actualizar saldo
    const nuevoSaldo = getSaldo() - monto;
    setSaldo(nuevoSaldo);
    
    // Agregar movimiento
    agregarMovimiento('compra', 'Transferencia a ' + contacto, monto);
    
    // Actualizar recibo en modal
    $('#recibo-destinatario').text(contacto);
    $('#recibo-monto').text(formatearMonto(monto));
    $('#recibo-fecha').text(new Date().toLocaleDateString('es-CL'));
    
    // Mostrar modal de exito si existe
    if ($('#modalExito').length) {
      $('#modalExito').modal('show');
    } else {
      // Fallback a alerta normal
      mostrarAlertaBootstrap('#alert-container', 'success', 
        'Transferencia de ' + formatearMonto(monto) + ' a ' + contacto + ' realizada con exito!');
      
      setTimeout(function() {
        window.location.href = 'menu.html';
      }, 2000);
    }
    
    $('#saldo-envio').text(nuevoSaldo.toLocaleString('es-CL'));
  });
  
  // ========================================
  // MOVIMIENTOS - Cargar y filtrar
  // ========================================
  if ($('#lista-movimientos').length) {
    mostrarUltimosMovimientos('todos');
    
    // Filtrar por tipo de movimiento
    $('#filtro-tipo').change(function() {
      const filtro = $(this).val();
      mostrarUltimosMovimientos(filtro);
    });
  }
});

// ========================================
// FUNCIONES AUXILIARES
// ========================================

// Cargar contactos con jQuery - Diseño moderno
function cargarContactosJQuery() {
  const $lista = $('#lista-contactos');
  if (!$lista.length) return;
  
  const contactos = getContactos();
  $lista.empty();
  
  const avatarColors = ['', 'green', 'blue', 'orange', 'pink'];
  
  contactos.forEach(function(contacto, index) {
    const colorClass = avatarColors[index % avatarColors.length];
    const inicial = contacto.nombre.charAt(0).toUpperCase();
    
    const $item = $('<div class="contact-item"></div>');
    $item.html(
      '<div class="contact-avatar ' + colorClass + '">' + inicial + '</div>' +
      '<div class="contact-info">' +
        '<div class="contact-name">' + contacto.nombre + '</div>' +
        '<div class="contact-detail">' + contacto.alias + ' • ' + contacto.banco + '</div>' +
      '</div>' +
      '<div class="contact-check"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg></div>'
    );
    
    // Al seleccionar contacto, mostrar formulario de envio
    $item.click(function() {
      $('.contact-item').removeClass('active');
      $(this).addClass('active');
      $('#contacto-seleccionado').text(contacto.nombre);
      $('#avatar-inicial').text(inicial);
      $('.contact-list').hide();
      $('.section-title').hide();
      $('[style*="position: relative"]').hide(); // Ocultar search
      $('#form-envio').fadeIn();
    });
    
    $lista.append($item);
  });
}

// Mostrar ultimos movimientos con filtro por tipo - Diseño moderno
function mostrarUltimosMovimientos(filtro) {
  const $lista = $('#lista-movimientos');
  if (!$lista.length) return;
  
  const movimientos = getMovimientos();
  $lista.empty();
  
  let movimientosFiltrados = movimientos;
  let totalMes = 0;
  
  // Filtrar por tipo si no es 'todos'
  if (filtro !== 'todos') {
    movimientosFiltrados = movimientos.filter(function(mov) {
      return mov.tipo === filtro;
    });
  }
  
  if (movimientosFiltrados.length === 0) {
    $lista.append('<div style="text-align: center; padding: 40px; color: #9CA3AF;">No hay movimientos de este tipo</div>');
    return;
  }
  
  movimientosFiltrados.forEach(function(mov) {
    const esIngreso = mov.tipo === 'deposito' || mov.tipo === 'transferencia';
    const signo = esIngreso ? '+' : '-';
    const amountClass = esIngreso ? 'positive' : 'negative';
    const iconClass = esIngreso ? 'income' : 'expense';
    
    if (esIngreso) {
      totalMes += mov.monto;
    } else {
      totalMes -= mov.monto;
    }
    
    let iconSvg = '';
    if (mov.tipo === 'deposito') {
      iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>';
    } else if (mov.tipo === 'transferencia') {
      iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>';
    } else {
      iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>';
    }
    
    const $item = $('<div class="transaction-item"></div>');
    $item.html(
      '<div class="transaction-icon ' + iconClass + '">' + iconSvg + '</div>' +
      '<div class="transaction-info">' +
        '<div class="transaction-title">' + mov.descripcion + '</div>' +
        '<div class="transaction-date">' + mov.fecha + '</div>' +
      '</div>' +
      '<div class="transaction-amount ' + amountClass + '">' + signo + formatearMonto(mov.monto) + '</div>'
    );
    
    $lista.append($item);
  });
  
  // Actualizar total del mes
  if ($('#total-mes').length) {
    $('#total-mes').text(formatearMonto(Math.abs(totalMes)));
  }
}

// Mostrar ultimos movimientos en el dashboard del menu
function mostrarMovimientosDashboard() {
  const $lista = $('#ultimos-movimientos');
  if (!$lista.length) return;
  
  const movimientos = getMovimientos().slice(0, 3); // Solo los 3 más recientes
  $lista.empty();
  
  if (movimientos.length === 0) {
    $lista.append('<div style="text-align: center; padding: 20px; color: #9CA3AF;">No hay movimientos recientes</div>');
    return;
  }
  
  movimientos.forEach(function(mov) {
    const esIngreso = mov.tipo === 'deposito' || mov.tipo === 'transferencia';
    const signo = esIngreso ? '+' : '-';
    const amountClass = esIngreso ? 'positive' : 'negative';
    const iconClass = esIngreso ? 'income' : 'expense';
    
    let iconSvg = '';
    if (mov.tipo === 'deposito') {
      iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>';
    } else if (mov.tipo === 'transferencia') {
      iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>';
    } else {
      iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>';
    }
    
    const $item = $('<div class="transaction-item"></div>');
    $item.html(
      '<div class="transaction-icon ' + iconClass + '">' + iconSvg + '</div>' +
      '<div class="transaction-info">' +
        '<div class="transaction-title">' + mov.descripcion + '</div>' +
        '<div class="transaction-date">' + mov.fecha + '</div>' +
      '</div>' +
      '<div class="transaction-amount ' + amountClass + '">' + signo + formatearMonto(mov.monto) + '</div>'
    );
    
    $lista.append($item);
  });
}
