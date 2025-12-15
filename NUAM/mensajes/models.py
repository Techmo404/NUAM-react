# mensajes/models.py
from django.db import models
from django.conf import settings

class Mensaje(models.Model):
    ESTADO_CHOICES = (
        ("ABIERTO", "Abierto"),
        ("RESPONDIDO", "Respondido"),
        ("CERRADO", "Cerrado"),
    )

    emisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mensajes_enviados"
    )

    # ✅ Ligado opcional a Certificado
    certificado = models.ForeignKey(
        "certificados.Certificado",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mensajes"
    )

    asunto = models.CharField(max_length=150)
    contenido = models.TextField()

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="ABIERTO")

    # Para “notificación”
    leido_por_admin = models.BooleanField(default=False)
    leido_por_emisor = models.BooleanField(default=True)  # el emisor ya lo “leyó” al crearlo

    # Respuesta admin
    respondido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mensajes_respondidos"
    )
    respuesta = models.TextField(null=True, blank=True)
    respondido_en = models.DateTimeField(null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.estado}] {self.asunto} - {self.emisor}"


class ArchivoMensaje(models.Model):
    mensaje = models.ForeignKey(
        Mensaje,
        on_delete=models.CASCADE,
        related_name="archivos"
    )

    archivo = models.FileField(upload_to="mensajes/")
    nombre_original = models.CharField(max_length=255)

    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_original
