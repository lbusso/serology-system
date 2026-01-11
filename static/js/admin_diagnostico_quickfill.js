// Agrega botones para completar rapidamente el diagnostico en pedidos
(function () {
    function getQuickfillData() {
        var script = document.getElementById("diagnostico-quickfill");
        if (!script) {
            return [];
        }
        try {
            return JSON.parse(script.textContent);
        } catch (err) {
            return [];
        }
    }

    function addQuickFillButtons() {
        var field = document.getElementById("id_diagnostico");
        if (!field) {
            return;
        }
        if (document.getElementById("diagnostico_quickfill")) {
            return;
        }

        var data = getQuickfillData();
        if (!data.length) {
            return;
        }

        var container = document.createElement("div");
        container.id = "diagnostico_quickfill";
        container.style.marginBottom = "8px";

        function createButton(label, text) {
            var btn = document.createElement("button");
            btn.type = "button";
            btn.className = "button";
            btn.style.marginRight = "6px";
            btn.textContent = label;
            btn.addEventListener("click", function () {
                var current = field.value || "";
                if (current.trim() === "") {
                    field.value = text;
                } else {
                    field.value = current + " " + text;
                }
                field.focus();
            });
            return btn;
        }

        for (var i = 0; i < data.length; i++) {
            var item = data[i] || {};
            if (!item.label || !item.texto) {
                continue;
            }
            container.appendChild(createButton(item.label, item.texto));
        }

        if (!container.children.length) {
            return;
        }

        field.parentNode.insertBefore(container, field);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", addQuickFillButtons);
    } else {
        addQuickFillButtons();
    }
})();
