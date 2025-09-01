function confirmar_impresion(pedido_id) {
    var confirmado = confirm("¿Se imprimió el pedido correctamente?");
    if (confirmado) {
        fetch(`/admin/lab/pedido/${pedido_id}/marcar_impreso/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        }).then(response => {
            if(response.ok){
                alert("Pedido marcado como impreso ✅");
                location.reload(); // recarga el admin para reflejar el cambio
            } else {
                alert("Error al marcar el pedido como impreso");
            }
        });
    }
    return false; // evita que la pestaña se abra inmediatamente
}

// Función para obtener CSRF
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
