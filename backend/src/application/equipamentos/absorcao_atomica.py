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

    def _descontar_branco(
        self, leitura_bruta: Decimal, leitura_branco: Decimal
    ) -> Decimal:
        """
        Executa o passo da 'Tabela de Absorção'.
        Subtrai o branco da leitura bruta do equipamento.
        """
        return leitura_bruta - leitura_branco

    def _calcular_base(
        self,
        leitura_corrigida: Decimal,
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
            leitura_corrigida - coeficiente_linear_b
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
        leitura_bruta: Decimal,  # Inserido pelo técnico (Esquerda da tabela)
        leitura_branco: Decimal,  # Branco do Ca
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Cálcio (Ca) disponível em cmol_c/dm³."""

        leitura_corrigida = self._descontar_branco(leitura_bruta, leitura_branco)
        peso_ca = Decimal("200")

        return self._calcular_base(
            leitura_corrigida,
            coeficiente_angular_a,
            coeficiente_linear_b,
            volume_extrator_ml,
            fator_diluicao,
            volume_solo_cm3,
            peso_equivalente=peso_ca,
        )

    def calcular_mg_disponivel(
        self,
        leitura_bruta: Decimal,
        leitura_branco: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Magnésio (Mg) disponível em cmol_c/dm³."""

        leitura_corrigida = self._descontar_branco(leitura_bruta, leitura_branco)
        peso_mg = Decimal("120")

        return self._calcular_base(
            leitura_corrigida,
            coeficiente_angular_a,
            coeficiente_linear_b,
            volume_extrator_ml,
            fator_diluicao,
            volume_solo_cm3,
            peso_equivalente=peso_mg,
        )

    def calcular_cu_disponivel(
        self,
        leitura_bruta: Decimal,
        leitura_branco: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Cobre (Cu) disponível em mg/dm³."""

        leitura_corrigida = self._descontar_branco(leitura_bruta, leitura_branco)
        peso_cu_neutro = Decimal("1")

        return self._calcular_base(
            leitura_corrigida,
            coeficiente_angular_a,
            coeficiente_linear_b,
            volume_extrator_ml,
            fator_diluicao,
            volume_solo_cm3,
            peso_equivalente=peso_cu_neutro,
        )

    def calcular_fe_disponivel(
        self,
        leitura_bruta: Decimal,
        leitura_branco: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Ferro (Fe) disponível em mg/dm³."""

        leitura_corrigida = self._descontar_branco(leitura_bruta, leitura_branco)
        peso_fe_neutro = Decimal("1")

        return self._calcular_base(
            leitura_corrigida,
            coeficiente_angular_a,
            coeficiente_linear_b,
            volume_extrator_ml,
            fator_diluicao,
            volume_solo_cm3,
            peso_equivalente=peso_fe_neutro,
        )

    def calcular_mn_disponivel(
        self,
        leitura_bruta: Decimal,
        leitura_branco: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Manganês (Mn) disponível em mg/dm³."""

        leitura_corrigida = self._descontar_branco(leitura_bruta, leitura_branco)
        peso_mn_neutro = Decimal("1")

        return self._calcular_base(
            leitura_corrigida,
            coeficiente_angular_a,
            coeficiente_linear_b,
            volume_extrator_ml,
            fator_diluicao,
            volume_solo_cm3,
            peso_equivalente=peso_mn_neutro,
        )

    def calcular_zn_disponivel(
        self,
        leitura_bruta: Decimal,
        leitura_branco: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Zinco (Zn) disponível em mg/dm³."""

        leitura_corrigida = self._descontar_branco(leitura_bruta, leitura_branco)
        peso_zn_neutro = Decimal("1")

        return self._calcular_base(
            leitura_corrigida,
            coeficiente_angular_a,
            coeficiente_linear_b,
            volume_extrator_ml,
            fator_diluicao,
            volume_solo_cm3,
            peso_equivalente=peso_zn_neutro,
        )
