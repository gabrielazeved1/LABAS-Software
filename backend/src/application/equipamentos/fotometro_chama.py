from decimal import Decimal
from .core_matematico import CurvaRegressaoLinear


class CalculadoraFotometroChama:
    """
    Motor de cálculo para os elementos lidos no Fotômetro de Chama:
    Potássio (K) e Sódio (Na).
    Lê a emissão direta, sem necessidade de conversão logarítmica.
    """

    def __init__(self, curva_calibracao: CurvaRegressaoLinear = None):
        self.curva = curva_calibracao

    def calcular_k_disponivel(
        self,
        leitura_emissao: Decimal,  # F (Emissão lida pelo aparelho)
        coeficiente_angular_a: Decimal,  # L16 (Inclinação da reta / b no Excel)
        coeficiente_linear_b: Decimal,  # L17 (Intercepto da reta / a no Excel)
        volume_extrator_ml: Decimal,  # D (50.00)
        fator_diluicao: Decimal,  # E (Variável)
        volume_solo_cm3: Decimal,  # C (0.005)
    ) -> Decimal:
        """
        Calcula o Potássio (K) disponível em mg/dm³.
        Fórmula: ((Emissão - Intercepto) / Inclinação) * V_extrator * Diluição / 1000 / V_solo
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação e Volume de Solo não podem ser zero."
            )

        # 1. Isola a concentração subtraindo o intercepto
        concentracao_extrato = (
            leitura_emissao - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 2. Aplica a estequiometria do laboratório
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
        leitura_emissao: Decimal,  # F6 (Emissão lida pelo aparelho)
        coeficiente_angular_a: Decimal,  # L16 (Inclinação da reta / b no Excel)
        coeficiente_linear_b: Decimal,  # L17 (Intercepto da reta / a no Excel)
        volume_extrator_ml: Decimal,  # D6 (50.00)
        fator_diluicao: Decimal,  # E6 (1)
        volume_solo_cm3: Decimal,  # C6 (0.005)
    ) -> Decimal:
        """
        Calcula o Sódio (Na) disponível em mg/dm³.
        Fórmula: ((Emissão - Intercepto) / Inclinação) * V_extrator * Diluição / 1000 / V_solo
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação e Volume de Solo não podem ser zero."
            )

        # 1. Isola a concentração subtraindo o intercepto
        concentracao_extrato = (
            leitura_emissao - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 2. Aplica a estequiometria do laboratório
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )

        return resultado.quantize(Decimal("0.01"))
