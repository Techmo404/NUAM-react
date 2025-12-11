# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, UserSerializer
from auditorias.models import Auditoria  # 👈 importamos el modelo


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.user  # viene del serializer
    ip = request.META.get("REMOTE_ADDR")
    ruta = request.path

    Auditoria.objects.create(
        usuario=user,
        accion="LOGIN",
        modelo="User",
        objeto_id=str(user.pk),
        cambios=None,
        ip=ip,
        ruta=ruta,
    )

    return Response(serializer.validated_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Create your views here.
