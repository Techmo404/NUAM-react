from django.contrib import admin
from .models import Calificacion

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ("cliente", "monto", "factor", "tipo", "fecha", "usuario_asociado")
    list_filter = ("tipo", "fecha")
    search_fields = ("cliente",)
