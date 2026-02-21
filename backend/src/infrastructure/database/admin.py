from django.contrib import admin
from .models import (
    Cliente,
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


class LeituraEquipamentoLaudoInline(admin.TabularInline):
    """Exibe as leituras brutas diretamente dentro da ficha do Laudo."""

    model = LeituraEquipamento
    extra = 6
    fields = ("bateria", "leitura_bruta", "fator_diluicao")


@admin.register(AnaliseSolo)
class AnaliseSoloAdmin(admin.ModelAdmin):
    list_display = ("n_lab", "cliente", "data_entrada", "ph_agua", "p_m")
    search_fields = ("n_lab", "cliente__nome")
    inlines = [LeituraEquipamentoLaudoInline]

    fieldsets = (
        (
            "1. Identificação e Controle",
            {"fields": (("n_lab", "cliente"), ("data_entrada", "data_saida"))},
        ),
        ("2. Phagâmetro (Acidez)", {"fields": (("ph_agua", "ph_cacl2", "ph_kcl"),)}),
        (
            "3. Espectrofotômetro (Fósforo, Enxofre, Boro e MO)",
            {"fields": (("p_m", "p_r", "p_rem"), ("mo", "s", "b"))},
        ),
        ("4. Fotômetro de Chama", {"fields": (("k", "na"),)}),
        (
            "5. Absorção Atômica (Bases e Micros)",
            {"fields": (("ca", "mg"), ("cu", "fe"), ("mn", "zn"))},
        ),
        ("6. Titulação", {"fields": (("al", "h_al"),)}),
        (
            "7. Física do Solo (Granulometria)",
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
# 2. CONFIGURAÇÃO DE BATERIAS E CURVAS DE CALIBRAÇÃO
# =============================================================================


class PontoCalibracaoInline(admin.TabularInline):
    """Pontos da Curva com conversão visual de Transmitância para Absorbância."""

    model = PontoCalibracao
    extra = 6
    fields = ("concentracao", "absorvancia", "exibir_abs_convertida")
    readonly_fields = ("exibir_abs_convertida",)

    @admin.display(description="Absorbância Real (Calculada)")
    def exibir_abs_convertida(self, instance):
        if not instance.pk or instance.absorvancia is None:
            return "-"
        from decimal import Decimal

        if instance.bateria.equipamento == "ES":
            if instance.absorvancia > 0:
                # Mostra ao técnico o valor que o sistema usará para a reta
                val = Decimal("2") - instance.absorvancia.log10()
                return f"{val:.6f}"
            return "Erro T%"
        return "N/A"


@admin.register(BateriaCalibracao)
class BateriaCalibracaoAdmin(admin.ModelAdmin):
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
        # PH e MO não possuem curva de calibração diária
        if obj and (obj.equipamento == "PH" or obj.elemento == "MO"):
            return []
        return [PontoCalibracaoInline]

    def get_fieldsets(self, request, obj=None):
        # Estrutura base de campos
        info_bloco = (
            "Informações da Bateria",
            {"fields": (("equipamento", "elemento"), "ativo")},
        )

        metodologia_bloco = (
            "Configuração da Metodologia",
            {
                "fields": (("volume_solo", "volume_extrator"),),
                "description": "Defina os volumes usados (Solo em cm³ e Extrator em ml).",
            },
        )

        equacao_bloco = (
            "Equação da Reta (Automática)",
            {
                "fields": (
                    "equacao_formada",
                    ("coeficiente_linear_b", "coeficiente_angular_a", "r_quadrado"),
                ),
                "description": "Recalculada instantaneamente com base nos pontos salvos abaixo.",
            },
        )

        fundo_bloco = ("Correção de Fundo", {"fields": ("leitura_branco",)})

        # Lógica de exibição por equipamento
        if obj and (obj.equipamento == "PH" or obj.elemento == "MO"):
            return (info_bloco,)

        if obj and obj.equipamento == "FC":
            # Fotômetro de chama não usa leitura de branco
            return (info_bloco, metodologia_bloco, equacao_bloco)

        # Padrão para AA e ES (Exibe tudo incluindo o Branco)
        return (info_bloco, metodologia_bloco, equacao_bloco, fundo_bloco)


# =============================================================================
# 3. LISTA GERAL DE LEITURAS
# =============================================================================


@admin.register(LeituraEquipamento)
class LeituraEquipamentoAdmin(admin.ModelAdmin):
    list_display = ("analise", "bateria", "leitura_bruta", "fator_diluicao")
    list_editable = ("bateria", "leitura_bruta", "fator_diluicao")
    list_filter = ("bateria__elemento", "bateria__equipamento")
    search_fields = ("analise__n_lab",)
