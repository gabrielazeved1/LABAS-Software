from django.contrib import admin
from .models import Cliente, AnaliseSolo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para o modelo Cliente.
    Define como os dados dos clientes são listados e buscados no painel.
    """

    list_display = ("codigo", "nome", "municipio", "contato")
    search_fields = ("nome", "codigo")


@admin.register(AnaliseSolo)
class AnaliseSoloAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para o modelo AnaliseSolo.

    Objetivo: Organizar os campos em blocos visuais que espelham
    exatamente as estações de trabalho e equipamentos do laboratório.
    """

    list_display = ("n_lab", "cliente", "data_entrada", "ph_agua", "p_m")
    search_fields = ("n_lab", "cliente__nome")

    # Fieldsets organiza a tela de cadastro em "blocos" de equipamentos
    fieldsets = (
        (
            "1. Identificação e Controle",
            {"fields": (("n_lab", "cliente"), ("data_entrada", "data_saida"))},
        ),
        (
            "2. Phagâmetro (Acidez)",
            {"fields": (("ph_agua", "ph_cacl2", "ph_kcl"),)},
        ),
        (
            "3. Espectrofotômetro (Fósforo, Enxofre, Boro e MO)",
            {"fields": (("p_m", "p_r", "p_rem"), ("mo", "s", "b"))},
        ),
        (
            "4. Fotômetro de Chama",
            {"fields": (("k", "na"),)},
        ),
        (
            "5. Absorção Atômica (Bases e Micros)",
            {"fields": (("ca", "mg"), ("cu", "fe"), ("mn", "zn"))},
        ),
        (
            "6. Titulação",
            {"fields": (("al", "h_al"),)},
        ),
        (
            "7. Física do Solo (Granulometria)",
            {
                "classes": ("collapse",),
                "fields": (("areia", "argila", "silte"),),
            },
        ),
        (
            "8. Resultados Calculados (Preenchimento Automático)",
            {
                # Deixamos minimizado porque o usuário não vai precisar digitar isso
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
