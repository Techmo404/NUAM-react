from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsAdmin
from .models import Auditoria
from .serializers import AuditoriaSerializer


def ping(request):
    return JsonResponse({"message": "auditorias OK"})


@api_view(["GET"])
@permission_classes([IsAdmin])
def listar_auditorias(request):
    auditorias = Auditoria.objects.all().order_by("-fecha")
    serializer = AuditoriaSerializer(auditorias, many=True)
    return Response(serializer.data)
