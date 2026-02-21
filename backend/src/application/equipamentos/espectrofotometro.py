from decimal import Decimal
from .core_matematico import CurvaRegressaoLinear


class CalculadoraEspectrofotometro:
    """
    Motor de cálculo para os elementos lidos no Espectrofotômetro.
    Possui inteligência para converter Transmitância em Absorbância usando logaritmo.
    """

    def __init__(self, curva_calibracao: CurvaRegressaoLinear = None):
        self.curva = curva_calibracao

    def _converter_transmitancia_para_absorvancia(
        self, transmitancia: Decimal
    ) -> Decimal:
        """Aplica a Lei de Beer-Lambert: Abs = 2 - log10(T%)"""
        if transmitancia <= Decimal("0"):
            raise ValueError(
                "Erro: A transmitância lida pelo aparelho deve ser maior que zero."
            )
        return Decimal("2") - transmitancia.log10()

    def calcular_mo_disponivel(self, leitura_transmitancia: Decimal) -> Decimal:
        """Fórmula fixa: =(L3+0,0136)/0,0729"""
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )
        resultado = (absorvancia + Decimal("0.0136")) / Decimal("0.0729")
        return resultado.quantize(Decimal("0.01"))

    # 👇 REVISADO PARA ESPELHAR A SINTAXE EXATA DA ESTEQUIOMETRIA 👇
    def calcular_p_mehlich_disponivel(
        self,
        leitura_transmitancia: Decimal,
        coeficiente_angular_a: Decimal,  # Inclinação
        coeficiente_linear_b: Decimal,  # Intercepto
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação e Volume de Solo não podem ser zero."
            )

        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # MUDANÇA: Linha de cálculo agrupada para evitar perda de precisão e espelhar a planilha
        resultado = (
            ((absorvancia - coeficiente_linear_b) / coeficiente_angular_a)
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )
        return resultado.quantize(Decimal("0.01"))

    # 👇 FÓRMULA EXATA DO EXCEL: =(G10-N$17)/N$16*E10 👇
    def calcular_p_rem(
        self,
        leitura_transmitancia: Decimal,  # G10 (Transformado em Abs)
        coeficiente_angular_a: Decimal,  # N$16 (Inclinação)
        coeficiente_linear_b: Decimal,  # N$17 (Intercepto)
        fator_coluna_e: Decimal,  # E10 (Fator / Vol Extrator)
    ) -> Decimal:
        """Calcula o Fósforo Remanescente (P-rem) em mg/L ignorando peso/volume do solo."""
        if coeficiente_angular_a == Decimal("0"):
            raise ValueError("Erro Matemático: Inclinação da reta não pode ser zero.")

        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # (G10 - N$17) / N$16
        concentracao_extrato = (
            absorvancia - coeficiente_linear_b
        ) / coeficiente_angular_a

        # * E10
        resultado = concentracao_extrato * fator_coluna_e
        return resultado.quantize(Decimal("0.01"))

    # 👇 REVISADO COM A FÓRMULA EXATA DO EXCEL: =((G11-N$20)/N$19)*E11*D11/1000/C11 👇
    def calcular_p_resina_disponivel(
        self,
        leitura_transmitancia: Decimal,  # G11 (Transformado em Abs)
        coeficiente_angular_a: Decimal,  # N$19 (Inclinação)
        coeficiente_linear_b: Decimal,  # N$20 (Intercepto)
        volume_extrator_ml: Decimal,  # E11 (Planilha original tratava extrator aqui)
        fator_diluicao: Decimal,  # D11 (Planilha original tratava diluição aqui)
        volume_solo_cm3: Decimal,  # C11
    ) -> Decimal:
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação da reta e Volume de Solo não podem ser zero."
            )

        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # MUDANÇA: Sintaxe idêntica à do P-Mehlich para evitar desvios no ponto flutuante
        resultado = (
            ((absorvancia - coeficiente_linear_b) / coeficiente_angular_a)
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )
        return resultado.quantize(Decimal("0.01"))

    def calcular_s_disponivel(
        self,
        leitura_transmitancia: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação da reta e Volume de Solo não podem ser zero."
            )
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )
        concentracao_extrato = (
            absorvancia - coeficiente_linear_b
        ) / coeficiente_angular_a
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )
        return resultado.quantize(Decimal("0.01"))

    def calcular_b_disponivel(
        self,
        leitura_transmitancia: Decimal,
        coeficiente_angular_a: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação da reta e Volume de Solo não podem ser zero."
            )
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )
        concentracao_extrato = absorvancia / coeficiente_angular_a
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )
        return resultado.quantize(Decimal("0.01"))
