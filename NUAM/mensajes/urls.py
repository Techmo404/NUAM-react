# mensajes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_mensajes),
    path("crear/", views.crear_mensaje),

    path("<int:mensaje_id>/subir-archivos/", views.subir_archivo_mensaje),
    path("<int:mensaje_id>/responder/", views.responder_mensaje),
    path("<int:mensaje_id>/leido/", views.marcar_leido),

    path("unread-count/", views.unread_count),
    path("archivo/<int:archivo_id>/descargar/", views.descargar_archivo),
]
