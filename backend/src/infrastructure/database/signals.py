# from django.db.models.signals import pre_save, post_save, post_delete
# from django.dispatch import receiver
# from decimal import Decimal
# from .models import AnaliseSolo, LeituraEquipamento, PontoCalibracao

# from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica
# from src.application.equipamentos.fotometro_chama import CalculadoraFotometroChama
# from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
# from src.application.equipamentos.phmetro import LeitorPHmetro
# from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro

# # =============================================================================
# # 1. CÁLCULO DA CURVA DE CALIBRAÇÃO
# # =============================================================================


# @receiver([post_save, post_delete], sender=PontoCalibracao)
# def atualizar_equacao_da_bateria(sender, instance, **kwargs):
#     bateria = instance.bateria
#     pontos = bateria.pontos.all()

#     if pontos.count() >= 2:
#         x_padroes = [p.concentracao for p in pontos]

#         if bateria.equipamento == "ES":
#             y_lidos = []
#             for p in pontos:
#                 if p.absorvancia <= Decimal("0"):
#                     bateria.coeficiente_angular_a = bateria.coeficiente_linear_b = (
#                         bateria.r_quadrado
#                     ) = None
#                     bateria.save()
#                     return
#                 # Converte Transmitância lida na curva para Absorbância
#                 y_lidos.append(Decimal("2") - p.absorvancia.log10())
#         else:
#             y_lidos = [p.absorvancia for p in pontos]

#         try:
#             motor = CurvaRegressaoLinear(valores_x=x_padroes, valores_y=y_lidos)
#             bateria.coeficiente_angular_a = motor.a
#             bateria.coeficiente_linear_b = motor.b
#             bateria.r_quadrado = motor.r2.quantize(Decimal("0.000001"))
#             bateria.save()
#         except Exception as e:
#             print(f"⚠️ Erro curva: {e}")
#     else:
#         bateria.coeficiente_angular_a = bateria.coeficiente_linear_b = (
#             bateria.r_quadrado
#         ) = None
#         bateria.save()


# # =============================================================================
# # 2. CÁLCULOS AGRONÔMICOS DO LAUDO
# # =============================================================================


# @receiver(pre_save, sender=AnaliseSolo)
# def calcular_relacoes_agronomicas(sender, instance, **kwargs):
#     k_cmolc = (instance.k / Decimal("390")) if instance.k else Decimal("0")
#     if instance.ca is not None and instance.mg is not None and instance.k is not None:
#         instance.sb = (instance.ca + instance.mg + k_cmolc).quantize(Decimal("0.01"))
#     if instance.sb is not None and instance.al is not None:
#         instance.t = (instance.sb + instance.al).quantize(Decimal("0.01"))
#     if instance.sb is not None and instance.h_al is not None:
#         instance.T_maiusculo = (instance.sb + instance.h_al).quantize(Decimal("0.01"))
#     if instance.sb is not None and instance.T_maiusculo and instance.T_maiusculo > 0:
#         instance.V = ((instance.sb / instance.T_maiusculo) * Decimal("100")).quantize(
#             Decimal("0.1")
#         )
#     if instance.al is not None and instance.t and instance.t > 0:
#         instance.m = ((instance.al / instance.t) * Decimal("100")).quantize(
#             Decimal("0.1")
#         )
#     if instance.ca and instance.mg and instance.mg > 0:
#         instance.ca_mg = (instance.ca / instance.mg).quantize(Decimal("0.01"))
#     if instance.ca and k_cmolc > 0:
#         instance.ca_k = (instance.ca / k_cmolc).quantize(Decimal("0.01"))
#     if instance.mg and k_cmolc > 0:
#         instance.mg_k = (instance.mg / k_cmolc).quantize(Decimal("0.01"))
#     if instance.mo:
#         instance.c_org = (instance.mo / Decimal("1.72")).quantize(Decimal("0.01"))


# # =============================================================================
# # 3. ROBÔ DE PROCESSAMENTO
# # =============================================================================


