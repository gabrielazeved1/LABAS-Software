from decimal import Decimal
from .core_matematico import CurvaRegressaoLinear


class CalculadoraEspectrofotometro:
    """
    Motor de calculo para os elementos lidos no Espectrofotometro.
    Possui inteligencia para converter Transmitancia em Absorbancia usando logaritmo,
    conforme a Lei de Beer-Lambert.
    """

    def __init__(self, curva_calibracao: CurvaRegressaoLinear = None):
        self.curva = curva_calibracao

    def _converter_transmitancia_para_absorvancia(
        self, transmitancia: Decimal
    ) -> Decimal:
        """
        Aplica a Lei de Beer-Lambert para conversao otica: Abs = 2 - log10(T%)
        """
        if transmitancia <= Decimal("0"):
            raise ValueError(
                "Erro: A transmitancia lida pelo aparelho deve ser maior que zero."
            )
        return Decimal("2") - transmitancia.log10()

    def calcular_mo_disponivel(self, leitura_transmitancia: Decimal) -> Decimal:
        """
        Calcula a Materia Organica (MO).
        Formula fixa padrao do laboratorio: =(Absorbancia + 0.0136) / 0.0729
        """
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )
        resultado = (absorvancia + Decimal("0.0136")) / Decimal("0.0729")
        return resultado.quantize(Decimal("0.01"))

    def calcular_p_mehlich_disponivel(
        self,
        leitura_transmitancia: Decimal,
        coeficiente_angular_a: Decimal,  # Inclinacao - usei o padrao
        coeficiente_linear_b: Decimal,  # Intercepto
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """
        Calcula o Fosforo (P) extraido por Mehlich-1.
        Agrupamento de operacoes para evitar perda de precisao decimal.
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matematico: Inclinacao e Volume de Solo nao podem ser zero."
            )

        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        resultado = (
            ((absorvancia - coeficiente_linear_b) / coeficiente_angular_a)
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )
        return resultado.quantize(Decimal("0.01"))

    def calcular_p_rem(
        self,
        leitura_transmitancia: Decimal,  # Transformado em Absorbancia internamente
        coeficiente_angular_a: Decimal,  # Inclinacao
        coeficiente_linear_b: Decimal,  # Intercepto
        fator_coluna_e: Decimal,  # Fator / Vol Extrator / Diluicao combinados
    ) -> Decimal:
        """
        Calcula o Fosforo Remanescente (P-rem) em mg/L.
        Ignora peso/volume do solo, aplicando multiplicador direto da tabela.
        Formula exata do Excel correspondente: =(G10-N$17)/N$16*E10
        """
        if coeficiente_angular_a == Decimal("0"):
            raise ValueError("Erro Matematico: Inclinacao da reta nao pode ser zero.")

        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        concentracao_extrato = (
            absorvancia - coeficiente_linear_b
        ) / coeficiente_angular_a

        resultado = concentracao_extrato * fator_coluna_e
        return resultado.quantize(Decimal("0.01"))

    def calcular_p_resina_disponivel(
        self,
        leitura_transmitancia: Decimal,
        coeficiente_angular_a: Decimal,
        coeficiente_linear_b: Decimal,
        volume_extrator_ml: Decimal,
        fator_diluicao: Decimal,
        volume_solo_cm3: Decimal,
    ) -> Decimal:
        """
        Calcula o Fosforo (P) extraido por Resina de Troca Ionica.
        Estrutura alinhada com P-Mehlich para prevencao de desvios de ponto flutuante.
        Formula exata do Excel: =((G11-N$20)/N$19)*E11*D11/1000/C11
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matematico: Inclinacao da reta e Volume de Solo nao podem ser zero."
            )

        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

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
        """
        Calcula o Enxofre (S) disponivel.
        Realiza a conversao otica, isola a concentracao descontando o intercepto,
        e aplica a estequiometria final.
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matematico: Inclinacao da reta e Volume de Solo nao podem ser zero."
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
        """
        Calcula o Boro (B) disponivel.
        Diferente dos demais, nao desconta o intercepto na logica padrao,
        dividindo a absorbancia diretamente pela inclinacao.
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matematico: Inclinacao da reta e Volume de Solo nao podem ser zero."
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
