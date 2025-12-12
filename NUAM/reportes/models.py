from django.db import models
from django.conf import settings


class Reporte(models.Model):
    TIPO_CHOICES = (
        ("ANUAL", "Anual"),
        ("CLIENTE", "Por cliente"),
    )

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    anio = models.PositiveIntegerField(null=True, blank=True)
    cliente = models.CharField(max_length=100, null=True, blank=True)

    generado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reportes"
    )

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte {self.tipo} - {self.anio or self.cliente}"