# @receiver(post_save, sender=LeituraEquipamento)
# def automatizar_calculo_equipamentos(sender, instance, created, **kwargs):
#     bateria = instance.bateria
#     laudo = instance.analise
#     resultado = None
#     campo_laudo = None

#     # Variáveis brutas sem valores padrões
#     vol_solo = bateria.volume_solo
#     vol_extrator = bateria.volume_extrator
#     diluicao = instance.fator_diluicao

#     # 🚨 MUDANÇA: TRAVA GLOBAL NO BACK-END PARA AA, FC, ES
#     # Mesmo que a tela passe, o robô recusa calcular se faltar qualquer um dos 3.
#     if bateria.equipamento in ["AA", "FC", "ES"]:
#         if vol_solo is None or vol_extrator is None or diluicao is None:
#             print(
#                 f"⚠️ [BLOQUEIO GLOBAL] Falha ao processar {bateria.elemento}. V-Solo, V-Extrator ou Diluição ausentes."
#             )
#             return

#     # 🔵 PHGÂMETRO (Passa direto pela trava acima)
#     if bateria.equipamento == "PH":
#         maquina_ph = LeitorPHmetro()
#         if "ph_agua" in bateria.elemento:
#             resultado, campo_laudo = (
#                 maquina_ph.registrar_leituras(ph_agua=instance.leitura_bruta).get(
#                     "ph_agua"
#                 ),
#                 "ph_agua",
#             )
#         elif "ph_cacl2" in bateria.elemento:
#             resultado, campo_laudo = (
#                 maquina_ph.registrar_leituras(ph_cacl2=instance.leitura_bruta).get(
#                     "ph_cacl2"
#                 ),
#                 "ph_cacl2",
#             )
#         elif "ph_kcl" in bateria.elemento:
#             resultado, campo_laudo = (
#                 maquina_ph.registrar_leituras(ph_kcl=instance.leitura_bruta).get(
#                     "ph_kcl"
#                 ),
#                 "ph_kcl",
#             )

#     # 🟡 ESPECTROFOTÔMETRO
#     elif bateria.equipamento == "ES":
#         maquina_es = CalculadoraEspectrofotometro()

#         if bateria.elemento == "MO":
#             resultado, campo_laudo = (
#                 maquina_es.calcular_mo_disponivel(instance.leitura_bruta),
#                 "mo",
#             )

#         elif (
#             bateria.coeficiente_angular_a is not None
#             and bateria.coeficiente_linear_b is not None
#         ):
#             # P_rem passa a Diluição (E10) como fator multiplicador para o motor matemático
#             if bateria.elemento == "P_rem":
#                 resultado = maquina_es.calcular_p_rem(
#                     leitura_transmitancia=instance.leitura_bruta,
#                     coeficiente_angular_a=bateria.coeficiente_angular_a,
#                     coeficiente_linear_b=bateria.coeficiente_linear_b,
#                     fator_coluna_e=diluicao,
#                 )
#                 campo_laudo = "p_rem"

#             elif bateria.elemento == "P_R":
#                 resultado = maquina_es.calcular_p_resina_disponivel(
#                     instance.leitura_bruta,
#                     bateria.coeficiente_angular_a,
#                     bateria.coeficiente_linear_b,
#                     vol_extrator,
#                     diluicao,
#                     vol_solo,
#                 )
#                 campo_laudo = "p_r"

#             elif bateria.elemento == "P_M":
#                 resultado = maquina_es.calcular_p_mehlich_disponivel(
#                     instance.leitura_bruta,
#                     bateria.coeficiente_angular_a,
#                     bateria.coeficiente_linear_b,
#                     vol_extrator,
#                     diluicao,
#                     vol_solo,
#                 )
#                 campo_laudo = "p_m"

#             elif bateria.elemento == "S":
#                 resultado = maquina_es.calcular_s_disponivel(
#                     instance.leitura_bruta,
#                     bateria.coeficiente_angular_a,
#                     bateria.coeficiente_linear_b,
#                     vol_extrator,
#                     diluicao,
#                     vol_solo,
#                 )
#                 campo_laudo = "s"

