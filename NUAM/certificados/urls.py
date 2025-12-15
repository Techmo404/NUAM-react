from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_certificados),
    path("crear/", views.crear_certificado),
    path("subir-archivo/<int:certificado_id>/", views.subir_archivo_certificado),
    path("descargar-archivo/<int:archivo_id>/", views.descargar_archivo),
    path("eliminar/<int:certificado_id>/", views.eliminar_certificado),

    path("archivos-masivos/", views.listar_archivos_masivos),
    path("archivos-masivos/subir/", views.subir_archivo_masivo),
    path("archivos-masivos/descargar/<int:archivo_id>/", views.descargar_archivo_masivo),
    path("archivos-masivos/eliminar/<int:archivo_id>/", views.eliminar_archivo_masivo),

    path("ping/", views.ping),
]
