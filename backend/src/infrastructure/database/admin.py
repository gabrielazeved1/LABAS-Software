from django.contrib import admin
from .models import Cliente, AnaliseSolo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    configuracao da interface administrativa para o modelo Cliente.
    define como os dados dos clientes sao listados e buscados no painel.
    """

    # define quais colunas aparecerão na tabela de listagem geral (grid).
    list_display = ("codigo", "nome", "municipio", "contato")

    # cria uma barra de busca no topo. Permite pesquisar por nome ou codigo.
    search_fields = ("nome", "codigo")


@admin.register(AnaliseSolo)
class AnaliseSoloAdmin(admin.ModelAdmin):
    """
    configuracao da interface administrativa para o modelo AnaliseSolo.

    Objetivo: organizar e espelhar a ordem da planilha mestr
    """

    # colunas visiveis na tabela de listagem (visão geral das análises).
    list_display = ("n_lab", "cliente", "data_entrada", "ph_agua", "p_m")

    # barra de busca
    #'cliente__nome' permite buscar pelo nome do cliente relacionado (JOIN).
    search_fields = ("n_lab", "cliente__nome")

    # Fieldsets organiza os campos do formulario em grupos (secoes) logicos, usei as colunas
    # Estrutura: ( "Título da Seção", { "fields": (campos...) } )
    fieldsets = (
        (
            "Identificação (Coluna 1 + Datas)",
            {"fields": (("n_lab", "cliente"), ("data_entrada", "data_saida"))},
        ),
        (
            "Colunas 2 a 6 (pH e Fósforo)",
            {"fields": (("ph_agua", "ph_kcl", "ph_cacl2"), ("p_m", "p_r"))},
        ),
        (
            "Colunas 7 a 12 (Bases e Acidez)",
            {"fields": (("k", "na"), ("ca", "mg"), ("al", "h_al"))},
        ),
        (
            "Colunas 13 a 17 (Cálculos de Troca)",
            {"fields": (("sb", "t", "T_maiusculo"), ("V", "m"))},
        ),
        (
            "Colunas 18 a 23 (P-rem, S e Micros)",
            {"fields": (("p_rem", "s"), ("b", "zn", "cu", "mn"))},
        ),
        (
            "Colunas 24 a 29 (Fe, MO e Relações)",
            {"fields": (("fe", "mo"), ("ca_mg", "ca_k", "mg_k"), "c_org")},
        ),
        (
            "Extras (Físico)",
            {
                # A classe 'collapse' faz esta seção iniciar recolhida (escondida)
                "classes": ("collapse",),
                "fields": (("areia", "argila", "silte"),),
            },
        ),
    )
