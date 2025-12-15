from django.db import models
from django.conf import settings
from django.utils import timezone


class Certificado(models.Model):
    TIPO_CHOICES = (
        ("Honorarios", "Honorarios"),
        ("Servicios", "Servicios"),
        ("Rentas", "Rentas"),
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="Honorarios"
    )

    cliente = models.CharField(max_length=100)
    rut_cliente = models.CharField(max_length=20)
    periodo = models.CharField(max_length=20, default="2025")

    # Fecha de emisión del certificado
    fecha_emision = models.DateField(default=timezone.localdate)

    monto_bruto = models.DecimalField(max_digits=12, decimal_places=2)
    monto_impuesto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_ingreso = models.DateField(auto_now_add=True)

    usuario_asociado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certificados"
    )

    def __str__(self):
        return f"Certificado {self.id} - {self.cliente}"


class CertificadoArchivo(models.Model):
    certificado = models.ForeignKey(
        Certificado,
        on_delete=models.CASCADE,
        related_name="archivos"
    )

    archivo = models.FileField(upload_to="certificados/adjuntos/")
    nombre_original = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20)

    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_original


class CargaMasivaArchivo(models.Model):
    archivo = models.FileField(upload_to="cargas_masivas/")
    nombre_original = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20)  # CSV, XLSX, DOCX, PDF

    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_original
