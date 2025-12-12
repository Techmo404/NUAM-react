from rest_framework import serializers
from .models import Certificado


class CertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = "__all__"
        read_only_fields = ("fecha_ingreso", "usuario_asociado")
