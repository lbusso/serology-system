from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Analisis
from django.db.models.signals import pre_save


@receiver(post_save, sender=Analisis)
def actualizar_estado_pedido(sender, instance, **kwargs):
    instance.pedido.actualizar_estado()


@receiver(pre_save, sender=Analisis)
def set_estado_finalizado(sender, instance, **kwargs):
    """
    Si el resultado está cargado y el estado no es finalizado,
    se marca automáticamente como finalizado.
    """
    if instance.resultado and instance.estado != "finalizado":
        instance.estado = "finalizado"
