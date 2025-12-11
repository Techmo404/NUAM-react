from django.contrib import admin
from .models import Auditoria
import json
from django.utils.safestring import mark_safe


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "usuario", "accion", "modelo", "objeto_id", "ip")
    list_filter = ("accion", "modelo", "fecha")
    search_fields = ("usuario__username", "modelo", "objeto_id", "ruta")

    readonly_fields = ("usuario", "accion", "modelo", "objeto_id", "cambios_pretty", "ip", "ruta", "fecha")

    fieldsets = (
        ("Información", {
            "fields": ("fecha", "usuario", "accion", "modelo", "objeto_id", "ip", "ruta")
        }),
        ("Cambios registrados", {
            "fields": ("cambios_pretty",),
        }),
    )

    def cambios_pretty(self, obj):
        """Muestra JSON formateado o mensaje vacío."""
        if not obj.cambios:
            return "(sin cambios)"

        try:
            pretty_json = json.dumps(obj.cambios, indent=4, ensure_ascii=False)
            return mark_safe(f"<pre>{pretty_json}</pre>")
        except:
            return obj.cambios

    cambios_pretty.short_description = "Cambios (JSON formateado)"
