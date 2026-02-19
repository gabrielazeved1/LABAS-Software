from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Cliente(models.Model):
    """
    Entidade de persistencia para dados cadastrais de Clientes.
    Mantem vinculo com o sistema de autenticação (User) para controle de acesso.
    """

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
    """
    Modelo principal de análise de solo.
    A ordem dos campos reflete estritamente a estrutura física das
    estações de trabalho/equipamentos do laboratório.
    """

    # --- 1. Identificação e Controle ---
    n_lab = models.CharField(max_length=50, unique=True, verbose_name="N Lab")
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="analises",
        verbose_name="Código cliente",
    )
    data_entrada = models.DateField(default=timezone.now, verbose_name="Data Entrada")
    data_saida = models.DateField(blank=True, null=True, verbose_name="Data Saída")

    # --- 2. Phagâmetro ---
    ph_agua = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="pH água"
    )
    ph_cacl2 = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="pH Cacl2"
    )
    ph_kcl = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="pH Kcl"
    )

    # --- 3. Espectrofotômetro ---
    p_m = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="P_M", help_text="Mehlich"
    )
    p_r = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="P_R",
        help_text="Resina",
    )
    p_rem = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="P-rem"
    )
    mo = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="MO")
    s = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="S"
    )
    b = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="B"
    )

    # --- 4. Fotômetro de Chama ---
    k = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="K")
    na = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Na"
    )

    # --- 5. Absorção Atômica ---
    ca = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ca")
    mg = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Mg2+")
    cu = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Cu"
    )
    fe = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Fe"
    )
    mn = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Mn"
    )
    zn = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Zn"
    )

    # --- 6. Titulação ---
    al = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Al3+")
    h_al = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="H+Al")

    # --- 7. Física do Solo (Granulometria) ---
    areia = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="Areia %"
    )
    argila = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="Argila %"
    )
    silte = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="Silte %"
    )

    # ==========================================
    # --- 8. CALCULADOS (Regras de Negócio) ---
    # ==========================================
    sb = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="SB"
    )
    t = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="t"
    )
    T_maiusculo = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="T"
    )
    V = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="V"
    )
    m = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True, verbose_name="m"
    )
    ca_mg = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Ca/Mg"
    )
    ca_k = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Ca/K"
    )
    mg_k = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Mg/K"
    )
    c_org = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="C-org"
    )

    def clean(self):
        """Validacao de regras de negocio"""
        if self.ph_agua and (self.ph_agua < 0 or self.ph_agua > 14):
            raise ValidationError({"ph_agua": "O pH deve estar entre 0 e 14."})

    def __str__(self):
        return f"Laudo {self.n_lab} - {self.cliente.nome}"

    class Meta:
        verbose_name = "Análise de Solo"
        verbose_name_plural = "Análises de Solo"
