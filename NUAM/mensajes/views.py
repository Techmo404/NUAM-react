# mensajes/views.py
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from django.http import FileResponse

from .models import Mensaje, ArchivoMensaje
from .serializers import MensajeSerializer
from accounts.permissions import IsAdmin, IsEmployee
from auditorias.models import Auditoria

def _audit(request, accion, modelo, objeto_id, cambios=None):
    Auditoria.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        accion=accion,
        modelo=modelo,
        objeto_id=str(objeto_id),
        cambios=cambios or {},
        ip=request.META.get("REMOTE_ADDR"),
        ruta=request.path,
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_mensajes(request):
    if request.user.role == "ADMIN":
        qs = Mensaje.objects.all().order_by("-creado")
    else:
        qs = Mensaje.objects.filter(emisor=request.user).order_by("-creado")

    return Response(MensajeSerializer(qs, many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsEmployee])
@parser_classes([MultiPartParser, FormParser])
def crear_mensaje(request):
    asunto = request.data.get("asunto", "").strip()
    contenido = request.data.get("contenido", "").strip()
    certificado_id = request.data.get("certificado_id")

    if not asunto or not contenido:
        return Response({"error": "Debes enviar asunto y contenido"}, status=400)

    mensaje = Mensaje.objects.create(
        emisor=request.user,
        asunto=asunto,
        contenido=contenido,
        certificado_id=certificado_id if certificado_id else None,
        leido_por_admin=False,
        leido_por_emisor=True,
        estado="ABIERTO",
    )

    # Adjuntos: permitir varios
    archivos = request.FILES.getlist("archivos")
    for f in archivos:
        ArchivoMensaje.objects.create(
            mensaje=mensaje,
            archivo=f,
            nombre_original=f.name,
            subido_por=request.user,
        )

    _audit(request, "CREATE", "Mensaje", mensaje.id, {"asunto": asunto, "certificado_id": certificado_id})
    return Response(MensajeSerializer(mensaje).data, status=201)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsEmployee])
@parser_classes([MultiPartParser, FormParser])
def subir_archivo_mensaje(request, mensaje_id):
    try:
        mensaje = Mensaje.objects.get(pk=mensaje_id, emisor=request.user)
    except Mensaje.DoesNotExist:
        return Response({"error": "Mensaje no encontrado"}, status=404)

    archivos = request.FILES.getlist("archivos")
    if not archivos:
        return Response({"error": "Debes adjuntar al menos 1 archivo"}, status=400)

    for f in archivos:
        ArchivoMensaje.objects.create(
            mensaje=mensaje,
            archivo=f,
            nombre_original=f.name,
            subido_por=request.user,
        )

    _audit(request, "CREATE", "ArchivoMensaje", mensaje.id, {"count": len(archivos)})
    return Response({"msg": "Archivos subidos"})

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def responder_mensaje(request, mensaje_id):
    try:
        mensaje = Mensaje.objects.get(pk=mensaje_id)
    except Mensaje.DoesNotExist:
        return Response({"error": "Mensaje no encontrado"}, status=404)

    respuesta = (request.data.get("respuesta") or "").strip()
    if not respuesta:
        return Response({"error": "Debes escribir una respuesta"}, status=400)

    mensaje.respuesta = respuesta
    mensaje.respondido_por = request.user
    mensaje.respondido_en = timezone.now()
    mensaje.estado = "RESPONDIDO"

    # notificación al empleado: el emisor tiene algo nuevo
    mensaje.leido_por_emisor = False
    mensaje.leido_por_admin = True

    mensaje.save()

    _audit(request, "UPDATE", "Mensaje", mensaje.id, {"respuesta": "OK", "estado": "RESPONDIDO"})
    return Response(MensajeSerializer(mensaje).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def marcar_leido(request, mensaje_id):
    try:
        if request.user.role == "ADMIN":
            mensaje = Mensaje.objects.get(pk=mensaje_id)
            mensaje.leido_por_admin = True
        else:
            mensaje = Mensaje.objects.get(pk=mensaje_id, emisor=request.user)
            mensaje.leido_por_emisor = True

        mensaje.save()
        return Response({"msg": "OK"})
    except Mensaje.DoesNotExist:
        return Response({"error": "Mensaje no encontrado"}, status=404)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_count(request):
    if request.user.role == "ADMIN":
        count = Mensaje.objects.filter(leido_por_admin=False).count()
    else:
        count = Mensaje.objects.filter(emisor=request.user, leido_por_emisor=False).count()

    return Response({"unread": count})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def descargar_archivo(request, archivo_id):
    try:
        archivo = ArchivoMensaje.objects.select_related("mensaje", "mensaje__emisor").get(pk=archivo_id)
    except ArchivoMensaje.DoesNotExist:
        return Response({"error": "Archivo no encontrado"}, status=404)

    # Permisos:
    # Admin puede todo
    # Empleado solo si es el emisor del mensaje
    if request.user.role != "ADMIN" and archivo.mensaje.emisor_id != request.user.id:
        return Response({"error": "No autorizado"}, status=403)

    # Descargar
    response = FileResponse(archivo.archivo.open("rb"), as_attachment=True, filename=archivo.nombre_original)
    _audit(request, "UPDATE", "ArchivoMensaje", archivo.id, {"download": True})
    return response
