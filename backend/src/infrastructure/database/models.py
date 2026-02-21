# from django.db import models
# from django.utils import timezone
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User


# class Cliente(models.Model):
#     nome = models.CharField(max_length=255, verbose_name="Solicitante")
#     codigo = models.CharField(max_length=50, unique=True, verbose_name="Código Cliente")
#     contato = models.CharField(
#         max_length=100, blank=True, null=True, verbose_name="Contato"
#     )
#     area = models.CharField(max_length=100, blank=True, null=True, verbose_name="Área")
#     municipio = models.CharField(
#         max_length=100, blank=True, null=True, verbose_name="Município"
#     )
#     data_cadastro = models.DateTimeField(auto_now_add=True)
#     observacoes = models.TextField(blank=True, null=True, verbose_name="Obs")
#     usuario = models.OneToOneField(
#         User, on_delete=models.SET_NULL, null=True, blank=True
#     )

#     def __str__(self):
#         return f"{self.codigo} - {self.nome}"

#     class Meta:
#         verbose_name = "Cliente"
#         verbose_name_plural = "Clientes"


# class AnaliseSolo(models.Model):
#     n_lab = models.CharField(max_length=50, unique=True, verbose_name="N Lab")
#     cliente = models.ForeignKey(
#         Cliente, on_delete=models.CASCADE, related_name="analises"
#     )
#     data_entrada = models.DateField(default=timezone.now, verbose_name="Data Entrada")
#     data_saida = models.DateField(blank=True, null=True, verbose_name="Data Saída")

#     ph_agua = models.DecimalField(
#         max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH água"
#     )
#     ph_cacl2 = models.DecimalField(
#         max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH CaCl2"
#     )
#     ph_kcl = models.DecimalField(
#         max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH KCl"
#     )

#     p_m = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="P_M (Mehlich)",
#     )
#     p_r = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="P_R (Resina)",
#     )
#     p_rem = models.DecimalField(
#         max_digits=12, decimal_places=4, blank=True, null=True, verbose_name="P-rem"
#     )
#     mo = models.DecimalField(
#         max_digits=10,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Matéria Orgânica",
#     )
#     s = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Enxofre (S)",
#     )
#     b = models.DecimalField(
#         max_digits=10, decimal_places=4, blank=True, null=True, verbose_name="Boro (B)"
#     )

#     k = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Potássio (K)",
#     )
#     na = models.DecimalField(
#         max_digits=10,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Sódio (Na)",
#     )

#     ca = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Cálcio (Ca)",
#     )
#     mg = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Magnésio (Mg)",
#     )
#     cu = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Cobre (Cu)",
#     )
#     fe = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Ferro (Fe)",
#     )
#     mn = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Manganês (Mn)",
#     )
#     zn = models.DecimalField(
#         max_digits=12,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Zinco (Zn)",
#     )

#     al = models.DecimalField(
#         max_digits=10,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Alumínio (Al3+)",
#     )
#     h_al = models.DecimalField(
#         max_digits=10,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Acidez Potencial (H+Al)",
#     )

#     areia = models.DecimalField(
#         max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Areia %"
#     )
#     argila = models.DecimalField(
#         max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Argila %"
#     )
#     silte = models.DecimalField(
#         max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Silte %"
#     )

#     sb = models.DecimalField(
#         max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="SB"
#     )
#     t = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#         verbose_name="t (CTC Efetiva)",
#     )
#     T_maiusculo = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#         verbose_name="T (CTC pH 7.0)",
#     )
#     V = models.DecimalField(
#         max_digits=6,
#         decimal_places=1,
#         blank=True,
#         null=True,
#         verbose_name="V% (Saturação por Bases)",
#     )
#     m = models.DecimalField(
#         max_digits=6,
#         decimal_places=1,
#         blank=True,
#         null=True,
#         verbose_name="m% (Saturação por Al)",
#     )
#     ca_mg = models.DecimalField(
#         max_digits=8,
#         decimal_places=2,
#         blank=True,
#         null=True,
#         verbose_name="Relação Ca/Mg",
#     )
#     ca_k = models.DecimalField(
#         max_digits=8,
#         decimal_places=2,
#         blank=True,
#         null=True,
#         verbose_name="Relação Ca/K",
#     )
#     mg_k = models.DecimalField(
#         max_digits=8,
#         decimal_places=2,
#         blank=True,
#         null=True,
#         verbose_name="Relação Mg/K",
#     )
#     c_org = models.DecimalField(
#         max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="C-org"
#     )

