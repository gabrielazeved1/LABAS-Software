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
    """
    Modelo com precisão de 4 casas decimais para entradas brutas,
    evitando erros de arredondamento ocultos do Excel.
    """

    # --- 1. Identificação ---
    n_lab = models.CharField(max_length=50, unique=True, verbose_name="N Lab")
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="analises"
    )
    data_entrada = models.DateField(default=timezone.now, verbose_name="Data Entrada")
    data_saida = models.DateField(blank=True, null=True, verbose_name="Data Saída")

    # --- 2. Phagâmetro (Entrada Bruta: 4 casas) ---
    ph_agua = models.DecimalField(
        max_digits=8, decimal_places=4, verbose_name="pH água"
    )
    ph_cacl2 = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH CaCl2"
    )
    ph_kcl = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH KCl"
    )

    # --- 3. Espectrofotômetro (Entrada Bruta: 4 casas) ---
    p_m = models.DecimalField(
        max_digits=12, decimal_places=4, verbose_name="P_M (Mehlich)"
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
        max_digits=10, decimal_places=4, verbose_name="Matéria Orgânica"
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

    # --- 4. Fotômetro de Chama (Entrada Bruta: 4 casas) ---
    k = models.DecimalField(
        max_digits=12, decimal_places=4, verbose_name="Potássio (K)"
    )
    na = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Sódio (Na)",
    )

    # --- 5. Absorção Atômica (Entrada Bruta: 4 casas para evitar 'fantasmas') ---
    ca = models.DecimalField(
        max_digits=12, decimal_places=4, verbose_name="Cálcio (Ca)"
    )
    mg = models.DecimalField(
        max_digits=12, decimal_places=4, verbose_name="Magnésio (Mg)"
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

    # --- 6. Titulação (Entrada Bruta: 4 casas) ---
    al = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Alumínio (Al3+)"
    )
    h_al = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Acidez Potencial (H+Al)"
    )

    # --- 7. Física (2 casas para precisão granulométrica) ---
    areia = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Areia %"
    )
    argila = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Argila %"
    )
    silte = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Silte %"
    )

    # --- 8. CALCULADOS (Saída para Laudo: 2 casas) ---
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
