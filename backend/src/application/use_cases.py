from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class CalculadoraAnaliseSolo:
    """
    Caso de Uso (Use Case) responsavel por abstrair as formulas da Planilha Mestra.
    Garante a integridade dos calculos agronomicos finais do laudo.
    Aderente ao SRP (Principio da Responsabilidade Unica).
    """

    @staticmethod
    def _to_decimal(valor) -> Decimal:
        """
        Converte entradas para Decimal para evitar erros de ponto flutuante.
        Garante que valores nulos ou invalidos sejam tratados como zero matematico.
        """
        if valor is None:
            return Decimal("0.00")
        try:
            return Decimal(str(valor))
        except (ValueError, InvalidOperation):
            return Decimal("0.00")

    def calcular_resultados_completos(self, k_mg, ca, mg, al, h_al, mo) -> dict:
        """
        Executa a logica exata da planilha mestra do laboratorio.
        Equivalencia na planilha: Hn=K, Jn=Ca, Kn=Mg, Ln=Al, Mn=H+Al, Z4=MO
        """
        # 1. Normalizacao de dados (Tratamento de nulos para zero)
        _k_mg = self._to_decimal(k_mg)
        _ca = self._to_decimal(ca)
        _mg = self._to_decimal(mg)
        _al = self._to_decimal(al)
        _h_al = self._to_decimal(h_al)
        _mo = self._to_decimal(mo)

        # 2. Conversao estequiometrica do Potassio (K) de mg/dm3 para cmolc/dm3 (Fator 390)
        k_cmol = _k_mg / Decimal("390")

        # 3. Calculo do Complexo de Troca (Soma de Bases e CTC)
        sb = k_cmol + _ca + _mg  # Nn = (Hn/390) + Jn + Kn
        t_efetiva = sb + _al  # On = Nn + Ln
        t_ph7 = sb + _h_al  # Pn = Nn + Mn

        # 4. Calculo das Saturacoes (V% e m%)
        v_perc = (
            (sb / t_ph7 * Decimal("100")) if t_ph7 > Decimal("0") else Decimal("0.0")
        )
        m_perc = (
            (_al / t_efetiva * Decimal("100"))
            if t_efetiva > Decimal("0")
            else Decimal("0.0")
        )

        # 5. Calculo das Relacoes Agronomicas e Carbono
        ca_mg = (_ca / _mg) if _mg > Decimal("0") else Decimal("0.0")
        ca_k = (_ca / k_cmol) if k_cmol > Decimal("0") else Decimal("0.0")
        mg_k = (_mg / k_cmol) if k_cmol > Decimal("0") else Decimal("0.0")
        c_org = _mo / Decimal("1.72")

        # 6. Retorno padronizado com arredondamento cientifico (ROUND_HALF_UP)
        return {
            "sb": sb.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "t": t_efetiva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "T": t_ph7.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "V": v_perc.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP),
            "m": m_perc.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP),
            "ca_mg": ca_mg.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "ca_k": ca_k.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "mg_k": mg_k.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "c_org": c_org.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        }