#     def clean(self):
#         if self.ph_agua and (self.ph_agua < 0 or self.ph_agua > 14):
#             raise ValidationError({"ph_agua": "O pH deve estar entre 0 e 14."})

#     def __str__(self):
#         return f"Laudo {self.n_lab} - {self.cliente.nome}"

#     class Meta:
#         verbose_name = "Análise de Solo"
#         verbose_name_plural = "Análises de Solo"


# class BateriaCalibracao(models.Model):
#     EQUIPAMENTO_CHOICES = [
#         ("AA", "Absorção Atômica"),
#         ("FC", "Fotômetro de Chama"),
#         ("ES", "Espectrofotômetro"),
#         ("TI", "Titulação"),
#         ("PH", "Phagâmetro"),
#     ]
#     ELEMENTO_CHOICES = [
#         ("Ca", "Cálcio"),
#         ("Mg", "Magnésio"),
#         ("Cu", "Cobre"),
#         ("Fe", "Ferro"),
#         ("Mn", "Manganês"),
#         ("Zn", "Zinco"),
#         ("K", "Potássio"),
#         ("Na", "Sódio"),
#         ("P_M", "Fósforo (Mehlich)"),
#         ("P_R", "Fósforo (Resina)"),
#         ("P_rem", "Fósforo Remanescente"),
#         ("S", "Enxofre"),
#         ("B", "Boro"),
#         ("Al", "Alumínio"),
#         ("H_Al", "Acidez Potencial"),
#         ("ph_agua", "pH em Água"),
#         ("ph_cacl2", "pH em CaCl2"),
#         ("ph_kcl", "pH em KCl"),
#         ("MO", "Matéria Orgânica"),
#     ]

#     volume_solo = models.DecimalField(
#         max_digits=10,
#         decimal_places=4,
#         null=True,
#         blank=True,
#         verbose_name="Volume de Solo (cm³)",
#     )
#     volume_extrator = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name="Volume de Extrator (ml)",
#     )

#     data_criacao = models.DateTimeField(
#         auto_now_add=True, verbose_name="Data da Calibração"
#     )
#     equipamento = models.CharField(max_length=2, choices=EQUIPAMENTO_CHOICES)
#     elemento = models.CharField(max_length=15, choices=ELEMENTO_CHOICES)

#     coeficiente_angular_a = models.DecimalField(
#         max_digits=15,
#         decimal_places=8,
#         blank=True,
#         null=True,
#         verbose_name="Inclinação (b)",
#     )
#     coeficiente_linear_b = models.DecimalField(
#         max_digits=15,
#         decimal_places=8,
#         blank=True,
#         null=True,
#         verbose_name="Intercepto (a)",
#     )
#     r_quadrado = models.DecimalField(
#         max_digits=7, decimal_places=6, blank=True, null=True, verbose_name="R²"
#     )
#     leitura_branco = models.DecimalField(
#         max_digits=10,
#         decimal_places=4,
#         blank=True,
#         null=True,
#         verbose_name="Leitura do Branco",
#     )

#     ativo = models.BooleanField(default=True, verbose_name="Bateria Ativa no Dia?")

