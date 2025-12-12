from django.urls import path
from .views import login_view, me_view
from rest_framework_simplejwt.views import TokenRefreshView
from .views import usuarios_admin, usuario_admin_detalle

urlpatterns = [
    path("login/", login_view),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", me_view),
    path("users/", usuarios_admin),
    path("users/<int:pk>/", usuario_admin_detalle),
]
