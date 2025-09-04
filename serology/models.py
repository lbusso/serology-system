from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone


class Enfermedad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre


class TipoAnalisis(models.Model):
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE, related_name="tipos_analisis")
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Test-Método"
        verbose_name_plural = "Test-Métodos"

    def __str__(self):
        return f"{self.enfermedad}-{self.nombre}"


class Paciente(models.Model):
    dni = models.CharField(max_length=15, unique=True)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni})"

class Pedido(models.Model):
    protocolo = models.IntegerField(blank=True, null=True, max_length=4)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='pedidos')
    medico = models.CharField(max_length=255, verbose_name="Médico solicitante")  # ahora texto libre
    diagnostico = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)
    impreso = models.BooleanField(default=False)
    es_urgente = models.BooleanField(default=False)
    estado = models.CharField(
        max_length=50,
        choices=[
            ("pendiente", "Pendiente"),
            ("en_proceso", "En proceso"),
            ("finalizado", "Finalizado"),
        ],
        default="pendiente",
    )

    def actualizar_estado(self):
        analisis_qs = self.analisis.all()
        if analisis_qs.exists():
            if all(a.estado == "finalizado" for a in analisis_qs):
                self.estado = "finalizado"
            elif any(a.estado == "en_proceso" for a in analisis_qs):
                self.estado = "en_proceso"
            else:
                self.estado = "pendiente"
            self.save(update_fields=["estado"])

    def generar_informe(self):
        """
        Devuelve el HTML renderizado del informe del pedido
        """
        return render_to_string("informes/pedido.html", {"pedido": self})

    def __str__(self):
        return f"Pedido {self.protocolo} - {self.paciente.apellido}, {self.paciente.nombre}"

class Analisis(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='analisis')
    tipo_analisis = models.ForeignKey(TipoAnalisis, on_delete=models.CASCADE, related_name="analisis_realizados")
    resultado = models.TextField()
    fecha = models.DateField(default=timezone.now)
    estado = models.CharField(
        max_length=50,
        choices=[
            ("pendiente", "Pendiente"),
            ("en_proceso", "En proceso"),
            ("finalizado", "Finalizado"),
        ],
        default="pendiente",
    )


    def __str__(self):
        return f"{self.tipo_analisis} - {self.pedido.paciente} - {self.fecha}"
