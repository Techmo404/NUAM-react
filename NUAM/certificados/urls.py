from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_certificados),
    path("crear/", views.crear_certificado),
    path("eliminar/<int:pk>/", views.eliminar_certificado),

    # Carga masiva CSV
    path("carga-masiva/", views.carga_masiva),

    path("ping/", views.ping),
]
