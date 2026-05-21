// Mapa de sonidos por nombre de categoría (rutas)
const SONIDO_CAIDA = '/static/audio/1.mp3';

const sonidoYaEmitido = {};

// Categorías para las que ya se emitió sonido
const sonidosEmitidos = new Set();
let sonidosActivos = false;
let fallosConsecutivos = {};

// Estado previo de todos los servidores { 'nombreServidor': 'Online'|'Offline' }
let estadoPrevioServidores = {};

// Precargar audios tras interacción usuario
function activarSonidos() {
    Object.values(sonidosPorCategoria).forEach(ruta => {
        const audio = new Audio(ruta);
        audio.play().then(() => {
            audio.pause();
            audio.currentTime = 0;
        }).catch(() => {
            console.warn('Autoplay bloqueado. Se necesita interacción del usuario.');
        });
    });
}

// Reproducir sonido X veces manteniendo objeto Audio
function reproducirSonidoRepetidoDesdeRuta(ruta, repeticiones = 3) {
    let contador = 0;
    const audio = new Audio(ruta);

    audio.addEventListener('ended', () => {
        contador++;
        if (contador < repeticiones) {
            audio.currentTime = 0;
            audio.play().catch(e => console.warn('No se pudo reproducir:', e));
        }
    });

    audio.play().catch(e => console.warn('No se pudo reproducir:', e));
}

let modalServidor = null;

function abrirModal() {
    const modalEl = document.getElementById('modal-servidor');

    if (!modalServidor) {
        modalServidor = new bootstrap.Modal(modalEl, {
            backdrop: 'static',
            keyboard: true
        });
    }

    modalServidor.show();
}

function cerrarModal() {
    if (modalServidor) {
        modalServidor.hide();
    }
}


function enviarReporte() {
    const form = document.getElementById('form-reporte');
    const formData = new FormData(form);

    fetch('/gestion/api/guardar_reporte/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
        body: formData
    })
    .then(res => {
        if (!res.ok) throw new Error('Error al guardar');
        return res.json();
    })
    .then(data => {
        cerrarModal();
        alert('Reporte creado correctamente');
        form.reset();
        cerrarModal();
    })
    .catch(err => {
        console.error(err);
        alert('Error al guardar el reporte');
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

const MAX_FALLOS = 3;
const form = document.getElementById('form-reporte');

// En panel.js, actualizar la función actualizarEstados():

function actualizarEstados() {
    fetch('/panel/ping-status/')
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById('servidores');
            const timestamp = document.getElementById('ultima-actualizacion');
            const onlineCount = document.getElementById('online-count');
            const offlineCount = document.getElementById('offline-count');
            const errorMessage = document.getElementById('error-message');

            const now = new Date();
            const timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            timestamp.textContent = `Actualizado: ${timeStr}`;

            let online = 0;
            let offline = 0;
            let contenidoHTML = '';

            const categoriasConCaidaNueva = new Set();

            for (const categoria in data) {
                const servidores = data[categoria];
                const categoriaCount = servidores.length;
                
                // Contar servidores por estado en esta categoría
                let catOnline = 0;
                let catOffline = 0;
                
                // Crear HTML de tarjetas para esta categoría
                let tarjetasHTML = '';
                
                servidores.forEach(servidor => {
                    const nombre = servidor.nombre;
                    const responde = servidor.status === 'Online';

                    if (!(nombre in fallosConsecutivos)) {
                        fallosConsecutivos[nombre] = 0;
                    }

                    if (responde) {
                        fallosConsecutivos[nombre] = 0;
                    } else {
                        fallosConsecutivos[nombre]++;
                    }

                    let estado, estadoClass, statusClass;
                    
                    if (fallosConsecutivos[nombre] === 0) {
                        estado = 'ON';
                        estadoClass = 'online';
                        statusClass = 'status-online';
                        catOnline++;
                        online++;
                    } else if (fallosConsecutivos[nombre] <= 2) {
                        estado = 'INS';
                        estadoClass = 'inestable';
                        statusClass = 'status-inestable';
                        catOnline++;
                        online++;
                    } else if (fallosConsecutivos[nombre] <= 6) {
                        estado = 'DEG';
                        estadoClass = 'degradado';
                        statusClass = 'status-degradado';
                        catOnline++;
                        online++;
                    } else {
                        estado = 'OFF';
                        estadoClass = 'offline';
                        statusClass = 'status-offline';
                        catOffline++;
                        offline++;
                    }

                    const estadoPrevio = estadoPrevioServidores[nombre];

                    // 🔊 detectar caída real
                    if (sonidosActivos) {

                    // 🟢 Si ya NO está OFF, liberamos el bloqueo
                    if (estado !== 'OFF') {
                        sonidoYaEmitido[nombre] = false;
                    }

                    // 🔴 Solo cuando ENTRA a OFF
                    if (
                        estado === 'OFF' &&
                        estadoPrevio !== 'OFF' &&
                        !sonidoYaEmitido[nombre]
                    ) {
                            reproducirSonidoRepetidoDesdeRuta('/static/audio/1.mp3', 2);
                            sonidoYaEmitido[nombre] = true;

                            console.log(`🔊 Sonido único por caída: ${nombre}`);
                        }
                    }

                    estadoPrevioServidores[nombre] = estado;



                    // Crear tarjeta compacta
                    const puertoHTML = servidor.puerto
                    ? `<div><strong>Puerto:</strong> ${servidor.puerto}</div>`
                    : "";

                    tarjetasHTML += `
                        <div class="server-card small ${estadoClass}"
                            data-ip="${servidor.ip}"
                            data-nombre="${servidor.nombre}"
                            data-bs-toggle="tooltip"
                            data-bs-html="true"
                            data-bs-title="
                                <div style='min-width:140px'>
                                    <div><strong>IP:</strong> ${servidor.ip}</div>
                                    ${puertoHTML}
                                </div>
                            "
                            onclick="cargarServidor('${servidor.ip}')">

                            <span class="server-name">${nombre}</span>
                            <span class="status-dot-mini">
                                ${
                                    estado === 'ON' ? '🟢' :
                                    estado === 'INS' ? '🟡' :
                                    estado === 'DEG' ? '🟠' :
                                    '🔴'
                                }
                            </span>
                        </div>
                    `;




                });

                // Agregar sección de categoría
                contenidoHTML += `
                    <div class="category-section">
                        <div class="category-header">
                            <span>${categoria}</span>
                            <span class="category-count">${catOnline}/${catOnline + catOffline}</span>
                        </div>
                        <div class="server-grid">
                            ${tarjetasHTML}
                        </div>
                    </div>
                `;
            }

            // Actualizar contenido
            contenedor.innerHTML = contenidoHTML;

            const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltipTriggerList.forEach(el => {
                new bootstrap.Tooltip(el);
            });

            // Actualizar contadores
            onlineCount.textContent = online;
            offlineCount.textContent = offline;

            // Ocultar mensaje de error
            if (errorMessage) {
                errorMessage.classList.add('d-none');
            }

        })
        .catch(error => {
            console.error('Error al obtener estados:', error);
            const errorMessage = document.getElementById('error-message');
            if (errorMessage) {
                errorMessage.classList.remove('d-none');
            }
        });
}

