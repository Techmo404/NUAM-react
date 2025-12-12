from django.urls import path
from . import views

urlpatterns = [
    path("ping/", views.ping),
    path("anual/", views.reporte_anual),
    path("cliente/", views.reporte_por_cliente),
    path("export/pdf/<int:reporte_id>/", views.exportar_reporte_pdf),
    path("export/excel/<int:reporte_id>/", views.exportar_reporte_excel),

]