#             elif bateria.elemento == "B":
#                 resultado = maquina_es.calcular_b_disponivel(
#                     instance.leitura_bruta,
#                     bateria.coeficiente_angular_a,
#                     vol_extrator,
#                     diluicao,
#                     vol_solo,
#                 )
#                 campo_laudo = "b"

#     # 🟢 ABSORÇÃO ATÔMICA
#     elif (
#         bateria.equipamento == "AA"
#         and bateria.leitura_branco is not None
#         and bateria.coeficiente_angular_a is not None
#     ):
#         maquina_aa = CalculadoraAbsorcaoAtomica()
#         elem = bateria.elemento.lower()
#         if hasattr(maquina_aa, f"calcular_{elem}_disponivel"):
#             resultado, campo_laudo = (
#                 getattr(maquina_aa, f"calcular_{elem}_disponivel")(
#                     instance.leitura_bruta,
#                     bateria.leitura_branco,
#                     bateria.coeficiente_angular_a,
#                     bateria.coeficiente_linear_b,
#                     vol_extrator,
#                     diluicao,
#                     vol_solo,
#                 ),
#                 elem,
#             )

#     # 🔴 FOTÔMETRO DE CHAMA
#     elif bateria.equipamento == "FC" and bateria.coeficiente_angular_a is not None:
#         maquina_fc = CalculadoraFotometroChama()
#         elem = bateria.elemento.lower()
#         resultado, campo_laudo = (
#             getattr(maquina_fc, f"calcular_{elem}_disponivel")(
#                 instance.leitura_bruta,
#                 bateria.coeficiente_angular_a,
#                 bateria.coeficiente_linear_b,
#                 vol_extrator,
#                 diluicao,
#                 vol_solo,
#             ),
#             elem,
#         )

#     # 💾 SALVAMENTO NO LAUDO
#     if resultado is not None and campo_laudo is not None:
#         if resultado < 0:
#             resultado = Decimal("0.00")
#         setattr(laudo, campo_laudo, resultado)
#         laudo.save()
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from .models import AnaliseSolo, LeituraEquipamento, PontoCalibracao

from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica
from src.application.equipamentos.fotometro_chama import CalculadoraFotometroChama
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.phmetro import LeitorPHmetro
from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro
from src.application.equipamentos.titulacao import (
    CalculadoraTitulacao,
)  # ADIÇÃO: Import do motor de Titulação

# =============================================================================
# 1. CÁLCULO DA CURVA DE CALIBRAÇÃO
# =============================================================================


@receiver([post_save, post_delete], sender=PontoCalibracao)
def atualizar_equacao_da_bateria(sender, instance, **kwargs):
    bateria = instance.bateria
    pontos = bateria.pontos.all()

    if pontos.count() >= 2:
        x_padroes = [p.concentracao for p in pontos]

        if bateria.equipamento == "ES":
            y_lidos = []
            for p in pontos:
                if p.absorvancia <= Decimal("0"):
                    bateria.coeficiente_angular_a = bateria.coeficiente_linear_b = (
                        bateria.r_quadrado
                    ) = None
                    bateria.save()
                    return
                # Converte Transmitância lida na curva para Absorbância
                y_lidos.append(Decimal("2") - p.absorvancia.log10())
        else:
            y_lidos = [p.absorvancia for p in pontos]

        try:
            motor = CurvaRegressaoLinear(valores_x=x_padroes, valores_y=y_lidos)
            bateria.coeficiente_angular_a = motor.a
            bateria.coeficiente_linear_b = motor.b
            bateria.r_quadrado = motor.r2.quantize(Decimal("0.000001"))
            bateria.save()
        except Exception as e:
            print(f"⚠️ Erro curva: {e}")
    else:
        bateria.coeficiente_angular_a = bateria.coeficiente_linear_b = (
            bateria.r_quadrado
        ) = None
        bateria.save()


# =============================================================================
# 2. CÁLCULOS AGRONÔMICOS DO LAUDO
# =============================================================================


