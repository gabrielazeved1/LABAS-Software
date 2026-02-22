from decimal import Decimal
from .core_matematico import CurvaRegressaoLinear


class CalculadoraAbsorcaoAtomica:
    """
    Motor de calculo para os equipamentos de Absorcao Atomica.
    Transforma a leitura de luz (Absorbancia) na concentracao de nutrientes no solo.
    """

    def __init__(self, curva_calibracao: CurvaRegressaoLinear = None):
        # A curva gerada pela calibracao dos padroes
        self.curva = curva_calibracao

    def _descontar_branco(
        self, leitura_bruta: Decimal, leitura_branco: Decimal
    ) -> Decimal:
        """
        Executa o passo da Tabela de Absorcao.
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
        Aplica a estequiometria exata da extracao:
        Concentracao no extrato = (Leitura - Intercepto) / Inclinacao
        Disponivel no Solo = (Concentracao * Vol Extrator * Diluicao) / (1000 * PE * Vol Solo)
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matematico: Inclinacao da reta e Volume de Solo nao podem ser zero."
            )

        # 1. Isola o 'x' na equacao da reta: x = (y - b) / a
        concentracao_extrato = (
            leitura_corrigida - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 2. Aplica as conversoes fisicas e quimicas
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / peso_equivalente
            / volume_solo_cm3
        )

        # Arredonda para 2 casas decimais (Padrao de laboratorio)
        return resultado.quantize(Decimal("0.01"))

    def calcular_ca_disponivel(
        self,
        leitura_bruta: Decimal,
        leitura_branco: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """Calcula o Calcio (Ca) disponivel em cmol_c/dm3."""

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
        """Calcula o Magnesio (Mg) disponivel em cmol_c/dm3."""

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
        """Calcula o Cobre (Cu) disponivel em mg/dm3."""

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
        """Calcula o Ferro (Fe) disponivel em mg/dm3."""

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
        """Calcula o Manganes (Mn) disponivel em mg/dm3."""

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
        """Calcula o Zinco (Zn) disponivel em mg/dm3."""

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
