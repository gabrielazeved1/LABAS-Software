from decimal import Decimal


class CalculadoraTitulacao:
    """
    Motor de calculo para os elementos obtidos por Titulacao/Volumetria:
    Acidez Trocavel (Al3+) e Acidez Potencial (H+Al).
    Regra padrao do laboratorio: Subtracao direta do valor do Branco.
    """

    def calcular_aluminio(
        self,
        leitura_amostra: Decimal,  # Valor da amostra (Coluna C)
        leitura_branco: Decimal,  # Valor do Branco
    ) -> Decimal:
        """
        Calcula o Aluminio (Al3+) em cmolc/dm3.
        Formula: Leitura da Amostra - Leitura do Branco
        """
        resultado = leitura_amostra - leitura_branco

        # Trava Agronomica de seguranca: Nao existe aluminio/acidez negativa no solo.
        # Caso a leitura seja menor que o branco, o valor disponivel e assumido como zero.
        if resultado < Decimal("0"):
            resultado = Decimal("0")

        return resultado.quantize(Decimal("0.01"))

    def calcular_acidez_potencial(
        self,
        leitura_amostra: Decimal,  # Valor da amostra (Coluna C)
        leitura_branco: Decimal,  # Valor do Branco
    ) -> Decimal:
        """
        Calcula a Acidez Potencial (H+Al) em cmolc/dm3.
        Formula: Leitura da Amostra - Leitura do Branco
        """
        resultado = leitura_amostra - leitura_branco

        # Trava Agronomica de seguranca garantindo que a acidez potencial nunca seja negativa
        if resultado < Decimal("0"):
            resultado = Decimal("0")

        return resultado.quantize(Decimal("0.01"))
