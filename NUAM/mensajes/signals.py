from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Mensaje
from auditorias.signals import _registrar_auditoria


@receiver(post_save, sender=Mensaje)
def auditar_mensaje_guardado(sender, instance, created, **kwargs):
    accion = "CREATE" if created else "UPDATE"
    _registrar_auditoria(instance, accion)


@receiver(post_delete, sender=Mensaje)
def auditar_mensaje_eliminado(sender, instance, **kwargs):
    _registrar_auditoria(instance, "DELETE")
