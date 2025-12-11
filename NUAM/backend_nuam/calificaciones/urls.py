from django.urls import path
from . import views

urlpatterns = [
    # Más adelante: listar, crear, etc.
    path('ping/', views.ping, name='calificaciones-ping'),
]
