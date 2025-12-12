from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.ping),

    # ADMIN
    path('listar/', views.lista_calificaciones),
    path('crear/', views.crear_calificacion),
    path('editar/<int:pk>/', views.editar_calificacion),
    path('eliminar/<int:pk>/', views.eliminar_calificacion),

    # EMPLEADO
    path('mis/', views.mis_calificaciones),

    # DESDE CERTIFICADO
    path(
        'crear-desde-certificado/<int:certificado_id>/',
        views.crear_desde_certificado
    ),

    # 🔁 RECALCULAR (A1)
    path(
        'recalcular/<int:pk>/',
        views.recalcular_calificacion
    ),
]
