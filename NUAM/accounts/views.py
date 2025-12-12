# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, UserSerializer
from auditorias.models import Auditoria  # 👈 importamos el modelo
from accounts.permissions import IsAdmin
from .models import User

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


@api_view(["GET", "POST"])
@permission_classes([IsAdmin])
def usuarios_admin(request):
    if request.method == "GET":
        usuarios = User.objects.all()
        serializer = UserSerializer(usuarios, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crear usuario con password por defecto
        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            role=serializer.validated_data.get("role", "EMP"),
            password="123456"  # luego se puede mejorar
        )

        return Response(UserSerializer(user).data, status=201)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAdmin])
def usuario_admin_detalle(request, pk):
    try:
        usuario = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)

    if request.method == "PUT":
        serializer = UserSerializer(usuario, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        usuario.delete()
        return Response({"msg": "Usuario eliminado"})
