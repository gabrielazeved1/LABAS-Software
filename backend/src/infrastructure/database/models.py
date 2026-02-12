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
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuário de Acesso",
    )

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class AnaliseSolo(models.Model):
    # Identificação
    n_lab = models.CharField(max_length=50, unique=True, verbose_name="N Lab")  # Col 1
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="analises",
        verbose_name="Código cliente",
    )  # Col 2

    # Acidez
    ph_agua = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="pH água"
    )  # Col 3
    ph_kcl = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="pH Kcl"
    )  # Col 4
    ph_cacl2 = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="pH Cacl2"
    )  # Col 5

    # Fósforo
    p_m = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="P_M", help_text="Mehlich"
    )  # Col 6
    p_r = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="P_R",
        help_text="Resina",
    )  # Col 7

    # Bases
    k = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="K")  # Col 8
    na = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Na"
    )  # Col 9
    ca = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Ca"
    )  # Col 10
    mg = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Mg2+"
    )  # Col 11

    # Alumínio
    al = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Al3+"
    )  # Col 12
    h_al = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="H+Al"
    )  # Col 13

    # Calculados (Intermediários na Planilha)
    sb = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="SB"
    )  # Col 14
    t = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="t"
    )  # Col 15
    T_maiusculo = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="T"
    )  # Col 16
    V = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="V"
    )  # Col 17
    m = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="m"
    )  # Col 18

    # O P-REM ESTÁ AQUI NA PLANILHA REAL
    p_rem = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="P-rem"
    )  # Col 19

    # Enxofre e Micros
    s = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="S"
    )  # Col 20
    b = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="B"
    )  # Col 21
    zn = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Zn"
    )  # Col 22
    cu = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Cu"
    )  # Col 23
    mn = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Mn"
    )  # Col 24
    fe = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Fe"
    )  # Col 25

    # Matéria Orgânica e Relações
    mo = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="MO"
    )  # Col 26
    ca_mg = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Ca/Mg"
    )  # Col 27
    ca_k = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Ca/K"
    )  # Col 28
    mg_k = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Mg/K"
    )  # Col 29
    c_org = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="C-org"
    )  # Col 30

    # Extras do Sistema
    data_entrada = models.DateField(default=timezone.now, verbose_name="Data Entrada")
    data_saida = models.DateField(blank=True, null=True, verbose_name="Data Saída")
    areia = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="Areia %"
    )
    argila = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="Argila %"
    )
    silte = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="Silte %"
    )

    def clean(self):
        if self.ph_agua and (self.ph_agua < 0 or self.ph_agua > 14):
            raise ValidationError({"ph_agua": "O pH deve estar entre 0 e 14."})

    def __str__(self):
        return f"Laudo {self.n_lab} - {self.cliente.nome}"

    class Meta:
        verbose_name = "Análise de Solo"
        verbose_name_plural = "Análises de Solo"
