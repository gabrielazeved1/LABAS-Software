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

        # transmitancia.log10() faz o exato papel do LOG() do Excel
        return Decimal("2") - transmitancia.log10()

    def calcular_b_disponivel(
        self,
        leitura_transmitancia: Decimal,  # F8 (Inserido pelo técnico)
        coeficiente_angular_a: Decimal,  # N16 (Inclinação da reta)
        volume_extrator_ml: Decimal,  # E8 (Fixo: 20)
        fator_diluicao: Decimal,  # D8 (Variável)
        volume_solo_cm3: Decimal,  # C8 (Fixo: 0.01)
    ) -> Decimal:
        """
        Calcula o Boro (B) disponível em mg/dm³.
        Fórmula do Excel: ((2 - LOG(F8)) / Inclinação) * V_extrator * Diluição / 1000 / V_solo
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação da reta e Volume de Solo não podem ser zero."
            )

        # 1. Faz a conversão que o Excel faz na Coluna G
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # 2. Isola a concentração (Absorbância / Inclinação)
        concentracao_extrato = absorvancia / coeficiente_angular_a

        # 3. Aplica a estequiometria
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )

        # Arredonda para 2 casas decimais para o laudo
        return resultado.quantize(Decimal("0.01"))

    def calcular_s_disponivel(
        self,
        leitura_transmitancia: Decimal,  # F (Transmitância inserida)
        coeficiente_angular_a: Decimal,  # Inclinação (b) da reta
        coeficiente_linear_b: Decimal,  # Intercepto (a) da reta <- ADICIONADO NOVAMENTE
        volume_extrator_ml: Decimal,  # V-extrator
        fator_diluicao: Decimal,  # Diluição
        volume_solo_cm3: Decimal,  # V-solo
    ) -> Decimal:
        """
        Calcula o Enxofre (S) disponível em mg/dm³.
        Regra Oficial (Jéssica): Mesma do P-Mehlich. Subtrai o intercepto da absorbância.
        Fórmula: ((2 - LOG(F) - Intercepto) / Inclinação) * V_extrator * Diluição / 1000 / V_solo
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação da reta e Volume de Solo não podem ser zero."
            )

        # 1. Converte Transmitância para Absorbância
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # 2. Isola a concentração subtraindo o intercepto (Ajuste oficial da Jéssica)
        concentracao_extrato = (
            absorvancia - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 3. Aplica a estequiometria
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )

        return resultado.quantize(Decimal("0.01"))

    def calcular_mo_disponivel(
        self,
        leitura_transmitancia: Decimal,  # Coluna F (Transmitância inserida pelo técnico)
    ) -> Decimal:
        """
        Calcula a Matéria Orgânica (MO) em dag/kg.
        Regra Oficial Fixa do Laboratório: (Absorbância + 0.0136) / 0.0729
        """
        # 1. Converte Transmitância para Absorbância (A coluna L do Excel: 2 - LOG(F))
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # 2. Aplica a fórmula cravada do Excel: =(L3+0,0136)/0,0729
        resultado = (absorvancia + Decimal("0.0136")) / Decimal("0.0729")

        # Arredonda para 2 casas decimais para o laudo
        return resultado.quantize(Decimal("0.01"))

    def calcular_p_mehlich_disponivel(
        self,
        leitura_transmitancia: Decimal,  # F8 (Inserido pelo técnico)
        coeficiente_angular_a: Decimal,  # N16 (Inclinação da reta / b no Excel)
        coeficiente_linear_b: Decimal,  # N21 (Intercepto da reta / a no Excel)
        volume_extrator_ml: Decimal,  # E8 (50.00)
        fator_diluicao: Decimal,  # D8 (2.00)
        volume_solo_cm3: Decimal,  # C8 (0.005)
    ) -> Decimal:
        """
        Calcula o Fósforo (P) Mehlich-1 disponível em mg/dm³.
        Fórmula do Excel: ((2 - LOG(F8) - Intercepto) / Inclinação) * V_extrator * Diluição / 1000 / V_solo
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação e Volume de Solo não podem ser zero."
            )

        # 1. Converte Transmitância para Absorbância
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # 2. Isola a concentração usando a reta completa (x = (y - a) / b)
        concentracao_extrato = (
            absorvancia - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 3. Aplica a estequiometria
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )

        return resultado.quantize(Decimal("0.01"))

    def calcular_p_rem(
        self,
        leitura_transmitancia: Decimal,  # F11 (Inserido pelo técnico)
        coeficiente_angular_a: Decimal,  # N16 (Inclinação da reta / b no Excel)
        coeficiente_linear_b: Decimal,  # N17 (Intercepto da reta / a no Excel)
        fator_coluna_e: Decimal,  # E11 (Fator multiplicador, ex: Diluição 50)
    ) -> Decimal:
        """
        Calcula o Fósforo Remanescente (P-rem) em mg/L.
        Fórmula do Excel: ((2 - LOG(F11) - Intercepto) / Inclinação) * E11
        """
        if coeficiente_angular_a == Decimal("0"):
            raise ValueError("Erro Matemático: Inclinação da reta não pode ser zero.")

        # 1. Converte Transmitância para Absorbância
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # 2. Isola a concentração usando a reta completa: x = (y - a) / b
        concentracao_extrato = (
            absorvancia - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 3. Aplica o fator de conversão/diluição (Coluna E da planilha)
        resultado = concentracao_extrato * fator_coluna_e

        return resultado.quantize(Decimal("0.01"))

    def calcular_p_resina_disponivel(
        self,
        leitura_transmitancia: Decimal,  # F6 (Inserido pelo técnico)
        coeficiente_angular_a: Decimal,  # N19 (Inclinação da reta / 'b' no Excel)
        coeficiente_linear_b: Decimal,  # N20 (Intercepto da reta / 'a' no Excel)
        volume_extrator_ml: Decimal,  # E6 (50.00)
        fator_diluicao: Decimal,  # D6 (1)
        volume_solo_cm3: Decimal,  # C6 (0.0025)
    ) -> Decimal:
        """
        Calcula o Fósforo (P) extraído por Resina em mg/dm³.
        Fórmula do Excel: ((2 - LOG(F6) - Intercepto) / Inclinação) * V_extrator * Diluição / 1000 / V_solo
        """
        if coeficiente_angular_a == Decimal("0") or volume_solo_cm3 == Decimal("0"):
            raise ValueError(
                "Erro Matemático: Inclinação da reta e Volume de Solo não podem ser zero."
            )

        # 1. Converte Transmitância para Absorbância
        absorvancia = self._converter_transmitancia_para_absorvancia(
            leitura_transmitancia
        )

        # 2. Isola a concentração subtraindo o intercepto
        concentracao_extrato = (
            absorvancia - coeficiente_linear_b
        ) / coeficiente_angular_a

        # 3. Aplica a estequiometria
        resultado = (
            concentracao_extrato
            * volume_extrator_ml
            * fator_diluicao
            / Decimal("1000")
            / volume_solo_cm3
        )

        return resultado.quantize(Decimal("0.01"))
