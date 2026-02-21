from decimal import Decimal


class CalculadoraTitulacao:
    """
    Motor de cálculo para os elementos obtidos por Titulação/Volumetria:
    Acidez Trocável (Al3+) e Acidez Potencial (H+Al).
    Regra do Laboratório: Subtração direta do valor do Branco.
    """

    def calcular_aluminio(
        self,
        leitura_amostra: Decimal,  # Valor da amostra (Coluna C)
        leitura_branco: Decimal,  # Valor do Branco
    ) -> Decimal:
        """
        Calcula o Alumínio (Al3+) em cmolc/dm³.
        Fórmula: Leitura da Amostra - Leitura do Branco
        """
        resultado = leitura_amostra - leitura_branco

        # Trava Agronômica: Não existe alumínio/acidez negativa no solo.
        if resultado < Decimal("0"):
            resultado = Decimal("0")

        return resultado.quantize(Decimal("0.01"))

    def calcular_acidez_potencial(
        self,
        leitura_amostra: Decimal,  # Valor da amostra (Coluna C)
        leitura_branco: Decimal,  # Valor do Branco
    ) -> Decimal:
        """
        Calcula a Acidez Potencial (H+Al) em cmolc/dm³.
        Fórmula: Leitura da Amostra - Leitura do Branco
        """
        resultado = leitura_amostra - leitura_branco

        if resultado < Decimal("0"):
            resultado = Decimal("0")

        return resultado.quantize(Decimal("0.01"))
