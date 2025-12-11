from django.db import models
from django.conf import settings


class Auditoria(models.Model):
    ACCION_CHOICES = (
        ("CREATE", "Creación"),
        ("UPDATE", "Actualización"),
        ("DELETE", "Eliminación"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="auditorias"
    )
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    modelo = models.CharField(max_length=100)
    objeto_id = models.CharField(max_length=50, blank=True)
    cambios = models.JSONField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    ruta = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.accion}] {self.modelo} ({self.objeto_id}) - {self.fecha}"
