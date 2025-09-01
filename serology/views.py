# views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Paciente, Enfermedad, TipoAnalisis, Pedido, Analisis

# -------------------
# Paciente
# -------------------
class PacienteListView(ListView):
    model = Paciente
    template_name = "pacientes/lista.html"
    context_object_name = "pacientes"

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = "pacientes/detalle.html"
    context_object_name = "paciente"

class PacienteCreateView(CreateView):
    model = Paciente
    fields = ["dni", "apellido", "nombre", "fecha_nacimiento"]
    template_name = "pacientes/form.html"
    success_url = reverse_lazy("paciente_list")

class PacienteUpdateView(UpdateView):
    model = Paciente
    fields = ["dni", "apellido", "nombre", "fecha_nacimiento"]
    template_name = "pacientes/form.html"
    success_url = reverse_lazy("paciente_list")

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = "pacientes/confirm_delete.html"
    success_url = reverse_lazy("paciente_list")


# -------------------
# Enfermedad
# -------------------
class EnfermedadListView(ListView):
    model = Enfermedad
    template_name = "enfermedades/lista.html"
    context_object_name = "enfermedades"

class EnfermedadCreateView(CreateView):
    model = Enfermedad
    fields = ["nombre"]
    template_name = "enfermedades/form.html"
    success_url = reverse_lazy("enfermedad_list")

class EnfermedadUpdateView(UpdateView):
    model = Enfermedad
    fields = ["nombre"]
    template_name = "enfermedades/form.html"
    success_url = reverse_lazy("enfermedad_list")

class EnfermedadDeleteView(DeleteView):
    model = Enfermedad
    template_name = "enfermedades/confirm_delete.html"
    success_url = reverse_lazy("enfermedad_list")


# -------------------
# TipoAnalisis
# -------------------
class TipoAnalisisListView(ListView):
    model = TipoAnalisis
    template_name = "tipos_analisis/lista.html"
    context_object_name = "tipos"

class TipoAnalisisCreateView(CreateView):
    model = TipoAnalisis
    fields = ["enfermedad", "nombre"]
    template_name = "tipos_analisis/form.html"
    success_url = reverse_lazy("tipoanalisis_list")

class TipoAnalisisUpdateView(UpdateView):
    model = TipoAnalisis
    fields = ["enfermedad", "nombre"]
    template_name = "tipos_analisis/form.html"
    success_url = reverse_lazy("tipoanalisis_list")

class TipoAnalisisDeleteView(DeleteView):
    model = TipoAnalisis
    template_name = "tipos_analisis/confirm_delete.html"
    success_url = reverse_lazy("tipoanalisis_list")


# -------------------
# Pedido
# -------------------
class PedidoListView(ListView):
    model = Pedido
    template_name = "pedidos/lista.html"
    context_object_name = "pedidos"

# views.py
from django.shortcuts import redirect, render
from django.views import View
from .models import Pedido
from .forms import AnalisisFormSet
from .forms import PedidoForm  # suponiendo que ya tienes un ModelForm para Pedido

class PedidoCreateView(View):
    def get(self, request):
        pedido_form = PedidoForm()
        analisis_formset = AnalisisFormSet()
        return render(request, "pedidos/form.html", {
            "form": pedido_form,
            "analisis_formset": analisis_formset,
        })

    def post(self, request):
        pedido_form = PedidoForm(request.POST)
        analisis_formset = AnalisisFormSet(request.POST)

        if pedido_form.is_valid() and analisis_formset.is_valid():
            pedido = pedido_form.save()
            analisis_formset.instance = pedido
            analisis_formset.save()
            return redirect("pedido_list")

        return render(request, "pedidos/form.html", {
            "form": pedido_form,
            "analisis_formset": analisis_formset,
        })
class PedidoUpdateView(UpdateView):
    model = Pedido
    fields = ["paciente", "medico", "diagnostico", "protocolo"]
    template_name = "pedidos/form.html"
    success_url = reverse_lazy("pedido_list")

class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = "pedidos/confirm_delete.html"
    success_url = reverse_lazy("pedido_list")


# -------------------
# Analisis
# -------------------
class AnalisisListView(ListView):
    model = Analisis
    template_name = "analisis/lista.html"
    context_object_name = "analisis"

class AnalisisCreateView(CreateView):
    model = Analisis
    fields = ["pedido", "tipo_analisis", "resultado", "estado", "impreso", "es_urgente"]
    template_name = "analisis/form.html"
    success_url = reverse_lazy("analisis_list")

class AnalisisUpdateView(UpdateView):
    model = Analisis
    fields = ["pedido", "tipo_analisis", "resultado", "estado", "impreso", "es_urgente"]
    template_name = "analisis/form.html"
    success_url = reverse_lazy("analisis_list")

class AnalisisDeleteView(DeleteView):
    model = Analisis
    template_name = "analisis/confirm_delete.html"
    success_url = reverse_lazy("analisis_list")
