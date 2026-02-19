from decimal import Decimal


class CurvaRegressaoLinear:
    """
    Motor matemático genérico para Regressão Linear Simples (Método dos Mínimos Quadrados).
    Equação da Reta: y = ax + b

    X = Leituras do equipamento (ex: Absorbância lida pelo fotômetro)
    Y = Concentração conhecida dos Padrões (ex: Padrão Branco, Padrão A, Padrão B)
    """

    def __init__(self, valores_x: list[Decimal], valores_y: list[Decimal]):
        if len(valores_x) != len(valores_y):
            raise ValueError(
                "Erro de Calibração: As listas de X e Y devem ter a mesma quantidade de pontos."
            )
        if len(valores_x) < 2:
            raise ValueError(
                "Erro de Calibração: São necessários pelo menos 2 padrões para traçar a curva."
            )

        self.n = Decimal(len(valores_x))

        # Simulando as colunas da "Tabela Azul" do Excel:
        self.soma_x = sum(valores_x)  # Σx
        self.soma_y = sum(valores_y)  # Σy
        self.soma_xy = sum(x * y for x, y in zip(valores_x, valores_y))  # Σxy
        self.soma_x_quadrado = sum(x**2 for x in valores_x)  # Σx²

        # Resolve a equação
        self.a = self._calcular_inclinacao()
        self.b = self._calcular_interseccao()

    def _calcular_inclinacao(self) -> Decimal:
        """
        Calcula o 'a' (coeficiente angular / inclinação da reta).
        Fórmula: [n(Σxy) - (Σx)(Σy)] / [n(Σx²) - (Σx)²]
        """
        numerador = (self.n * self.soma_xy) - (self.soma_x * self.soma_y)
        denominador = (self.n * self.soma_x_quadrado) - (self.soma_x**2)

        if denominador == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Denominador zero. Os valores de leitura (X) não podem ser todos iguais."
            )

        return numerador / denominador

    def _calcular_interseccao(self) -> Decimal:
        """
        Calcula o 'b' (coeficiente linear / onde a reta corta o eixo y).
        Fórmula: [Σy - a(Σx)] / n
        """
        return (self.soma_y - (self.a * self.soma_x)) / self.n

    def calcular_y(self, x_leitura: Decimal) -> Decimal:
        """
        A Mágica: O técnico digita a Absorbância da amostra (x),
        e a função devolve a Concentração Bruta (y).
        """
        return (self.a * x_leitura) + self.b