// Función auxiliar para cargar servidor
function cargarServidor(ip) {
    const encodedIp = encodeURIComponent(ip);
    const form = document.getElementById('form-reporte');

    fetch(`/gestion/api/servidor/${encodedIp}/`)
        .then(res => {
            if (!res.ok) throw new Error('No encontrado');
            return res.json();
        })
        .then(data => {
            form.nombre.value = data.nombre ?? '';
            form.ip.value = data.ip ?? '';
            form.enlace.value = data.servicio ?? '';
            
            // Select ¿Qué cayó?
            const select = document.getElementById('que_cayo');
            select.innerHTML = '<option value="">Selecciona una opción</option>';

            if (data.referencia) {
                const opt1 = document.createElement('option');
                opt1.value = data.referencia;
                opt1.textContent = "Ref. Enlace - " + data.referencia;
                select.appendChild(opt1);
            }

            if (data.referencia2) {
                const opt2 = document.createElement('option');
                opt2.value = data.referencia2;
                opt2.textContent = "Ref. TKS - " + data.referencia2;
                select.appendChild(opt2);
            }

            abrirModal();
        })
        .catch(err => {
            console.error('Error cargando servidor:', err);
            showAlert('Error cargando servidor', 'danger');
        });
}

document.getElementById('form-conexion')?.addEventListener('submit', e => {
    console.log('Registrando evento de conexión/desconexión...');
    e.preventDefault();
    fetch('/panel/registrar-evento/', {
        method: 'POST',
        body: new FormData(e.target),
        headers: { 'X-CSRFToken': getCSRFToken() }
    }).then(() => cerrarModal());
});


// Al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const switchSonido = document.getElementById('activar-sonidos');

    // 🔊 Audio global
    const audioAlerta = document.getElementById('sonido-alerta');

    // 🔁 Cargar preferencia guardada
    const guardado = localStorage.getItem('sonidosActivos');
    if (guardado === 'true' && switchSonido) {
        switchSonido.checked = true;

        // intento de desbloqueo (solo funcionará si ya hubo interacción antes)
        audioAlerta.play().then(() => {
            audioAlerta.pause();
            audioAlerta.currentTime = 0;
            sonidosActivos = true;
        }).catch(() => {});
    }

    // 🎚️ Escuchar cambio del switch
    if (switchSonido) {
        switchSonido.addEventListener('change', (e) => {
            sonidosActivos = e.target.checked;
            localStorage.setItem('sonidosActivos', sonidosActivos);

            if (sonidosActivos) {
                // 🔓 desbloqueo REAL del audio
                audioAlerta.play().then(() => {
                    audioAlerta.pause();
                    audioAlerta.currentTime = 0;
                    console.log('🔊 Sonidos activados');
                }).catch(err => {
                    console.warn('No se pudo activar el audio:', err);
                });
            } else {
                console.log('🔇 Sonidos desactivados');
            }
        });
    }

    // 📩 Formulario
    if (form){
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            enviarReporte();
        });

        document.getElementById('cerrar-modal')
            ?.addEventListener('click', cerrarModal);
    }

    actualizarEstados();
    setInterval(actualizarEstados, 5000);
});