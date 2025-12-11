import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

def serializar_instancia(instance):
    """
    Convierte un modelo a un dict válido para JSONField,
    evitando errores con datetime, decimal, etc.
    """
    datos = model_to_dict(instance)
    return json.loads(json.dumps(datos, cls=DjangoJSONEncoder))
