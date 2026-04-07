from django.contrib import admin
from .models import (
    Cliente,
    Laudo,
    AnaliseSolo,
    BateriaCalibracao,
    LeituraEquipamento,
    PontoCalibracao,
)

# =============================================================================
# 1. GERENCIAMENTO DE CLIENTES E LAUDOS
# =============================================================================


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "municipio", "contato")
    search_fields = ("nome", "codigo")


@admin.register(Laudo)
class LaudoAdmin(admin.ModelAdmin):
    list_display = ("codigo_laudo", "cliente", "data_emissao")
    search_fields = ("codigo_laudo", "cliente__nome", "cliente__codigo")
    readonly_fields = ("codigo_laudo",)


class LeituraEquipamentoLaudoInline(admin.TabularInline):
    """
    Interface inline que exibe as leituras brutas diretamente dentro da ficha do Laudo.
    Agiliza a digitacao dos resultados pelo tecnico.
    """

    model = LeituraEquipamento
    extra = 6
    fields = ("bateria", "leitura_bruta", "fator_diluicao")


@admin.register(AnaliseSolo)
class AnaliseSoloAdmin(admin.ModelAdmin):
    list_display = ("n_lab", "laudo", "ativo", "data_entrada", "ph_agua", "p_m")
    search_fields = ("n_lab", "laudo__cliente__nome", "laudo__codigo_laudo")
    list_filter = ("ativo",)
    inlines = [LeituraEquipamentoLaudoInline]

    fieldsets = (
        (
            "1. Identificacao e Controle",
            {
                "fields": (
                    ("n_lab", "laudo", "ativo", "referencia"),
                    ("data_entrada", "data_saida"),
                )
            },
        ),
        ("2. Phagametro (Acidez)", {"fields": (("ph_agua", "ph_cacl2", "ph_kcl"),)}),
        (
            "3. Espectrofotometro (Fosforo, Enxofre, Boro e MO)",
            {"fields": (("p_m", "p_r", "p_rem"), ("mo", "s", "b"))},
        ),
        ("4. Fotometro de Chama", {"fields": (("k", "na"),)}),
        (
            "5. Absorcao Atomica (Bases e Micros)",
            {"fields": (("ca", "mg"), ("cu", "fe"), ("mn", "zn"))},
        ),
        ("6. Titulacao", {"fields": (("al", "h_al"),)}),
        (
            "7. Fisica do Solo (Granulometria)",
            {"classes": ("collapse",), "fields": (("areia", "argila", "silte"),)},
        ),
        (
            "8. Resultados Calculados",
            {
                "classes": ("collapse",),
                "fields": (
                    ("sb", "t", "T_maiusculo"),
                    ("V", "m"),
                    ("ca_mg", "ca_k", "mg_k"),
                    "c_org",
                ),
            },
        ),
    )


# =============================================================================
# 2. CONFIGURACAO DE BATERIAS E CURVAS DE CALIBRACAO
# =============================================================================


class PontoCalibracaoInline(admin.TabularInline):
    """
    Interface inline para inserir os pontos padroes da curva de calibracao.
    Inclui um feedback visual convertendo Transmitancia para Absorbancia em tempo real.
    """

    model = PontoCalibracao
    extra = 6
    fields = ("concentracao", "absorvancia", "exibir_abs_convertida")
    readonly_fields = ("exibir_abs_convertida",)

    @admin.display(description="Absorbancia Real (Calculada)")
    def exibir_abs_convertida(self, instance):
        """
        Gera o feedback visual para o operador da maquina.
        Aplica a Lei de Beer para visualizacao da conversao otica no painel.
        """
        if not instance.pk or instance.absorvancia is None:
            return "-"
        from decimal import Decimal

        if instance.bateria.equipamento == "ES":
            if instance.absorvancia > 0:
                # Mostra ao tecnico o valor exato que o sistema usara no motor matematico
                val = Decimal("2") - instance.absorvancia.log10()
                return f"{val:.6f}"
            return "Erro T%"
        return "N/A"


@admin.register(BateriaCalibracao)
class BateriaCalibracaoAdmin(admin.ModelAdmin):
    """
    Painel de controle das configuracoes diarias dos equipamentos.
    Apresenta dinamicamente os campos necessarios dependendo da maquina selecionada.
    """

    list_display = (
        "elemento",
        "equipamento",
        "data_criacao",
        "equacao_formada",
        "r_quadrado",
        "ativo",
    )
    readonly_fields = ("equacao_formada",)

    def get_inlines(self, request, obj=None):
        """
        Remove a tabela de pontos de calibracao para equipamentos ou elementos
        que utilizam logica direta, como pH e Materia Organica.
        """
        if obj and (obj.equipamento == "PH" or obj.elemento == "MO"):
            return []
        return [PontoCalibracaoInline]

    def get_fieldsets(self, request, obj=None):
        """
        Monta a interface de configuracao exibindo apenas os campos que
        fazem sentido fisico e quimico para o equipamento especifico.
        """
        info_bloco = (
            "Informacoes da Bateria",
            {"fields": (("equipamento", "elemento"), "ativo")},
        )

        metodologia_bloco = (
            "Configuracao da Metodologia",
            {
                "fields": (("volume_solo", "volume_extrator"),),
                "description": "Defina os volumes usados (Solo em cm3 e Extrator em ml).",
            },
        )

        equacao_bloco = (
            "Equacao da Reta (Automatica)",
            {
                "fields": (
                    "equacao_formada",
                    ("coeficiente_linear_b", "coeficiente_angular_a", "r_quadrado"),
                ),
                "description": "Recalculada instantaneamente com base nos pontos salvos abaixo.",
            },
        )

        fundo_bloco = ("Correcao de Fundo", {"fields": ("leitura_branco",)})

        # Logica de exibicao condicional por equipamento
        if obj and (obj.equipamento == "PH" or obj.elemento == "MO"):
            return (info_bloco,)

        if obj and obj.equipamento == "FC":
            # Fotometro de chama nao requer configuracao de leitura de branco
            return (info_bloco, metodologia_bloco, equacao_bloco)

        # Padrao para Absorcao Atomica e Espectrofotometro (Exibe bloco completo)
        return (info_bloco, metodologia_bloco, equacao_bloco, fundo_bloco)


# =============================================================================
# 3. LISTA GERAL DE LEITURAS
# =============================================================================


@admin.register(LeituraEquipamento)
class LeituraEquipamentoAdmin(admin.ModelAdmin):
    """
    Visao geral em lista de todas as leituras brutas registradas no laboratorio.
    Permite edicao rapida em lote e filtragem avancada por equipamento ou elemento.
    """

    list_display = ("analise", "bateria", "leitura_bruta", "fator_diluicao")
    list_editable = ("bateria", "leitura_bruta", "fator_diluicao")
    list_filter = ("bateria__elemento", "bateria__equipamento")
    search_fields = ("analise__n_lab",)
