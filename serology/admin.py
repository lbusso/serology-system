from django.contrib import admin, messages
from .models import Enfermedad, TipoAnalisis, Paciente, Pedido, Analisis, PerfilPedido
from django.utils.html import format_html
from django.http import HttpResponse, JsonResponse
from django.urls import path, reverse
from .filter import FechaRapidaFilter
from django.shortcuts import get_object_or_404, redirect, render

from django.views.decorators.csrf import csrf_exempt

# Filtro rápido de fechas (ya lo tenías)
import datetime
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.db.models import Count

# -------------------------------
# Inline de Analisis para Pedido
# -------------------------------
class AnalisisInline(admin.TabularInline):
    model = Analisis
    extra = 1  # cuántos formularios vacíos mostrar
    fields = ("tipo_analisis", "estado")  # solo mostrar lo necesario
    show_change_link = True  # permite abrir el analisis en detalle
    template = "admin/serology/pedido/analisis_inline.html"

# -------------------------------
# Registro de modelos
# -------------------------------
@admin.register(Enfermedad)
class EnfermedadAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)

@admin.register(TipoAnalisis)
class TipoAnalisisAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "enfermedad")
    list_filter = ("enfermedad",)
    search_fields = ("nombre",)

@admin.register(PerfilPedido)
class PerfilPedidoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)
    filter_horizontal = ("tipos_analisis",)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("dni", "apellido", "nombre", "edad", "fecha_nacimiento", "sexo")
    search_fields = ("dni", "apellido", "nombre")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    change_form_template = "admin/serology/pedido/change_form.html"
    fieldsets = (
        (None, {"fields": ("protocolo", "paciente", "medico", "diagnostico", "fecha", "impreso", "es_urgente", "estado")}),
        ("Perfil", {"fields": ("perfil",), "description": "Selecciona un perfil para precargar analisis."}),
    )
    list_display = (
        "protocolo",
        "paciente",
        "medico",
        "estado",
        "es_urgente",
        "fecha",
        "impreso",
        "imprimir_informe_btn",
        "imprimir_hiv_btn",
    )
    readonly_fields = ("estado",)
    list_filter = ("protocolo","estado", "es_urgente", ("fecha", DateRangeFilter), FechaRapidaFilter, "diagnostico")
    inlines = (AnalisisInline, )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        pedido = form.instance
        if change:
            return
        if pedido.perfil is None:
            return
        if pedido.analisis.exists():
            return
        tipos = list(pedido.perfil.tipos_analisis.all())
        if not tipos:
            return
        Analisis.objects.bulk_create(
            [Analisis(pedido=pedido, tipo_analisis=tipo, resultado="") for tipo in tipos]
        )

    # --- Botón imprimir que abre modal ---
    def imprimir_informe_btn(self, obj):
        if obj.estado == "finalizado":
            url = reverse("admin:serology"
                          "_"
                          "pedido_imprimir", args=[obj.pk])
            return format_html(
                '''
                <a class="button btn btn-info" href="#" onclick="abrir_modal_informe('{}', {})">
                    🖨️ Imprimir
                </a>
                ''',
                url,
                obj.pk,
            )
        return "-"
    imprimir_informe_btn.short_description = "Imprimir informe"

    def imprimir_hiv_btn(self, obj):
        if obj.estado != "finalizado" or not obj.analisis_hiv().exists():
            return "-"
        url = reverse("admin:serology"
                      "_"
                      "pedido_imprimir_hiv", args=[obj.pk])
        return format_html(
            '''
            <a class="button btn btn-warning" href="#" onclick="abrir_modal_informe('{}', {})">
                Imprimir HIV
            </a>
            ''',
            url,
            obj.pk,
        )
    imprimir_hiv_btn.short_description = "Imprimir HIV"

    # --- URLs personalizadas ---
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # Vista HTML del informe
            path(
                "<int:pedido_id>/imprimir/",
                self.admin_site.admin_view(self.imprimir_informe),
                name="serology_pedido_imprimir",
            ),
            path(
                "<int:pedido_id>/imprimir_hiv/",
                self.admin_site.admin_view(self.imprimir_informe_hiv),
                name="serology_pedido_imprimir_hiv",
            ),
            # Endpoint AJAX para marcar impreso
            path(
                "<int:pedido_id>/marcar_impreso/",
                self.admin_site.admin_view(self.marcar_impreso),
                name="serolog_pedido_marcar_impreso",
            ),
        ]
        return custom_urls + urls

    # Acción de confirmar impresión
    def confirmar_impresion(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        pedido.impreso = True
        pedido.save()
        self.message_user(request, f"El pedido {pedido.id} fue marcado como impreso ✅", messages.SUCCESS)
        return redirect("..")  # vuelve al changelist

    def imprimir_informe(self, request, pedido_id):
        pedido = Pedido.objects.get(pk=pedido_id)
        html = pedido.generar_informe()
        return HttpResponse(html)

    def imprimir_informe_hiv(self, request, pedido_id):
        pedido = Pedido.objects.get(pk=pedido_id)
        if not pedido.analisis_hiv().exists():
            self.message_user(request, "El pedido no tiene analisis HIV.", messages.WARNING)
            return redirect("admin:serology_pedido_change", pedido_id)
        if not pedido.paciente.sexo:
            self.message_user(
                request,
                "El paciente no tiene sexo registrado. Actualice el paciente antes de imprimir HIV.",
                messages.ERROR,
            )
            return redirect("admin:serology_paciente_change", pedido.paciente_id)
        html = pedido.generar_informe_hiv()
        return HttpResponse(html)

    @csrf_exempt
    def marcar_impreso(self, request, pedido_id):
        if request.method == "POST":
            pedido = Pedido.objects.get(pk=pedido_id)
            pedido.impreso = True
            pedido.save(update_fields=["impreso"])
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    # --- JS y CSS ---
    class Media:
        js = ('js/admin_modal_imprimir.js',)
        css = {
            'all': ('css/admin_modal_imprimir.css',)
        }




class FechaRapidaFilter(admin.SimpleListFilter):
    title = _('Fecha rápida')
    parameter_name = 'fecha_rapida'

    def lookups(self, request, model_admin):
        return [
            ('hoy', _('Hoy')),
            ('este_mes', _('Este mes')),
            ('mes_pasado', _('Mes pasado')),
        ]

    def queryset(self, request, queryset):
        hoy = datetime.date.today()
        if self.value() == 'hoy':
            return queryset.filter(fecha=hoy)
        if self.value() == 'este_mes':
            return queryset.filter(fecha__year=hoy.year, fecha__month=hoy.month)
        if self.value() == 'mes_pasado':
            primer_dia_mes = hoy.replace(day=1)
            mes_pasado = primer_dia_mes - datetime.timedelta(days=1)
            return queryset.filter(fecha__year=mes_pasado.year, fecha__month=mes_pasado.month)
        return queryset

# Admin
@admin.register(Analisis)
class AnalisisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido__protocolo",
        "pedido",
        "tipo_analisis",
        "estado_coloreado",
        "fecha",
        "es_urgente_icono",   # reemplaza el campo original
    )
    list_filter = (
        "pedido__protocolo",
        "estado",
        "tipo_analisis",
        ("fecha", DateRangeFilter),
        FechaRapidaFilter,
        "resultado",
        "pedido__es_urgente",
    )
    search_fields = (
        "pedido__paciente__apellido",
        "pedido__paciente__dni",
        "tipo_analisis__nombre",
        "pedido__protocolo",
        "resultado",
    )
    actions = ["marcar_en_progreso"]
    change_list_template = "admin/serology/analisis/change_list.html"

    # Estado coloreado
    def estado_coloreado(self, obj):
        color_map = {
            "pendiente": "#f0ad4e",
            "en_proceso": "#5bc0de",
            "finalizado": "#5cb85c",
        }
        color = color_map.get(obj.estado, "#777")
        return format_html(
            '<span style="color: white; background-color: {}; padding: 4px 8px; border-radius: 6px; font-size: 12px;">{}</span>',
            color,
            obj.get_estado_display(),
        )
    estado_coloreado.short_description = "Estado"

    # Booleano pedido__es_urgente como icono
    def es_urgente_icono(self, obj):
        if obj.pedido.es_urgente:
            return format_html('<span class="icon-tick"></span>')
        return format_html('<span class="icon-cross"></span>')
    es_urgente_icono.short_description = "Urgente"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "estadisticas/",
                self.admin_site.admin_view(self.estadisticas_view),
                name="serology_analisis_estadisticas",
            ),
        ]
        return custom_urls + urls

    def estadisticas_view(self, request):
        por_tipo = (
            Analisis.objects
            .values("tipo_analisis__nombre")
            .annotate(total=Count("id"))
            .order_by("tipo_analisis__nombre")
        )
        labels = [row["tipo_analisis__nombre"] for row in por_tipo]
        data = [row["total"] for row in por_tipo]

        por_estado = (
            Analisis.objects
            .values("estado")
            .annotate(total=Count("id"))
            .order_by("estado")
        )
        estados_field = Analisis._meta.get_field("estado")
        estados_map = dict(estados_field.choices)
        estados_labels = [estados_map.get(row["estado"], row["estado"]) for row in por_estado]
        estados_data = [row["total"] for row in por_estado]

        context = dict(
            self.admin_site.each_context(request),
            title="Estadísticas de Análisis",
            labels=labels,
            data=data,
            estados_labels=estados_labels,
            estados_data=estados_data,
            opts=Analisis._meta,
            app_label=Analisis._meta.app_label,
        )
        return render(request, "admin/serology/analisis/estadisticas.html", context)

    # Acción para marcar en progreso
    def marcar_en_progreso(self, request, queryset):
        updated = queryset.update(estado="en_proceso")
        self.message_user(request, f"{updated} análisis fueron marcados como 'En progreso'.")
    marcar_en_progreso.short_description = "Marcar análisis seleccionados como 'En progreso'"
