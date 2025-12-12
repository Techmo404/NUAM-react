from django.db import models
from django.conf import settings
from django.utils import timezone

class Certificado(models.Model):
    TIPO_CHOICES = (
        ("A", "Tipo A"),
        ("B", "Tipo B"),
        ("C", "Tipo C"),
    )

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default="A")

    cliente = models.CharField(max_length=100, default="")
    rut_cliente = models.CharField(max_length=20, default="")
    periodo = models.CharField(max_length=20, default="2025")
    fecha_emision = models.DateField(default=timezone.now)

    monto_bruto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    fecha_ingreso = models.DateField(auto_now_add=True)

    usuario_asociado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certificados"
    )

    archivo = models.FileField(upload_to="certificados/", null=True, blank=True)

    def __str__(self):
        return f"Certificado {self.tipo} - Usuario {self.usuario_asociado.username}"
