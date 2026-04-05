import logging
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from .models import AnaliseSolo, BateriaCalibracao, LeituraEquipamento, PontoCalibracao

logger = logging.getLogger(__name__)

from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica
from src.application.equipamentos.fotometro_chama import CalculadoraFotometroChama
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.phmetro import LeitorPHmetro
from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro
from src.application.equipamentos.titulacao import CalculadoraTitulacao
from src.application.use_cases import CalculadoraAnaliseSolo


# =============================================================================
# 1. GERENCIAMENTO DA BATERIA ATIVA
# =============================================================================


@receiver(pre_save, sender=BateriaCalibracao)
def garantir_bateria_unica_ativa(sender, instance, **kwargs):
    """
    Ao marcar uma bateria como ativa, desativa automaticamente todas as outras
    do mesmo equipamento/elemento para garantir unicidade da curva do dia.
    """
    if instance.ativo:
        BateriaCalibracao.objects.filter(
            equipamento=instance.equipamento,
            elemento=instance.elemento,
            ativo=True,
        ).exclude(pk=instance.pk).update(ativo=False)


# =============================================================================
# 2. CALCULO DA CURVA DE CALIBRACAO
# =============================================================================


@receiver([post_save, post_delete], sender=PontoCalibracao)
def atualizar_equacao_da_bateria(sender, instance, **kwargs):
    """
    Escuta alteracoes nos padroes de calibracao.
    Sempre que um ponto e adicionado, alterado ou removido,
    recalcula a equacao da reta para o equipamento correspondente.
    """
    bateria = instance.bateria
    pontos = bateria.pontos.all()

    if pontos.count() >= 2:
        x_padroes = [p.concentracao for p in pontos]
        print(
            "[CURVA DEBUG] Bateria %s (%s/%s) pontos=%s",
            bateria.id,
            bateria.equipamento,
            bateria.elemento,
            list(zip(x_padroes, [p.absorvancia for p in pontos])),
        )

        if bateria.equipamento == "ES":
            y_lidos = []
            for p in pontos:
                if p.absorvancia <= Decimal("0"):
                    # Invalida a curva caso haja uma leitura optica nula ou negativa
                    bateria.coeficiente_angular_a = bateria.coeficiente_linear_b = (
                        bateria.r_quadrado
                    ) = None
                    bateria.save(
                        update_fields=[
                            "coeficiente_angular_a",
                            "coeficiente_linear_b",
                            "r_quadrado",
                        ]
                    )
                    return
                # Converte Transmitancia lida na curva para Absorbancia (Lei de Beer)
                y_lidos.append(Decimal("2") - p.absorvancia.log10())
        else:
            y_lidos = [p.absorvancia for p in pontos]

        try:
            # Invoca o motor matematico isolado
            motor = CurvaRegressaoLinear(valores_x=x_padroes, valores_y=y_lidos)
            bateria.coeficiente_angular_a = motor.a
            bateria.coeficiente_linear_b = motor.b
            bateria.r_quadrado = motor.r2.quantize(Decimal("0.000001"))
            bateria.save(
                update_fields=[
                    "coeficiente_angular_a",
                    "coeficiente_linear_b",
                    "r_quadrado",
                ]
            )
            logger.info(
                "[CURVA OK] Bateria %s (%s/%s): y = %sx + %s | R²=%s",
                bateria.id,
                bateria.equipamento,
                bateria.elemento,
                bateria.coeficiente_angular_a,
                bateria.coeficiente_linear_b,
                bateria.r_quadrado,
            )
        except Exception as e:
            logger.error(
                "[ERRO CURVA] Bateria %s (%s/%s) com %s pontos: %s",
                bateria.id,
                bateria.equipamento,
                bateria.elemento,
                len(x_padroes),
                e,
            )
            print(
                "[ERRO CURVA] Bateria %s (%s/%s) com %s pontos: %s",
                bateria.id,
                bateria.equipamento,
                bateria.elemento,
                len(x_padroes),
                e,
            )
            # Invalida a curva para que a UI exiba aviso correto
            bateria.coeficiente_angular_a = None
            bateria.coeficiente_linear_b = None
            bateria.r_quadrado = None
            bateria.save(
                update_fields=[
                    "coeficiente_angular_a",
                    "coeficiente_linear_b",
                    "r_quadrado",
                ]
            )
    else:
        # Reseta os coeficientes se nao houver pontos suficientes para formar uma reta
        bateria.coeficiente_angular_a = bateria.coeficiente_linear_b = (
            bateria.r_quadrado
        ) = None
        bateria.save(
            update_fields=[
                "coeficiente_angular_a",
                "coeficiente_linear_b",
                "r_quadrado",
            ]
        )


