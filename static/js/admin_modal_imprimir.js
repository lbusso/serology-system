// Función para abrir modal con el informe
function abrir_modal_informe(url, pedido_id) {
    // Crear modal si no existe
    if (!document.getElementById('modal_informe')) {
        const modal = document.createElement('div');
        modal.id = 'modal_informe';
        modal.className = 'modal_informe';
        modal.innerHTML = `
            <div class="modal_content">
                <span class="modal_close" onclick="cerrar_modal()">&times;</span>
                <iframe id="iframe_informe" style="width:100%; height:70vh; border:1px solid #ddd; border-radius:8px;"></iframe>
                <div class="modal_buttons">
                    <button class="btn btn-info" onclick="imprimir_informe()">
                        🖨️ Imprimir
                    </button>
                    <button class="btn btn-success" onclick="confirmar_impresion(${pedido_id})">
                        ✅ Confirmar impresión
                    </button>
                    <button class="btn btn-secondary" onclick="cerrar_modal()">
                        ❌ Cerrar
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    // Abrir modal y cargar iframe
    document.getElementById('modal_informe').style.display = 'block';
    document.getElementById('iframe_informe').src = url;
}

// Cerrar modal
function cerrar_modal() {
    document.getElementById('modal_informe').style.display = 'none';
}

// Imprimir informe desde iframe
function imprimir_informe() {
    const iframe = document.getElementById('iframe_informe');
    iframe.contentWindow.focus();
    iframe.contentWindow.print();
}

// Confirmar impresión
function confirmar_impresion(pedido_id) {
    fetch(`/admin/serology/pedido/${pedido_id}/marcar_impreso/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    }).then(response => {
        if (response.ok) {
            alert("Pedido marcado como impreso ✅");
            cerrar_modal();
            location.reload();
        } else {
            alert("Error al marcar el pedido como impreso");
        }
    });
}

// Función CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
