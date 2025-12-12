from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from .models import Reporte
from .serializers import ReporteSerializer
from calificaciones.models import Calificacion
from accounts.permissions import IsAdmin
import os
from django.conf import settings
from .utils import generar_pdf


def ping(request):
    return JsonResponse({"message": "reportes OK"})


@api_view(["POST"])
@permission_classes([IsAdmin])
def reporte_anual(request):
    """
    Genera reporte anual de calificaciones
    body: { "anio": 2025 }
    """
    anio = request.data.get("anio")
    if not anio:
        return Response({"error": "Debes indicar el año"}, status=400)

    calificaciones = Calificacion.objects.filter(fecha__year=anio)

    total_monto = sum([c.monto for c in calificaciones])

    reporte = Reporte.objects.create(
        tipo="ANUAL",
        anio=anio,
        generado_por=request.user
    )

    return Response({
        "reporte": ReporteSerializer(reporte).data,
        "total_calificaciones": calificaciones.count(),
        "total_monto": total_monto,
        "detalle": [
            {
                "cliente": c.cliente,
                "monto": str(c.monto),
                "fecha": c.fecha
            }
            for c in calificaciones
        ]
    })


@api_view(["POST"])
@permission_classes([IsAdmin])
def reporte_por_cliente(request):
    """
    Genera reporte por cliente
    body: { "cliente": "Empresa Demo SpA" }
    """
    cliente = request.data.get("cliente")
    if not cliente:
        return Response({"error": "Debes indicar el cliente"}, status=400)

    calificaciones = Calificacion.objects.filter(cliente__icontains=cliente)
    total_monto = sum([c.monto for c in calificaciones])

    reporte = Reporte.objects.create(
        tipo="CLIENTE",
        cliente=cliente,
        generado_por=request.user
    )

    return Response({
        "reporte": ReporteSerializer(reporte).data,
        "total_calificaciones": calificaciones.count(),
        "total_monto": total_monto,
        "detalle": [
            {
                "anio": c.fecha.year,
                "monto": str(c.monto)
            }
            for c in calificaciones
        ]
    })

@api_view(["GET"])
@permission_classes([IsAdmin])
def exportar_reporte_pdf(request, reporte_id):
    try:
        reporte = Reporte.objects.get(pk=reporte_id)
    except Reporte.DoesNotExist:
        return Response({"error": "Reporte no encontrado"}, status=404)

    path = os.path.join(settings.BASE_DIR, f"reporte_{reporte.id}.pdf")

    lineas = [
        f"Tipo: {reporte.tipo}",
        f"Año: {reporte.anio}",
        f"Cliente: {reporte.cliente}",
        f"Generado por: {reporte.generado_por}",
    ]

    generar_pdf(path, "Reporte NUAM", lineas)

    return Response({"msg": "PDF generado", "archivo": path})

from .utils import generar_excel


@api_view(["GET"])
@permission_classes([IsAdmin])
def exportar_reporte_excel(request, reporte_id):
    try:
        reporte = Reporte.objects.get(pk=reporte_id)
    except Reporte.DoesNotExist:
        return Response({"error": "Reporte no encontrado"}, status=404)

    path = os.path.join(settings.BASE_DIR, f"reporte_{reporte.id}.xlsx")

    encabezados = ["Tipo", "Año", "Cliente", "Monto"]
    filas = [[reporte.tipo, reporte.anio, reporte.cliente, ""]]

    generar_excel(path, encabezados, filas)

    return Response({"msg": "Excel generado", "archivo": path})
