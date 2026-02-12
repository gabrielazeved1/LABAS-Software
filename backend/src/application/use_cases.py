from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class CalculadoraAnaliseSolo:
    """
    abstrair as formulas da Planilha Mestra para garantir integridade
    srp
    """

    @staticmethod
    def _to_decimal(valor):
        """converte entradas para decimal para evitar erros de ponto flutuante
        nunca usar ponto flutuante se eu precisar de precisão
        """
        if valor is None:
            return Decimal("0.00")
        try:
            return Decimal(str(valor))
        except (ValueError, InvalidOperation):
            return Decimal("0.00")

    def calcular_resultados_completos(self, k_mg, ca, mg, al, h_al, mo):
        """
        executa a logica exata da planilha mestra
        Hn=K, Jn=Ca, Kn=Mg, Ln=Al, Mn=H+Al, Z4=MO
        """
        #  normalizar de dados (inputs)
        _k_mg = self._to_decimal(k_mg)
        _ca = self._to_decimal(ca)
        _mg = self._to_decimal(mg)
        _al = self._to_decimal(al)
        _h_al = self._to_decimal(h_al)
        _mo = self._to_decimal(mo)

        # conversao de potassio (Hn/390)
        k_cmol = _k_mg / Decimal("390")

        # complexo de troca (SB, t, T)
        sb = k_cmol + _ca + _mg  # Nn = (Hn/390) + Jn + Kn
        t_efetiva = sb + _al  # On = Nn + Ln
        t_ph7 = sb + _h_al  # Pn = Nn + Mn

        # saturações (V% e m%)
        v_perc = (sb / t_ph7 * 100) if t_ph7 > 0 else Decimal("0.0")  # (Nn/Pn)*100
        m_perc = (
            (_al / t_efetiva * 100) if t_efetiva > 0 else Decimal("0.0")
        )  # (Ln/On)*100

        # relaçoes e carbono (Ca/Mg, Ca/K, Mg/K, C-org)
        ca_mg = (_ca / _mg) if _mg > 0 else Decimal("0.0")  # Jn / Kn
        ca_k = (_ca / k_cmol) if k_cmol > 0 else Decimal("0.0")  # Jn / (Hn/390)
        mg_k = (_mg / k_cmol) if k_cmol > 0 else Decimal("0.0")  # Kn / (Hn/390)
        c_org = _mo / Decimal("1.72")  # Z4 / 1,72

        # apenas 2 casas decimais e arredondar para manter precisao cientifica, pra cima
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
