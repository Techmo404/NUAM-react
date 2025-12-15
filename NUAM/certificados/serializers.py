from rest_framework import serializers
from .models import Certificado, CertificadoArchivo, CargaMasivaArchivo


class CertificadoArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificadoArchivo
        fields = (
            "id",
            "nombre_original",
            "tipo",
            "fecha_subida",
        )


class CertificadoSerializer(serializers.ModelSerializer):
    archivos = CertificadoArchivoSerializer(many=True, read_only=True)

    class Meta:
        model = Certificado
        fields = "__all__"
        read_only_fields = ("usuario_asociado", "fecha_ingreso")



class CargaMasivaArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargaMasivaArchivo
        fields = "__all__"

