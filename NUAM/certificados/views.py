import csv
from io import TextIOWrapper

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin, IsEmployee
from rest_framework.response import Response
from django.http import JsonResponse

from auditorias.models import Auditoria
from .models import Certificado
from .serializers import CertificadoSerializer


def ping(request):
    return JsonResponse({"message": "certificados OK"})


# ============================
# LISTADO
# ============================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_certificados(request):
    if request.user.role == "EMP":
        certificados = Certificado.objects.filter(usuario_asociado=request.user)
    else:
        certificados = Certificado.objects.all()

    serializer = CertificadoSerializer(certificados, many=True)
    return Response(serializer.data)


# ============================
# CREAR MANUAL
# ============================
@api_view(["POST"])
@permission_classes([IsEmployee])
def crear_certificado(request):
    data = request.data.copy()
    data["usuario_asociado"] = request.user.id

    serializer = CertificadoSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    certificado = serializer.save()

    Auditoria.objects.create(
        usuario=request.user,
        accion="CREATE",
        modelo="Certificado",
        objeto_id=str(certificado.pk),
        cambios=data,
        ip=request.META.get("REMOTE_ADDR"),
        ruta=request.path,
    )

    return Response(serializer.data)


# ============================
# ELIMINAR (SOLO ADMIN)
# ============================
@api_view(["DELETE"])
@permission_classes([IsAdmin])
def eliminar_certificado(request, pk):

    try:
        certificado = Certificado.objects.get(pk=pk)
    except Certificado.DoesNotExist:
        return Response({"error": "No encontrado"}, status=404)

    certificado.delete()

    Auditoria.objects.create(
        usuario=request.user,
        accion="DELETE",
        modelo="Certificado",
        objeto_id=str(pk),
        cambios={},
        ip=request.META.get("REMOTE_ADDR"),
        ruta=request.path,
    )

    return Response({"msg": "Eliminado"})


# ============================
# CARGA MASIVA CSV
# ============================
@api_view(["POST"])
@permission_classes([IsEmployee])
def carga_masiva(request):
    """
    Recibe archivo CSV con columnas:
    cliente,rut_cliente,periodo,tipo,monto_bruto,monto_impuesto,fecha_emision
    """

    if "archivo" not in request.FILES:
        return Response({"error": "Debes subir un archivo CSV"}, status=400)

    archivo = request.FILES["archivo"]
    file = TextIOWrapper(archivo.file, encoding="utf-8")
    reader = csv.DictReader(file)

    creados = 0

    for fila in reader:
        data = {
            "cliente": fila["cliente"],
            "rut_cliente": fila["rut_cliente"],
            "periodo": fila["periodo"],
            "tipo": fila["tipo"],
            "monto_bruto": fila["monto_bruto"],
            "monto_impuesto": fila["monto_impuesto"],
            "fecha_emision": fila["fecha_emision"],
            "usuario_asociado": request.user.id,
        }

        serializer = CertificadoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            creados += 1

    Auditoria.objects.create(
        usuario=request.user,
        accion="CREATE",
        modelo="Certificado",
        objeto_id="CARGA_MASIVA",
        cambios={"filas_creadas": creados},
        ip=request.META.get("REMOTE_ADDR"),
        ruta=request.path,
    )

    return Response({"msg": f"Certificados creados: {creados}"})
