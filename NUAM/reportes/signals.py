from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reporte
from auditorias.models import Auditoria


@receiver(post_save, sender=Reporte)
def auditar_reporte_save(sender, instance, created, **kwargs):
    Auditoria.objects.create(
        usuario=instance.generado_por,
        accion="CREATE" if created else "UPDATE",
        modelo="Reporte",
        objeto_id=str(instance.pk),
        cambios={"tipo": instance.tipo},
    )


@receiver(post_delete, sender=Reporte)
def auditar_reporte_delete(sender, instance, **kwargs):
    Auditoria.objects.create(
        usuario=instance.generado_por,
        accion="DELETE",
        modelo="Reporte",
        objeto_id=str(instance.pk),
        cambios={},
    )
