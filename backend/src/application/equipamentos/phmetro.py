from decimal import Decimal


class LeitorPHmetro:
    """
    Módulo para o pHmetro.
    A leitura do pH é direta (o valor do visor vai direto para o laudo).
    Este módulo padroniza a entrada e aplica validações agronômicas de segurança.
    """

    def registrar_leituras(
        self, ph_agua: Decimal = None, ph_cacl2: Decimal = None, ph_kcl: Decimal = None
    ) -> dict:
        """
        Registra as leituras de pH.
        Como o laboratório pode não ler todas as soluções de uma vez,
        os parâmetros são opcionais.
        """
        resultados = {}

        if ph_agua is not None:
            self._validar_escala_ph(ph_agua, "pH em Água")
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
        Solos normalmente variam de 3 a 9, mas travamos na escala química padrão.
        """
        if valor < Decimal("0") or valor > Decimal("14"):
            raise ValueError(
                f"Erro de Digitação: O valor de {tipo_leitura} ({valor}) "
                f"está fora da escala real de pH (0 a 14)."
            )
