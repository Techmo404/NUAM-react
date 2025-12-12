from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Q

from .models import Calificacion
from .serializers import CalificacionSerializer
from accounts.permissions import IsAdmin, IsEmployee
from auditorias.models import Auditoria
from certificados.models import Certificado
from .services import CalculoTributarioService




# ----------- AUDITORIA REUTILIZABLE -------------
def registrar_auditoria(request, instance, accion):
    Auditoria.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        accion=accion,
        modelo="Calificacion",
        objeto_id=str(instance.pk),
        cambios=CalificacionSerializer(instance).data if accion != "DELETE" else {},
        ip=request.META.get("REMOTE_ADDR"),
        ruta=request.path,
    )


# ----------- PING -------------
def ping(request):
    return JsonResponse({"message": "calificaciones OK"})


# ----------- LISTADO ADMIN (todo) -------------
@api_view(["GET"])
@permission_classes([IsAdmin])
def lista_calificaciones(request):
    queryset = Calificacion.objects.all().order_by("-id")

    # FILTROS
    cliente = request.GET.get("cliente")
    tipo = request.GET.get("tipo")
    ano = request.GET.get("ano")

    if cliente:
        queryset = queryset.filter(cliente__icontains=cliente)
    if tipo:
        queryset = queryset.filter(tipo__icontains=tipo)
    if ano:
        queryset = queryset.filter(fecha__year=ano)

    serializer = CalificacionSerializer(queryset, many=True)
    return Response(serializer.data)


# ----------- LISTADO EMPLEADO (solo las suyas) -------------
@api_view(["GET"])
@permission_classes([IsEmployee])
def mis_calificaciones(request):
    queryset = Calificacion.objects.filter(usuario_asociado=request.user)

    serializer = CalificacionSerializer(queryset, many=True)
    return Response(serializer.data)


# ----------- CREAR REGISTRO (ADMIN) -------------
@api_view(["POST"])
@permission_classes([IsAdmin])
def crear_calificacion(request):
    serializer = CalificacionSerializer(data=request.data)
    if serializer.is_valid():
        calif = serializer.save()
        registrar_auditoria(request, calif, "CREATE")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------- EDITAR REGISTRO (ADMIN) -------------
@api_view(["PUT"])
@permission_classes([IsAdmin])
def editar_calificacion(request, pk):
    try:
        calif = Calificacion.objects.get(pk=pk)
    except Calificacion.DoesNotExist:
        return Response({"error": "No encontrado"}, status=404)

    serializer = CalificacionSerializer(calif, data=request.data, partial=True)
    if serializer.is_valid():
        calif = serializer.save()
        registrar_auditoria(request, calif, "UPDATE")
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# ----------- ELIMINAR REGISTRO (ADMIN) -------------
@api_view(["DELETE"])
@permission_classes([IsAdmin])
def eliminar_calificacion(request, pk):
    try:
        calif = Calificacion.objects.get(pk=pk)
    except Calificacion.DoesNotExist:
        return Response({"error": "No encontrado"}, status=404)

    registrar_auditoria(request, calif, "DELETE")
    calif.delete()

    return Response({"msg": "Eliminado correctamente"})

@api_view(["POST"])
@permission_classes([IsAdmin])
def crear_desde_certificado(request, certificado_id):
    """
    Genera una calificación tributaria a partir de un certificado
    """
    try:
        certificado = Certificado.objects.get(pk=certificado_id)
    except Certificado.DoesNotExist:
        return Response({"error": "Certificado no encontrado"}, status=404)

    # Evitar duplicados por certificado + periodo
    if Calificacion.objects.filter(
        cliente=certificado.cliente,
        fecha__year=certificado.fecha_emision.year,
        tipo=certificado.tipo
    ).exists():
        return Response(
            {"error": "Ya existe una calificación para este certificado"},
            status=400
        )

    servicio = CalculoTributarioService(certificado)
    resultado = servicio.calcular_declaracion()

    calificacion = Calificacion.objects.create(
        cliente=resultado["cliente"],
        monto=resultado["monto_final"],
        factor=resultado["factor"],
        tipo=resultado["tipo_certificado"],
        fecha=certificado.fecha_emision,
        usuario_asociado=certificado.usuario_asociado,
    )

    registrar_auditoria(request, calificacion, "CREATE")

    return Response({
        "msg": "Calificación creada desde certificado",
        "calificacion": CalificacionSerializer(calificacion).data,
    }, status=201)

@api_view(["PUT"])
@permission_classes([IsAdmin])
def recalcular_calificacion(request, pk):
    """
    Recalcula una calificación usando su certificado asociado
    """
    try:
        calificacion = Calificacion.objects.get(pk=pk)
    except Calificacion.DoesNotExist:
        return Response({"error": "Calificación no encontrada"}, status=404)

    if not calificacion.certificado:
        return Response(
            {"error": "La calificación no tiene certificado asociado"},
            status=400
        )

    servicio = CalculoTributarioService(calificacion.certificado)
    resultado = servicio.calcular_declaracion()

    calificacion.monto = resultado["monto_final"]
    calificacion.factor = resultado["factor"]
    calificacion.tipo = resultado["tipo_certificado"]
    calificacion.fecha = calificacion.certificado.fecha_emision
    calificacion.save()

    return Response({
        "msg": "Calificación recalculada correctamente",
        "calificacion": CalificacionSerializer(calificacion).data
    })
