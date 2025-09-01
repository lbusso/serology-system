# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Pacientes
    path("pacientes/", PacienteListView.as_view(), name="paciente_list"),
    path("pacientes/<int:pk>/", PacienteDetailView.as_view(), name="paciente_detail"),
    path("pacientes/nuevo/", PacienteCreateView.as_view(), name="paciente_create"),
    path("pacientes/<int:pk>/editar/", PacienteUpdateView.as_view(), name="paciente_update"),
    path("pacientes/<int:pk>/eliminar/", PacienteDeleteView.as_view(), name="paciente_delete"),

    # Enfermedades
    path("enfermedades/", EnfermedadListView.as_view(), name="enfermedad_list"),
    path("enfermedades/nueva/", EnfermedadCreateView.as_view(), name="enfermedad_create"),
    path("enfermedades/<int:pk>/editar/", EnfermedadUpdateView.as_view(), name="enfermedad_update"),
    path("enfermedades/<int:pk>/eliminar/", EnfermedadDeleteView.as_view(), name="enfermedad_delete"),

    # Tipos de Análisis
    path("tipos-analisis/", TipoAnalisisListView.as_view(), name="tipoanalisis_list"),
    path("tipos-analisis/nuevo/", TipoAnalisisCreateView.as_view(), name="tipoanalisis_create"),
    path("tipos-analisis/<int:pk>/editar/", TipoAnalisisUpdateView.as_view(), name="tipoanalisis_update"),
    path("tipos-analisis/<int:pk>/eliminar/", TipoAnalisisDeleteView.as_view(), name="tipoanalisis_delete"),

    # Pedidos
    path("pedidos/", PedidoListView.as_view(), name="pedido_list"),
    path("pedidos/nuevo/", PedidoCreateView.as_view(), name="pedido_create"),
    path("pedidos/<int:pk>/editar/", PedidoUpdateView.as_view(), name="pedido_update"),
    path("pedidos/<int:pk>/eliminar/", PedidoDeleteView.as_view(), name="pedido_delete"),

    # Análisis
    path("analisis/", AnalisisListView.as_view(), name="analisis_list"),
    path("analisis/nuevo/", AnalisisCreateView.as_view(), name="analisis_create"),
    path("analisis/<int:pk>/editar/", AnalisisUpdateView.as_view(), name="analisis_update"),
    path("analisis/<int:pk>/eliminar/", AnalisisDeleteView.as_view(), name="analisis_delete"),
]
