from django.contrib import admin
from .models import Certificado


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = (
        "id", "cliente", "rut_cliente", "periodo",
        "tipo", "monto_bruto", "monto_impuesto",
        "usuario_asociado", "fecha_emision"
    )
    search_fields = ("cliente", "rut_cliente", "periodo")
    list_filter = ("tipo", "periodo", "fecha_emision")
