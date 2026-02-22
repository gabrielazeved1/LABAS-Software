from decimal import Decimal


class LeitorPHmetro:
    """
    Modulo para o equipamento pHmetro.
    A leitura do pH e direta (o valor do visor vai direto para o laudo).
    Este modulo padroniza a entrada e aplica validacoes agronomicas de seguranca
    contra erros de digitacao do operador.
    """

    def registrar_leituras(
        self, ph_agua: Decimal = None, ph_cacl2: Decimal = None, ph_kcl: Decimal = None
    ) -> dict:
        """
        Registra as leituras de pH.
        Como o laboratorio pode nao ler todas as solucoes em uma unica bateria,
        os parametros sao opcionais e tratados de forma independente.
        """
        resultados = {}

        if ph_agua is not None:
            self._validar_escala_ph(ph_agua, "pH em Agua")
            resultados["ph_agua"] = ph_agua.quantize(Decimal("0.01"))

        if ph_cacl2 is not None:
            self._validar_escala_ph(ph_cacl2, "pH em CaCl2")
            resultados["ph_cacl2"] = ph_cacl2.quantize(Decimal("0.01"))

        if ph_kcl is not None:
            self._validar_escala_ph(ph_kcl, "pH em KCl")
            resultados["ph_kcl"] = ph_kcl.quantize(Decimal("0.01"))

        return resultados

    def _validar_escala_ph(self, valor: Decimal, tipo_leitura: str):
        """
        Garante que o valor digitado faz sentido fisicamente (0 a 14).
        Solos normalmente variam de 3 a 9, mas a trava de seguranca
        utiliza a escala quimica padrao completa.
        """
        if valor < Decimal("0") or valor > Decimal("14"):
            # Mantida a string de erro original com acentos para exibicao correta na tela do usuario
            raise ValueError(
                f"Erro de Digitação: O valor de {tipo_leitura} ({valor}) "
                f"está fora da escala real de pH (0 a 14)."
            )
