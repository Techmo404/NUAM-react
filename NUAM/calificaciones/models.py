from django.db import models
from django.conf import settings

from certificados.models import Certificado

class Calificacion(models.Model):
    cliente = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    factor = models.DecimalField(max_digits=5, decimal_places=2)
    tipo = models.CharField(max_length=50)
    fecha = models.DateField()

    certificado = models.ForeignKey(
        Certificado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calificaciones"
    )

    usuario_asociado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="calificaciones"
    )


    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cliente} - {self.monto}"
    
    