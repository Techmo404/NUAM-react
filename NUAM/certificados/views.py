import csv
import os
from io import TextIOWrapper
from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsEmployee
from auditorias.models import Auditoria
from .models import Certificado, CertificadoArchivo, CargaMasivaArchivo
from .serializers import (
    CertificadoSerializer,
    CargaMasivaArchivoSerializer
)
from decimal import Decimal


def ping(request):
    return JsonResponse({"message": "certificados OK"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_certificados(request):
    if request.user.role == "EMP":
        certificados = Certificado.objects.filter(usuario_asociado=request.user)
    else:
        certificados = Certificado.objects.all()

    return Response(CertificadoSerializer(certificados, many=True).data)


@api_view(["POST"])
@permission_classes([IsEmployee])
def crear_certificado(request):
    serializer = CertificadoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    certificado = serializer.save(usuario_asociado=request.user)

    # ✅ FIX: convertir Decimal → str para JSON
    cambios = {}
    for k, v in serializer.validated_data.items():
        if isinstance(v, Decimal):
            cambios[k] = str(v)
        else:
            cambios[k] = v

    Auditoria.objects.create(
        usuario=request.user,
        accion="CREATE",
        modelo="Certificado",
        objeto_id=str(certificado.pk),
        cambios=cambios,
        ruta=request.path,
    )

    return Response(
        CertificadoSerializer(certificado).data,
        status=201
    )


@api_view(["POST"])
@permission_classes([IsEmployee])
def subir_archivo_certificado(request, certificado_id):
    certificado = Certificado.objects.get(
        pk=certificado_id,
        usuario_asociado=request.user
    )

    archivo = request.FILES.get("archivo")
    extension = archivo.name.split(".")[-1].upper()

    CertificadoArchivo.objects.create(
        certificado=certificado,
        archivo=archivo,
        nombre_original=archivo.name,
        tipo=extension,
        subido_por=request.user
    )

    return Response({"msg": "Archivo subido"}, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def descargar_archivo(request, archivo_id):
    archivo = CertificadoArchivo.objects.get(pk=archivo_id)

    if request.user.role == "EMP" and archivo.certificado.usuario_asociado != request.user:
        return Response({"error": "No autorizado"}, status=403)

    return FileResponse(
        open(archivo.archivo.path, "rb"),
        as_attachment=True,
        filename=archivo.nombre_original
    )


# ==========================
# 🔥 ARCHIVOS MASIVOS
# ==========================

# views.py
@api_view(["POST"])
@permission_classes([IsEmployee])
def subir_archivo_masivo(request):
    archivo = request.FILES.get("archivo")
    extension = archivo.name.split(".")[-1].upper()

    registro = CargaMasivaArchivo.objects.create(
        archivo=archivo,
        nombre_original=archivo.name,
        tipo=extension,
        subido_por=request.user
    )

    return Response(CargaMasivaArchivoSerializer(registro).data, status=201)

@api_view(["GET"])
@permission_classes([IsEmployee])
def listar_archivos_masivos(request):
    archivos = CargaMasivaArchivo.objects.filter(subido_por=request.user)
    return Response(CargaMasivaArchivoSerializer(archivos, many=True).data)

@api_view(["GET"])
@permission_classes([IsEmployee])
def descargar_archivo_masivo(request, archivo_id):
    archivo = CargaMasivaArchivo.objects.get(pk=archivo_id, subido_por=request.user)

    return FileResponse(
        open(archivo.archivo.path, "rb"),
        as_attachment=True,
        filename=archivo.nombre_original
    )

@api_view(["DELETE"])
@permission_classes([IsEmployee])
def eliminar_archivo_masivo(request, archivo_id):
    archivo = CargaMasivaArchivo.objects.get(pk=archivo_id, subido_por=request.user)
    archivo.archivo.delete(save=False)
    archivo.delete()
    return Response({"msg": "Archivo eliminado"})

@api_view(["DELETE"])
@permission_classes([IsEmployee])
def eliminar_certificado(request, certificado_id):
    try:
        certificado = Certificado.objects.get(
            pk=certificado_id,
            usuario_asociado=request.user
        )
    except Certificado.DoesNotExist:
        return Response({"error": "Certificado no encontrado"}, status=404)

    certificado.delete()

    return Response({"msg": "Certificado eliminado correctamente"})
