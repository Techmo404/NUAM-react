# mensajes/serializers.py
from rest_framework import serializers
from .models import Mensaje, ArchivoMensaje

class ArchivoMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoMensaje
        fields = ["id", "nombre_original", "creado"]


class MensajeSerializer(serializers.ModelSerializer):
    archivos = ArchivoMensajeSerializer(many=True, read_only=True)

    # Info útil del certificado (si viene)
    certificado_id = serializers.IntegerField(source="certificado.id", read_only=True)
    certificado_cliente = serializers.CharField(source="certificado.cliente", read_only=True)
    certificado_periodo = serializers.CharField(source="certificado.periodo", read_only=True)
    certificado_tipo = serializers.CharField(source="certificado.tipo", read_only=True)

    emisor_username = serializers.CharField(source="emisor.username", read_only=True)
    emisor_email = serializers.CharField(source="emisor.email", read_only=True)

    respondido_por_username = serializers.CharField(source="respondido_por.username", read_only=True)

    class Meta:
        model = Mensaje
        fields = [
            "id",
            "asunto",
            "contenido",
            "estado",
            "creado",

            "certificado_id",
            "certificado_cliente",
            "certificado_periodo",
            "certificado_tipo",

            "leido_por_admin",
            "leido_por_emisor",

            "respuesta",
            "respondido_por_username",
            "respondido_en",

            "emisor_username",
            "emisor_email",

            "archivos",
        ]
