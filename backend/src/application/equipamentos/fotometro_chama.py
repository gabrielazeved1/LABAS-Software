from decimal import Decimal
from .core_matematico import CurvaRegressaoLinear


class CalculadoraFotometroChama:
    """
    Motor de calculo para os elementos lidos no Fotometro de Chama:
    Potassio (K) e Sodio (Na).
    Le a emissao direta, sem necessidade de conversao logaritmica otica.
    """

    def __init__(self, curva_calibracao: CurvaRegressaoLinear = None):
        """
        Recebe a curva de calibracao padrao gerada pelo motor matematico.
        """
        self.curva = curva_calibracao

    def calcular_k_disponivel(
        self,
        leitura_emissao: Decimal,  # F (Emissao lida pelo aparelho)
        coeficiente_angular_a: Decimal,  # L16 (Inclinacao da reta / b no Excel)
        coeficiente_linear_b: Decimal,  # L17 (Intercepto da reta / a no Excel)
        volume_extrator_ml: Decimal,  # D (50.00)
        fator_diluicao: Decimal,  # E (Variavel)
        volume_solo_cm3: Decimal,  # C (0.005)
    ) -> Decimal:
        """
        Calcula o Potassio (K) disponivel em mg/dm3.
        Formula: ((Emissao - Intercepto) / Inclinacao) * V_extrator * Diluicao / 1000 / V_solo
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matematico: Inclinacao e Volume de Solo nao podem ser zero."
            )

        # 1. Isola a concentracao subtraindo o intercepto (equacao da reta invertida)
        concentracao_extrato = (
            leitura_emissao - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 2. Aplica a estequiometria oficial do laboratorio
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )

        return resultado.quantize(Decimal("0.01"))

    def calcular_na_disponivel(
        self,
        leitura_emissao: Decimal,  # F6 (Emissao lida pelo aparelho)
        coeficiente_angular_a: Decimal,  # L16 (Inclinacao da reta / b no Excel)
        coeficiente_linear_b: Decimal,  # L17 (Intercepto da reta / a no Excel)
        volume_extrator_ml: Decimal,  # D6 (50.00)
        fator_diluicao: Decimal,  # E6 (1)
        volume_solo_cm3: Decimal,  # C6 (0.005)
    ) -> Decimal:
        """
        Calcula o Sodio (Na) disponivel em mg/dm3.
        Formula: ((Emissao - Intercepto) / Inclinacao) * V_extrator * Diluicao / 1000 / V_solo
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matematico: Inclinacao e Volume de Solo nao podem ser zero."
            )

        # 1. Isola a concentracao subtraindo o intercepto
        concentracao_extrato = (
            leitura_emissao - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 2. Aplica a estequiometria do laboratorio
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )

        return resultado.quantize(Decimal("0.01"))
