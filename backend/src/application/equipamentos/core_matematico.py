from decimal import Decimal


class CurvaRegressaoLinear:
    """
    Motor matemático genérico para Regressão Linear Simples.
    Seguindo rigorosamente: X = Concentrações, Y = Leituras.
    """

    def __init__(self, valores_x: list[Decimal], valores_y: list[Decimal]):
        if len(valores_x) != len(valores_y):
            raise ValueError("As listas de X e Y devem ter o mesmo tamanho.")
        if len(valores_x) < 2:
            raise ValueError("Mínimo de 2 pontos necessários.")

        self.valores_x = valores_x
        self.valores_y = valores_y
        self.n = Decimal(len(valores_x))

        # Cálculos Base
        self.soma_x = sum(valores_x)
        self.soma_y = sum(valores_y)
        self.soma_xy = sum(x * y for x, y in zip(valores_x, valores_y))
        self.soma_x_quadrado = sum(x**2 for x in valores_x)
        self.soma_y_quadrado = sum(y**2 for y in valores_y)

        # Coeficientes
        self.a = self._calcular_inclinacao()
        self.b = self._calcular_interseccao()
        self.r2 = self._calcular_r_quadrado()  # <--- Agora calculando o R²

    def _calcular_inclinacao(self) -> Decimal:
        """Calcula o 'a' (slope)."""
        numerador = (self.n * self.soma_xy) - (self.soma_x * self.soma_y)
        denominador = (self.n * self.soma_x_quadrado) - (self.soma_x**2)
        if denominador == Decimal("0"):
            raise ValueError("Erro: Leituras idênticas impossibilitam a reta.")
        return numerador / denominador

    def _calcular_interseccao(self) -> Decimal:
        """Calcula o 'b' (intercept)."""
        return (self.soma_y - (self.a * self.soma_x)) / self.n

    def _calcular_r_quadrado(self) -> Decimal:
        """Calcula o Coeficiente de Determinação R²."""
        media_y = self.soma_y / self.n
        # SS_res = Soma dos quadrados dos resíduos
        ss_res = sum(
            (
                (y - (self.a * x + self.b)) ** 2
                for x, y in zip(self.valores_x, self.valores_y)
            ),
            Decimal("0"),
        )
        # SS_tot = Soma total dos quadrados
        ss_tot = sum(((y - media_y) ** 2 for y in self.valores_y), Decimal("0"))

        if ss_tot == Decimal("0"):
            return Decimal("1")
        return Decimal("1") - (ss_res / ss_tot)

    def calcular_y(self, x_leitura: Decimal) -> Decimal:
        return (self.a * x_leitura) + self.b
