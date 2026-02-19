from decimal import Decimal
from .core_matematico import CurvaRegressaoLinear


class CalculadoraAbsorcaoAtomica:
    """
    Motor de cálculo para os equipamentos de Absorção Atômica.
    Transforma a leitura de luz (Absorbância) na concentração de nutrientes no solo.
    """

    def __init__(self, curva_calibracao: CurvaRegressaoLinear = None):
        # A curva gerada de manhã pela calibração dos padrões
        self.curva = curva_calibracao

    def _calcular_base(
        self,
        leitura_absorvancia: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
        peso_equivalente: Decimal,
    ) -> Decimal:
        """
        Aplica a estequiometria exata da extração:
        Concentração no extrato = (Leitura - Intercepto) / Inclinação
        Disponível no Solo = (Concentração * Vol Extrator * Diluição) / (1000 * PE * Vol Solo)
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação da reta e Volume de Solo não podem ser zero."
            )

        # 1. Isola o 'x' na equação da reta: x = (y - b) / a
        concentracao_extrato = (
            leitura_absorvancia - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 2. Aplica as conversões físicas e químicas
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / peso_equivalente
            / volume_solo_cm3
        )

        # Arredonda para 2 casas decimais (Padrão de laboratório)
        return resultado.quantize(Decimal("0.01"))

    def calcular_ca_disponivel(
        self,
        leitura_absorvancia: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Cálcio (Ca) disponível em cmol_c/dm³."""

        peso_ca = Decimal("200")

        return self._calcular_base(
            leitura_absorvancia,
            coeficiente_angular_a,
            coeficiente_linear_b,
            volume_extrator_ml,
            fator_diluicao,
            volume_solo_cm3,
            peso_equivalente=peso_ca,
        )

    def calcular_mg_disponivel(
        self,
        leitura_absorvancia: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Magnésio (Mg) disponível em cmol_c/dm³."""

        peso_mg = Decimal("120")

        return self._calcular_base(
            leitura_absorvancia,
            coeficiente_angular_a,
            coeficiente_linear_b,
            volume_extrator_ml,
            fator_diluicao,
            volume_solo_cm3,
            peso_equivalente=peso_mg,
        )