# =============================================================================
# 2. CALCULOS AGRONOMICOS DO LAUDO
# =============================================================================


@receiver(pre_save, sender=AnaliseSolo)
def calcular_relacoes_agronomicas(sender, instance, **kwargs):
    """
    Atua como controlador interceptando o salvamento do laudo.
    Delega a matematica pesada e as regras de arredondamento para o Use Case,
    garantindo que as regras de negocio fiquem isoladas do framework web.
    """
    # 1. Instancia o Use Case
    motor_agronomico = CalculadoraAnaliseSolo()

    # 2. Verifica presenca de dados minimos para execucao do calculo
    if instance.ca is not None or instance.mg is not None or instance.k is not None:

        # 3. Envia os dados brutos para o motor calcular
        resultados = motor_agronomico.calcular_resultados_completos(
            k_mg=instance.k,
            ca=instance.ca,
            mg=instance.mg,
            al=instance.al,
            h_al=instance.h_al,
            mo=instance.mo,
        )

        # 4. Atualiza os campos do modelo com os resultados validados pelo Use Case
        instance.sb = resultados["sb"]
        instance.t = resultados["t"]
        instance.T_maiusculo = resultados["T"]
        instance.V = resultados["V"]
        instance.m = resultados["m"]
        instance.ca_mg = resultados["ca_mg"]
        instance.ca_k = resultados["ca_k"]
        instance.mg_k = resultados["mg_k"]
        instance.c_org = resultados["c_org"]


# =============================================================================
# 3. ROBO DE PROCESSAMENTO E INTEGRACAO DE EQUIPAMENTOS
# =============================================================================


@receiver(post_save, sender=LeituraEquipamento)
def automatizar_calculo_equipamentos(sender, instance, created, **kwargs):
    """
    Orquestra o roteamento das leituras brutas inseridas pelos tecnicos.
    Identifica a origem do dado (Equipamento) e delega o processamento
    para a classe de dominio correspondente na camada de aplicacao.
    """
    bateria = instance.bateria
    laudo = instance.analise
    resultado = None
    campo_laudo = None

    # Variaveis estequiometricas de base
    vol_solo = bateria.volume_solo
    vol_extrator = bateria.volume_extrator
    diluicao = instance.fator_diluicao

    # [BLOQUEIO GLOBAL] TRAVA NO BACK-END PARA EQUIPAMENTOS DE EXTRACAO
    if bateria.equipamento in ["AA", "FC", "ES"]:
        if vol_solo is None or vol_extrator is None or diluicao is None:
            print(
                f"[FALHA DE PROCESSAMENTO] Impossivel calcular {bateria.elemento}. "
                "V-Solo, V-Extrator ou Diluicao ausentes na configuracao da bateria."
            )
            return

    # [BLOCO TI] TITULACAO (Aluminio e Acidez Potencial)
    if bateria.equipamento == "TI":
        if bateria.leitura_branco is None:
            print("[BLOQUEIO TI] Leitura do Branco ausente para o lote de Titulacao.")
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
            print(f"[ERRO TI] Falha no calculo volumetrico: {e}")

    # [BLOCO PH] PHMETRO
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

    # [BLOCO ES] ESPECTROFOTOMETRO
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

    # [BLOCO AA] ABSORCAO ATOMICA
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

    # [BLOCO FC] FOTOMETRO DE CHAMA
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

    # [SALVAMENTO] ATUALIZACAO DO LAUDO
    if resultado is not None and campo_laudo is not None:
        # Trava de integridade garantindo que nutrientes nao fiquem negativos
        if resultado < 0:
            resultado = Decimal("0.00")
        setattr(laudo, campo_laudo, resultado)
        laudo.save()