#     @property
#     def equacao_formada(self):
#         if (
#             self.coeficiente_angular_a is not None
#             and self.coeficiente_linear_b is not None
#         ):
#             a, b = self.coeficiente_angular_a, self.coeficiente_linear_b
#             sinal = "+" if b >= 0 else "-"
#             return f"y = {a:.6f}x {sinal} {abs(b):.6f}"
#         return "Equação ainda não gerada"

#     def clean(self):
#         # 🚨 MUDANÇA: Trava Universal. Se for AA, FC ou ES, V-Solo e V-Extrator são obrigatórios.
#         erros = {}
#         if self.equipamento in ["AA", "FC", "ES"]:
#             if self.volume_solo is None:
#                 erros["volume_solo"] = (
#                     f"Obrigatório informar o Volume de Solo para {self.get_equipamento_display()}."
#                 )
#             if self.volume_extrator is None:
#                 erros["volume_extrator"] = (
#                     f"Obrigatório informar o Volume de Extrator para {self.get_equipamento_display()}."
#                 )

#         if self.equipamento == "AA" and self.leitura_branco is None:
#             erros["leitura_branco"] = (
#                 "A Leitura do Branco é OBRIGATÓRIA para Absorção Atômica."
#             )

#         if erros:
#             raise ValidationError(erros)

#     def __str__(self):
#         data_formatada = self.data_criacao.strftime("%d/%m/%Y")
#         instrucoes = {
#             "ES": "a TRANSMITÂNCIA %",
#             "AA": "a ABSORBÂNCIA",
#             "FC": "a EMISSÃO",
#             "PH": "o pH DIRETO",
#             "TI": "o volume a subtrair do BRANCO",
#         }
#         instrucao = instrucoes.get(self.equipamento, "")
#         return f"{self.get_elemento_display()} - {data_formatada} ({self.get_equipamento_display()} -> Digite {instrucao})"

#     class Meta:
#         verbose_name = "Bateria de Calibração"
#         verbose_name_plural = "Baterias de Calibração"


# class LeituraEquipamento(models.Model):
#     analise = models.ForeignKey(
#         AnaliseSolo, on_delete=models.CASCADE, related_name="leituras_brutas"
#     )
#     bateria = models.ForeignKey(
#         BateriaCalibracao, on_delete=models.PROTECT, related_name="leituras"
#     )
#     leitura_bruta = models.DecimalField(
#         max_digits=10, decimal_places=4, verbose_name="Leitura do Visor"
#     )
#     fator_diluicao = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name="Fator de Diluição (Opcional)",
#     )

#     def clean(self):
#         # 🚨 MUDANÇA: Trava Universal. Se for AA, FC ou ES, a Diluição é obrigatória na leitura.
#         if hasattr(self, "bateria") and self.bateria is not None:
#             if self.bateria.equipamento in ["AA", "FC", "ES"]:
#                 if self.fator_diluicao is None:
#                     raise ValidationError(
#                         {
#                             "fator_diluicao": f"O Fator de Diluição é OBRIGATÓRIO na leitura de {self.bateria.get_equipamento_display()}."
#                         }
#                     )

#     def __str__(self):
#         return f"Laudo {self.analise.n_lab} | {self.bateria.get_elemento_display()}: {self.leitura_bruta}"


# class PontoCalibracao(models.Model):
#     bateria = models.ForeignKey(
#         BateriaCalibracao, on_delete=models.CASCADE, related_name="pontos"
#     )
#     concentracao = models.DecimalField(
#         max_digits=10, decimal_places=4, verbose_name="Concentração (Padrão)"
#     )
#     absorvancia = models.DecimalField(
#         max_digits=10, decimal_places=4, verbose_name="Leitura Bruta (Transm % ou Abs)"
#     )

#     class Meta:
#         verbose_name = "Ponto de Calibração"
#         verbose_name_plural = "Pontos de Calibração"
#         ordering = ["concentracao"]