@receiver(pre_save, sender=AnaliseSolo)
def calcular_relacoes_agronomicas(sender, instance, **kwargs):
    k_cmolc = (instance.k / Decimal("390")) if instance.k else Decimal("0")
    if instance.ca is not None and instance.mg is not None and instance.k is not None:
        instance.sb = (instance.ca + instance.mg + k_cmolc).quantize(Decimal("0.01"))
    if instance.sb is not None and instance.al is not None:
        instance.t = (instance.sb + instance.al).quantize(Decimal("0.01"))
    if instance.sb is not None and instance.h_al is not None:
        instance.T_maiusculo = (instance.sb + instance.h_al).quantize(Decimal("0.01"))
    if instance.sb is not None and instance.T_maiusculo and instance.T_maiusculo > 0:
        instance.V = ((instance.sb / instance.T_maiusculo) * Decimal("100")).quantize(
            Decimal("0.1")
        )
    if instance.al is not None and instance.t and instance.t > 0:
        instance.m = ((instance.al / instance.t) * Decimal("100")).quantize(
            Decimal("0.1")
        )
    if instance.ca and instance.mg and instance.mg > 0:
        instance.ca_mg = (instance.ca / instance.mg).quantize(Decimal("0.01"))
    if instance.ca and k_cmolc > 0:
        instance.ca_k = (instance.ca / k_cmolc).quantize(Decimal("0.01"))
    if instance.mg and k_cmolc > 0:
        instance.mg_k = (instance.mg / k_cmolc).quantize(Decimal("0.01"))
    if instance.mo:
        instance.c_org = (instance.mo / Decimal("1.72")).quantize(Decimal("0.01"))


# =============================================================================
# 3. ROBÔ DE PROCESSAMENTO
# =============================================================================


