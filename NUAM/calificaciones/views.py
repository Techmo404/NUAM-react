from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsAdmin, IsEmployee
from django.http import JsonResponse

def ping(request):
    return JsonResponse({"message": "calificaciones OK"})

@api_view(["GET"])
@permission_classes([IsAdmin])
def lista_calificaciones(request):
    return Response({"msg": "Solo admins pueden ver TODAS las calificaciones"})


@api_view(["GET"])
@permission_classes([IsEmployee])
def mis_calificaciones(request):
    return Response({"msg": "Los empleados solo ven sus propios datos"})