#     def __str__(self):
#         return f"{self.concentracao} -> {self.absorvancia}"
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Cliente(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Solicitante")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código Cliente")
    contato = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Contato"
    )
    area = models.CharField(max_length=100, blank=True, null=True, verbose_name="Área")
    municipio = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Município"
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True, verbose_name="Obs")
    usuario = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class AnaliseSolo(models.Model):
    n_lab = models.CharField(max_length=50, unique=True, verbose_name="N Lab")
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="analises"
    )
    data_entrada = models.DateField(default=timezone.now, verbose_name="Data Entrada")
    data_saida = models.DateField(blank=True, null=True, verbose_name="Data Saída")

    ph_agua = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH água"
    )
    ph_cacl2 = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH CaCl2"
    )
    ph_kcl = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH KCl"
    )

    p_m = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="P_M (Mehlich)",
    )
    p_r = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="P_R (Resina)",
    )
    p_rem = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True, verbose_name="P-rem"
    )
    mo = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Matéria Orgânica",
    )
    s = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Enxofre (S)",
    )
    b = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True, verbose_name="Boro (B)"
    )

    k = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Potássio (K)",
    )
    na = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Sódio (Na)",
    )

    ca = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Cálcio (Ca)",
    )
    mg = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Magnésio (Mg)",
    )
    cu = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Cobre (Cu)",
    )
    fe = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Ferro (Fe)",
    )
    mn = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Manganês (Mn)",
    )
    zn = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Zinco (Zn)",
    )

    al = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Alumínio (Al3+)",
    )
    h_al = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Acidez Potencial (H+Al)",
    )

    areia = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Areia %"
    )
    argila = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Argila %"
    )
    silte = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Silte %"
    )

    sb = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="SB"
    )
    t = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="t (CTC Efetiva)",
    )
    T_maiusculo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="T (CTC pH 7.0)",
    )
    V = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name="V% (Saturação por Bases)",
    )
    m = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name="m% (Saturação por Al)",
    )
    ca_mg = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Relação Ca/Mg",
    )
    ca_k = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Relação Ca/K",
    )
    mg_k = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Relação Mg/K",
    )
    c_org = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="C-org"
    )

    def clean(self):
        if self.ph_agua and (self.ph_agua < 0 or self.ph_agua > 14):
            raise ValidationError({"ph_agua": "O pH deve estar entre 0 e 14."})

    def __str__(self):
        return f"Laudo {self.n_lab} - {self.cliente.nome}"

    class Meta:
        verbose_name = "Análise de Solo"
        verbose_name_plural = "Análises de Solo"


