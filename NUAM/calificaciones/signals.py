from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from datetime import datetime
import json

from .models import Calificacion
from auditorias.models import Auditoria


def serializar_calificacion(instance):
    data = model_to_dict(instance)
    serializado = {}

    for key, value in data.items():
        if isinstance(value, datetime):
            serializado[key] = value.isoformat()
        else:
            try:
                json.dumps(value)
                serializado[key] = value
            except:
                serializado[key] = str(value)

    return serializado


def registrar_auditoria(instance, accion):
    actor = getattr(instance, "_actor", None)
    request = getattr(instance, "_request", None)

    Auditoria.objects.create(
        usuario=actor if actor and actor.is_authenticated else None,
        accion=accion,
        modelo="Calificacion",
        objeto_id=str(instance.pk),
        cambios=serializar_calificacion(instance) if accion != "DELETE" else {},
        ip=request.META.get("REMOTE_ADDR") if request else None,
        ruta=request.path if request else "",
    )


@receiver(post_save, sender=Calificacion)
def auditar_guardado(sender, instance, created, **kwargs):
    accion = "CREATE" if created else "UPDATE"
    registrar_auditoria(instance, accion)


@receiver(post_delete, sender=Calificacion)
def auditar_eliminado(sender, instance, **kwargs):
    registrar_auditoria(instance, "DELETE")
