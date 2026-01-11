import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib import admin


class FechaRapidaFilter(admin.SimpleListFilter):
    title = _("Fecha rápida")
    parameter_name = "fecha_rapida"

    def lookups(self, request, model_admin):
        return [
            ("hoy", _("Hoy")),
            ("este_mes", _("Este mes")),
            ("mes_pasado", _("Mes pasado")),
        ]

    def queryset(self, request, queryset):
        hoy = datetime.date.today()
        if self.value() == "hoy":
            return queryset.filter(fecha=hoy)
        if self.value() == "este_mes":
            return queryset.filter(fecha__year=hoy.year, fecha__month=hoy.month)
        if self.value() == "mes_pasado":
            primer_dia_mes = hoy.replace(day=1)
            mes_pasado = primer_dia_mes - datetime.timedelta(days=1)
            return queryset.filter(
                fecha__year=mes_pasado.year, fecha__month=mes_pasado.month
            )
        return queryset