class BateriaCalibracao(models.Model):
    EQUIPAMENTO_CHOICES = [
        ("AA", "Absorção Atômica"),
        ("FC", "Fotômetro de Chama"),
        ("ES", "Espectrofotômetro"),
        ("TI", "Titulação"),
        ("PH", "Phagâmetro"),
    ]
    ELEMENTO_CHOICES = [
        ("Ca", "Cálcio"),
        ("Mg", "Magnésio"),
        ("Cu", "Cobre"),
        ("Fe", "Ferro"),
        ("Mn", "Manganês"),
        ("Zn", "Zinco"),
        ("K", "Potássio"),
        ("Na", "Sódio"),
        ("P_M", "Fósforo (Mehlich)"),
        ("P_R", "Fósforo (Resina)"),
        ("P_rem", "Fósforo Remanescente"),
        ("S", "Enxofre"),
        ("B", "Boro"),
        ("Al", "Alumínio"),
        ("H_Al", "Acidez Potencial"),
        ("ph_agua", "pH em Água"),
        ("ph_cacl2", "pH em CaCl2"),
        ("ph_kcl", "pH em KCl"),
        ("MO", "Matéria Orgânica"),
    ]

    volume_solo = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="Volume de Solo (cm³)",
    )
    volume_extrator = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Volume de Extrator (ml)",
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data da Calibração"
    )
    equipamento = models.CharField(max_length=2, choices=EQUIPAMENTO_CHOICES)
    elemento = models.CharField(max_length=15, choices=ELEMENTO_CHOICES)
    coeficiente_angular_a = models.DecimalField(
        max_digits=15,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name="Inclinação (b)",
    )
    coeficiente_linear_b = models.DecimalField(
        max_digits=15,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name="Intercepto (a)",
    )
    r_quadrado = models.DecimalField(
        max_digits=7, decimal_places=6, blank=True, null=True, verbose_name="R²"
    )
    leitura_branco = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Leitura do Branco",
    )
    ativo = models.BooleanField(default=True, verbose_name="Bateria Ativa no Dia?")

    @property
    def equacao_formada(self):
        if (
            self.coeficiente_angular_a is not None
            and self.coeficiente_linear_b is not None
        ):
            a, b = self.coeficiente_angular_a, self.coeficiente_linear_b
            sinal = "+" if b >= 0 else "-"
            return f"y = {a:.6f}x {sinal} {abs(b):.6f}"
        return "Equação ainda não gerada"

    def clean(self):
        erros = {}
        if self.equipamento in ["AA", "FC", "ES"]:
            if self.volume_solo is None:
                erros["volume_solo"] = (
                    f"Obrigatório informar o Volume de Solo para {self.get_equipamento_display()}."
                )
            if self.volume_extrator is None:
                erros["volume_extrator"] = (
                    f"Obrigatório informar o Volume de Extrator para {self.get_equipamento_display()}."
                )

        # ADIÇÃO: Trava para exigir o Branco na Titulação e no AA
        if self.equipamento in ["AA", "TI"] and self.leitura_branco is None:
            erros["leitura_branco"] = (
                f"A Leitura do Branco é OBRIGATÓRIA para {self.get_equipamento_display()}."
            )

        if erros:
            raise ValidationError(erros)

    def __str__(self):
        data_formatada = self.data_criacao.strftime("%d/%m/%Y")
        instrucoes = {
            "ES": "a TRANSMITÂNCIA %",
            "AA": "a ABSORBÂNCIA",
            "FC": "a EMISSÃO",
            "PH": "o pH DIRETO",
            "TI": "o volume a subtrair do BRANCO",
        }
        instrucao = instrucoes.get(self.equipamento, "")
        return f"{self.get_elemento_display()} - {data_formatada} ({self.get_equipamento_display()} -> Digite {instrucao})"

    class Meta:
        verbose_name = "Bateria de Calibração"
        verbose_name_plural = "Baterias de Calibração"


class LeituraEquipamento(models.Model):
    analise = models.ForeignKey(
        AnaliseSolo, on_delete=models.CASCADE, related_name="leituras_brutas"
    )
    bateria = models.ForeignKey(
        BateriaCalibracao, on_delete=models.PROTECT, related_name="leituras"
    )
    leitura_bruta = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Leitura do Visor"
    )
    fator_diluicao = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Fator de Diluição (Opcional)",
    )

    def clean(self):
        if hasattr(self, "bateria") and self.bateria is not None:
            if self.bateria.equipamento in ["AA", "FC", "ES"]:
                if self.fator_diluicao is None:
                    raise ValidationError(
                        {
                            "fator_diluicao": f"O Fator de Diluição é OBRIGATÓRIO na leitura de {self.bateria.get_equipamento_display()}."
                        }
                    )

    def __str__(self):
        return f"Laudo {self.analise.n_lab} | {self.bateria.get_elemento_display()}: {self.leitura_bruta}"


class PontoCalibracao(models.Model):
    bateria = models.ForeignKey(
        BateriaCalibracao, on_delete=models.CASCADE, related_name="pontos"
    )
    concentracao = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Concentração (Padrão)"
    )
    absorvancia = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Leitura Bruta (Transm % ou Abs)"
    )

    class Meta:
        verbose_name = "Ponto de Calibração"
        verbose_name_plural = "Pontos de Calibração"
        ordering = ["concentracao"]

    def __str__(self):
        return f"{self.concentracao} -> {self.absorvancia}"
