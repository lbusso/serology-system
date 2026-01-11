from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import date


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


class PerfilPedido(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    tipos_analisis = models.ManyToManyField(TipoAnalisis, related_name="perfiles")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Perfil de pedido"
        verbose_name_plural = "Perfiles de pedido"

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    dni = models.CharField(max_length=15, unique=True)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(
        max_length=1,
        choices=[("F", "Femenino"), ("M", "Masculino")],
        blank=True,
        null=True,
    )

    def codigo_filiacion(self):
        if not self.sexo:
            return None
        nombre = (self.nombre or "").strip().upper()
        apellido = (self.apellido or "").strip().upper()
        fecha = self.fecha_nacimiento.strftime("%d%m%Y")
        return f"{self.sexo}{nombre[:2]}{apellido[:2]}{fecha}"

    @property
    def edad(self):
        hoy = date.today()
        if not self.fecha_nacimiento:
            return None
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def __str__(self):
        edad = self.edad
        edad_texto = f"{edad} años" if edad is not None else "edad desconocida"
        return f"{self.apellido}, {self.nombre} ({self.dni}) - {edad_texto}"

class Pedido(models.Model):
    protocolo = models.IntegerField(blank=True, null=True, max_length=4)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='pedidos')
    perfil = models.ForeignKey(
        'PerfilPedido',
        on_delete=models.SET_NULL,
        related_name='pedidos',
        blank=True,
        null=True,
    )
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

    def analisis_no_hiv(self):
        return self.analisis.exclude(tipo_analisis__enfermedad__nombre="HIV")

    def analisis_hiv(self):
        return self.analisis.filter(tipo_analisis__enfermedad__nombre="HIV")

    def generar_informe(self):
        """
        Devuelve el HTML renderizado del informe del pedido
        """
        return render_to_string("informes/pedido.html", {
            "pedido": self,
            "analisis": self.analisis_no_hiv(),
        })

    def generar_informe_hiv(self):
        return render_to_string("informes/pedido_hiv.html", {
            "pedido": self,
            "analisis": self.analisis_hiv(),
        })

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # guardamos el pedido primero
        # Actualizamos las fechas de sus análisis
        self.analisis.update(fecha=self.fecha.date())

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
