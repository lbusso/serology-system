from django import forms
from .models import Paciente, Analisis, Enfermedad, TipoAnalisis, Pedido
from django.forms import inlineformset_factory


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["dni", "apellido", "nombre", "fecha_nacimiento"]
        widgets = {
            "dni": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class EnfermedadForm(forms.ModelForm):
    class Meta:
        model = Enfermedad
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }


class TipoAnalisisForm(forms.ModelForm):
    class Meta:
        model = TipoAnalisis
        fields = ["enfermedad", "nombre"]
        widgets = {
            "enfermedad": forms.Select(attrs={"class": "form-select"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["paciente", "medico", "protocolo"]
        widgets = {
            "paciente": forms.Select(attrs={"class": "form-select"}),
            "medico": forms.TextInput(attrs={"class": "form-control"}),
            "protocolo": forms.TextInput(attrs={"class": "form-control"}),
        }

class AnalisisForm(forms.ModelForm):
    class Meta:
        model = Analisis
        fields = ["tipo_analisis"]
        widgets = {
            "tipo_analisis": forms.Select(attrs={"class": "form-select"}),
        }

AnalisisFormSet = inlineformset_factory(
    Pedido, Analisis, form=AnalisisForm,
    extra=1, can_delete=True
)
