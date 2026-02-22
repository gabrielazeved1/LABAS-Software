from decimal import Decimal


class CurvaRegressaoLinear:
    """
    matematico generico para Regressao Linear Simples.
    Seguindo rigorosamente a padronizacao do laboratorio:
    X = Concentracoes (Padroes), Y = Leituras (Absorbancia/Emissao).
    """

    def __init__(self, valores_x: list[Decimal], valores_y: list[Decimal]):
        """
        Inicializa o calculo da curva validando as entradas e pre-computando
        os somatorios necessarios para as equacoes da regressao.
        """
        if len(valores_x) != len(valores_y):
            raise ValueError("As listas de X e Y devem ter o mesmo tamanho.")
        if len(valores_x) < 2:
            raise ValueError("Minimo de 2 pontos necessarios para formar uma reta.")

        self.valores_x = valores_x
        self.valores_y = valores_y
        self.n = Decimal(len(valores_x))

        # Calculos Base (Somatorios para a equacao dos minimos quadrados)
        self.soma_x = sum(valores_x)
        self.soma_y = sum(valores_y)
        self.soma_xy = sum(x * y for x, y in zip(valores_x, valores_y))
        self.soma_x_quadrado = sum(x**2 for x in valores_x)
        self.soma_y_quadrado = sum(y**2 for y in valores_y)

        # Coeficientes resultantes da regressao
        self.a = self._calcular_inclinacao()
        self.b = self._calcular_interseccao()
        self.r2 = self._calcular_r_quadrado()

    def _calcular_inclinacao(self) -> Decimal:
        """
        Calcula o coeficiente angular 'a' (slope).
        Representa a inclinacao da reta de calibracao.
        """
        numerador = (self.n * self.soma_xy) - (self.soma_x * self.soma_y)
        denominador = (self.n * self.soma_x_quadrado) - (self.soma_x**2)
        if denominador == Decimal("0"):
            raise ValueError(
                "Erro: Leituras identicas impossibilitam a criacao da reta."
            )
        return numerador / denominador

    def _calcular_interseccao(self) -> Decimal:
        """
        Calcula o coeficiente linear 'b' (intercept).
        Representa o ponto onde a reta cruza o eixo Y.
        """
        return (self.soma_y - (self.a * self.soma_x)) / self.n

    def _calcular_r_quadrado(self) -> Decimal:
        """
        Calcula o Coeficiente de Determinacao R2.
        Mede a qualidade do ajuste da reta aos pontos da calibracao (0 a 1).
        """
        media_y = self.soma_y / self.n

        # SS_res = Soma dos quadrados dos residuos (erros de predicao)
        ss_res = sum(
            (
                (y - (self.a * x + self.b)) ** 2
                for x, y in zip(self.valores_x, self.valores_y)
            ),
            Decimal("0"),
        )

        # SS_tot = Soma total dos quadrados (variancia total)
        ss_tot = sum(((y - media_y) ** 2 for y in self.valores_y), Decimal("0"))

        if ss_tot == Decimal("0"):
            return Decimal("1")
        return Decimal("1") - (ss_res / ss_tot)

    def calcular_y(self, x_leitura: Decimal) -> Decimal:
        """
        Aplica a equacao da reta gerada (y = ax + b) para encontrar um valor
        projetado com base em uma nova concentracao.
        """
        return (self.a * x_leitura) + self.b
