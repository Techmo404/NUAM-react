from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from django.utils.timezone import is_naive
from datetime import datetime
import json

from .models import Auditoria

User = get_user_model()


# --- Función para serializar valores no JSON-compatibles ---
def serializar_cambios(instance):
    data = model_to_dict(instance)
    serializado = {}

    for key, value in data.items():

        # Manejar datetime -> ISO string
        if isinstance(value, datetime):
            serializado[key] = value.isoformat()

        else:
            try:
                json.dumps(value)  # probar si se puede convertir directamente
                serializado[key] = value
            except:
                serializado[key] = str(value)

    return serializado


def _registrar_auditoria(instance, accion):
    actor = getattr(instance, "_actor", None)
    request = getattr(instance, "_request", None)

    Auditoria.objects.create(
        usuario=actor if (actor and actor.is_authenticated) else None,
        accion=accion,
        modelo=instance.__class__.__name__,
        objeto_id=str(instance.pk),
        cambios=serializar_cambios(instance) if accion != "DELETE" else {},
        ip=request.META.get("REMOTE_ADDR") if request else None,
        ruta=request.path if request else "",
    )



@receiver(post_save, sender=User)
def auditar_usuario_guardado(sender, instance, created, **kwargs):
    accion = "CREATE" if created else "UPDATE"
    _registrar_auditoria(instance, accion)


@receiver(post_delete, sender=User)
def auditar_usuario_eliminado(sender, instance, **kwargs):
    _registrar_auditoria(instance, "DELETE")
