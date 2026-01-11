// Agrega botones para completar rapidamente el resultado del analisis
(function () {
    function addQuickFillButtons() {
        var field = document.getElementById("id_resultado");
        if (!field) {
            return;
        }
        if (document.getElementById("resultado_quickfill")) {
            return;
        }

        var container = document.createElement("div");
        container.id = "resultado_quickfill";
        container.style.marginBottom = "8px";

        function createButton(label) {
            var btn = document.createElement("button");
            btn.type = "button";
            btn.className = "button";
            btn.style.marginRight = "6px";
            btn.textContent = label;
            btn.addEventListener("click", function () {
                var current = field.value || "";
                if (current.trim() === "") {
                    field.value = label;
                } else {
                    field.value = current + " " + label;
                }
                field.focus();
            });
            return btn;
        }

        container.appendChild(createButton("REACTIVO"));
        container.appendChild(createButton("NO REACTIVO"));

        field.parentNode.insertBefore(container, field);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", addQuickFillButtons);
    } else {
        addQuickFillButtons();
    }
})();
