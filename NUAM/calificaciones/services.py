# calificaciones/services.py
from decimal import Decimal, InvalidOperation
from certificados.models import Certificado


class CalculoTributarioService:
    """
    Servicio encargado de:
    - Validar certificados
    - Calcular monto final
    - Determinar declaración tributaria
    """

    def __init__(self, certificado: Certificado):
        self.certificado = certificado

    def calcular_factor(self) -> Decimal:
        """
        Define factor según tipo de certificado
        (ejemplo académico, ajustable)
        """
        factores = {
            "A": Decimal("1.10"),
            "B": Decimal("1.05"),
            "C": Decimal("1.00"),
        }
        return factores.get(self.certificado.tipo, Decimal("1.00"))

    def calcular_monto(self) -> Decimal:
        """
        Monto final = monto_bruto - monto_impuesto
        """
        try:
            return self.certificado.monto_bruto - self.certificado.monto_impuesto
        except InvalidOperation:
            raise ValueError("Error en montos del certificado")

    def calcular_declaracion(self) -> dict:
        """
        Retorna el resultado completo del cálculo
        """
        monto_base = self.calcular_monto()
        factor = self.calcular_factor()
        monto_final = monto_base * factor

        return {
            "cliente": self.certificado.cliente,
            "periodo": self.certificado.periodo,
            "tipo_certificado": self.certificado.tipo,
            "monto_base": monto_base,
            "factor": factor,
            "monto_final": monto_final,
        }