@receiver(post_save, sender=LeituraEquipamento)
def automatizar_calculo_equipamentos(sender, instance, created, **kwargs):
    bateria = instance.bateria
    laudo = instance.analise
    resultado = None
    campo_laudo = None

    # Variáveis brutas sem valores padrões
    vol_solo = bateria.volume_solo
    vol_extrator = bateria.volume_extrator
    diluicao = instance.fator_diluicao

    # 🚨 TRAVA GLOBAL NO BACK-END PARA AA, FC, ES
    if bateria.equipamento in ["AA", "FC", "ES"]:
        if vol_solo is None or vol_extrator is None or diluicao is None:
            print(
                f"⚠️ [BLOQUEIO GLOBAL] Falha ao processar {bateria.elemento}. V-Solo, V-Extrator ou Diluição ausentes."
            )
            return

    # 🟣 ADIÇÃO: BLOCO DA TITULAÇÃO (Alumínio e H+Al)
    if bateria.equipamento == "TI":
        if bateria.leitura_branco is None:
            print(f"⚠️ [BLOQUEIO TI] Leitura do Branco ausente para Titulação.")
            return

        maquina_ti = CalculadoraTitulacao()
        try:
            if bateria.elemento == "Al":
                resultado = maquina_ti.calcular_aluminio(
                    instance.leitura_bruta, bateria.leitura_branco
                )
                campo_laudo = "al"
            elif bateria.elemento == "H_Al":
                resultado = maquina_ti.calcular_acidez_potencial(
                    instance.leitura_bruta, bateria.leitura_branco
                )
                campo_laudo = "h_al"
        except Exception as e:
            print(f"⚠️ [ERRO TI] {e}")

    # 🔵 PHGÂMETRO
    elif bateria.equipamento == "PH":
        maquina_ph = LeitorPHmetro()
        if "ph_agua" in bateria.elemento:
            resultado, campo_laudo = (
                maquina_ph.registrar_leituras(ph_agua=instance.leitura_bruta).get(
                    "ph_agua"
                ),
                "ph_agua",
            )
        elif "ph_cacl2" in bateria.elemento:
            resultado, campo_laudo = (
                maquina_ph.registrar_leituras(ph_cacl2=instance.leitura_bruta).get(
                    "ph_cacl2"
                ),
                "ph_cacl2",
            )
        elif "ph_kcl" in bateria.elemento:
            resultado, campo_laudo = (
                maquina_ph.registrar_leituras(ph_kcl=instance.leitura_bruta).get(
                    "ph_kcl"
                ),
                "ph_kcl",
            )

    # 🟡 ESPECTROFOTÔMETRO
    elif bateria.equipamento == "ES":
        maquina_es = CalculadoraEspectrofotometro()
        if bateria.elemento == "MO":
            resultado, campo_laudo = (
                maquina_es.calcular_mo_disponivel(instance.leitura_bruta),
                "mo",
            )
        elif (
            bateria.coeficiente_angular_a is not None
            and bateria.coeficiente_linear_b is not None
        ):
            if bateria.elemento == "P_rem":
                resultado = maquina_es.calcular_p_rem(
                    leitura_transmitancia=instance.leitura_bruta,
                    coeficiente_angular_a=bateria.coeficiente_angular_a,
                    coeficiente_linear_b=bateria.coeficiente_linear_b,
                    fator_coluna_e=diluicao,
                )
                campo_laudo = "p_rem"
            elif bateria.elemento == "P_R":
                resultado = maquina_es.calcular_p_resina_disponivel(
                    instance.leitura_bruta,
                    bateria.coeficiente_angular_a,
                    bateria.coeficiente_linear_b,
                    vol_extrator,
                    diluicao,
                    vol_solo,
                )
                campo_laudo = "p_r"
            elif bateria.elemento == "P_M":
                resultado = maquina_es.calcular_p_mehlich_disponivel(
                    instance.leitura_bruta,
                    bateria.coeficiente_angular_a,
                    bateria.coeficiente_linear_b,
                    vol_extrator,
                    diluicao,
                    vol_solo,
                )
                campo_laudo = "p_m"
            elif bateria.elemento == "S":
                resultado = maquina_es.calcular_s_disponivel(
                    instance.leitura_bruta,
                    bateria.coeficiente_angular_a,
                    bateria.coeficiente_linear_b,
                    vol_extrator,
                    diluicao,
                    vol_solo,
                )
                campo_laudo = "s"
            elif bateria.elemento == "B":
                resultado = maquina_es.calcular_b_disponivel(
                    instance.leitura_bruta,
                    bateria.coeficiente_angular_a,
                    vol_extrator,
                    diluicao,
                    vol_solo,
                )
                campo_laudo = "b"

    # 🟢 ABSORÇÃO ATÔMICA
    elif (
        bateria.equipamento == "AA"
        and bateria.leitura_branco is not None
        and bateria.coeficiente_angular_a is not None
    ):
        maquina_aa = CalculadoraAbsorcaoAtomica()
        elem = bateria.elemento.lower()
        if hasattr(maquina_aa, f"calcular_{elem}_disponivel"):
            resultado, campo_laudo = (
                getattr(maquina_aa, f"calcular_{elem}_disponivel")(
                    instance.leitura_bruta,
                    bateria.leitura_branco,
                    bateria.coeficiente_angular_a,
                    bateria.coeficiente_linear_b,
                    vol_extrator,
                    diluicao,
                    vol_solo,
                ),
                elem,
            )

    # 🔴 FOTÔMETRO DE CHAMA
    elif bateria.equipamento == "FC" and bateria.coeficiente_angular_a is not None:
        maquina_fc = CalculadoraFotometroChama()
        elem = bateria.elemento.lower()
        resultado, campo_laudo = (
            getattr(maquina_fc, f"calcular_{elem}_disponivel")(
                instance.leitura_bruta,
                bateria.coeficiente_angular_a,
                bateria.coeficiente_linear_b,
                vol_extrator,
                diluicao,
                vol_solo,
            ),
            elem,
        )

    # 💾 SALVAMENTO NO LAUDO
    if resultado is not None and campo_laudo is not None:
        if resultado < 0:
            resultado = Decimal("0.00")
        setattr(laudo, campo_laudo, resultado)
        laudo.save()
