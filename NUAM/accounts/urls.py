from django.urls import path
from .views import login_view, me_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", login_view),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", me_view),
]
