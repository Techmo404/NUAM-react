from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from datetime import datetime
import json

from .models import Auditoria
from certificados.models import Certificado
from calificaciones.models import Calificacion

User = get_user_model()


# ==========================
# UTILIDAD SERIALIZACIÓN
# ==========================
def serializar_cambios(instance):
    """
    Convierte una instancia de modelo en un dict compatible con JSON,
    manejando datetime, decimal y otros tipos no serializables.
    """
    data = model_to_dict(instance)
    serializado = {}

    for key, value in data.items():
        if isinstance(value, datetime):
            serializado[key] = value.isoformat()
        else:
            try:
                json.dumps(value)
                serializado[key] = value
            except Exception:
                serializado[key] = str(value)

    return serializado


# ==========================
# FUNCIÓN CENTRAL DE AUDITORÍA
# ==========================
def _registrar_auditoria(instance, accion):
    """
    Registra una auditoría para cualquier modelo.
    Usa _actor y _request si existen (API),
    funciona sin ellos (Admin).
    """
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


# ==========================
# AUDITORÍA USUARIOS
# ==========================
@receiver(post_save, sender=User)
def auditar_usuario_guardado(sender, instance, created, **kwargs):
    accion = "CREATE" if created else "UPDATE"
    _registrar_auditoria(instance, accion)


@receiver(post_delete, sender=User)
def auditar_usuario_eliminado(sender, instance, **kwargs):
    _registrar_auditoria(instance, "DELETE")


# ==========================
# AUDITORÍA CERTIFICADOS
# ==========================
@receiver(post_save, sender=Certificado)
def auditar_certificado_guardado(sender, instance, created, **kwargs):
    accion = "CREATE" if created else "UPDATE"
    _registrar_auditoria(instance, accion)


@receiver(post_delete, sender=Certificado)
def auditar_certificado_eliminado(sender, instance, **kwargs):
    _registrar_auditoria(instance, "DELETE")


# ==========================
# AUDITORÍA CALIFICACIONES
# ==========================
@receiver(post_save, sender=Calificacion)
def auditar_calificacion_guardada(sender, instance, created, **kwargs):
    accion = "CREATE" if created else "UPDATE"
    _registrar_auditoria(instance, accion)


@receiver(post_delete, sender=Calificacion)
def auditar_calificacion_eliminada(sender, instance, **kwargs):
    _registrar_auditoria(instance, "DELETE")
