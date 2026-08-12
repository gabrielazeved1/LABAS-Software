from datetime import date
from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Cliente(models.Model):
    """
    Representa a entidade Cliente (Produtor Rural, Fazenda ou Empresa).
    Armazena dados cadastrais basicos e vinculo com o usuario do sistema.
    """

    nome = models.CharField(max_length=255, verbose_name="Solicitante")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Codigo")
    telefone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Telefone"
    )
    email = models.EmailField(
        max_length=254, blank=True, null=True, verbose_name="E-mail"
    )
    area = models.CharField(max_length=100, blank=True, null=True, verbose_name="Area")
    municipio = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Municipio"
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


class Laudo(models.Model):
    """
    Cabeçalho do documento entregue ao cliente.
    Agrupa N análises de solo (AnaliseSolo) em um único laudo.
    O código é gerado automaticamente no formato L-AAAA/N.
    """

    codigo_laudo = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="Código do Laudo",
    )
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="laudos"
    )
    data_emissao = models.DateField(
        default=date.today, verbose_name="Data de Entrada"
    )
    data_saida = models.DateField(blank=True, null=True, verbose_name="Data de Saída")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    def save(self, *args, **kwargs):
        if not self.codigo_laudo:
            with transaction.atomic():
                ano = timezone.now().year
                ultimo = (
                    Laudo.objects.select_for_update()
                    .filter(codigo_laudo__startswith=f"L-{ano}/")
                    .order_by("-id")
                    .first()
                )
                proximo_num = (
                    int(ultimo.codigo_laudo.split("/")[1]) + 1
                ) if ultimo else 1
                self.codigo_laudo = f"L-{ano}/{proximo_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_laudo} — {self.cliente.nome}"

    class Meta:
        verbose_name = "Laudo"
        verbose_name_plural = "Laudos"


class AnaliseSolo(models.Model):
    """
    Amostra individual de solo. Filho de Laudo (N análises por laudo, máx 50).
    Atributos agora possuem default=0 para evitar erros matematicos e nulos na API.
    """

    n_lab = models.CharField(max_length=50, unique=True, verbose_name="N Lab")
    laudo = models.ForeignKey(Laudo, on_delete=models.CASCADE, related_name="analises")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    referencia = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Referência Cliente"
    )
    data_entrada = models.DateField(default=date.today, verbose_name="Data Entrada")
    data_saida = models.DateField(blank=True, null=True, verbose_name="Data Saida")

    # [PHMETRO] Atributos de Acidez Ativa
    ph_agua = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="pH agua",
    )
    ph_cacl2 = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="pH CaCl2",
    )
    ph_kcl = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="pH KCl",
    )

    # [ESPECTROFOTOMETRO] Elementos de Extracao Otica
    p_m = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="P_M (Mehlich)",
    )
    p_r = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="P_R (Resina)",
    )
    p_rem = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="P-rem",
    )
    mo = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Materia Organica",
    )
    s = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Enxofre (S)",
    )
    b = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Boro (B)",
    )

    # [FOTOMETRO DE CHAMA] Emissao Direta
    k = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Potassio (K)",
    )
    na = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Sodio (Na)",
    )

    # [ABSORCAO ATOMICA] Macronutrientes Secundarios e Micronutrientes
    ca = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Calcio (Ca)",
    )
    mg = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Magnesio (Mg)",
    )
    cu = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Cobre (Cu)",
    )
    fe = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Ferro (Fe)",
    )
    mn = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Manganes (Mn)",
    )
    zn = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Zinco (Zn)",
    )

    # [TITULACAO] Volumetria
    al = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Aluminio (Al3+)",
    )
    h_al = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
        blank=True,
        null=True,
        verbose_name="Acidez Potencial (H+Al)",
    )

    # Granulometria Fisica
    areia = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="Areia %",
    )
    argila = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="Argila %",
    )
    silte = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="Silte %",
    )

    # Relacoes Agronomicas (Processadas pelo Use Case)
    sb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="SB",
    )
    t = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="t (CTC Efetiva)",
    )
    T_maiusculo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="T (CTC pH 7.0)",
    )
    V = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        default=0,
        blank=True,
        null=True,
        verbose_name="V% (Saturacao por Bases)",
    )
    m = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        default=0,
        blank=True,
        null=True,
        verbose_name="m% (Saturacao por Al)",
    )
    ca_mg = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="Relacao Ca/Mg",
    )
    ca_k = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="Relacao Ca/K",
    )
    mg_k = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="Relacao Mg/K",
    )
    c_org = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name="C-org",
    )

    def clean(self):
        """Validação de integridade antes do salvamento no banco."""
        campos_ph = [
            ("ph_agua", "pH em Água"),
            ("ph_cacl2", "pH em CaCl₂"),
            ("ph_kcl", "pH em KCl"),
        ]
        erros = {}
        for campo, label in campos_ph:
            valor = getattr(self, campo)
            if valor and (valor < 0 or valor > 14):
                erros[campo] = f"{label} deve estar entre 0 e 14."
        if erros:
            raise ValidationError(erros)

    def __str__(self):
        return f"Análise {self.n_lab} — Laudo {self.laudo.codigo_laudo}"

    class Meta:
        verbose_name = "Analise de Solo"
        verbose_name_plural = "Analises de Solo"


class ConjuntoPadrao(models.Model):
    """
    Agrupa as 4 linhas de referência (Padrão A/B e P.Labas A/B) sob um nome.
    Apenas um conjunto pode estar ativo por vez — o ativo é usado como padrão
    ao gerar PDFs sem especificar conjunto explicitamente.
    """

    nome = models.CharField(max_length=100, verbose_name="Nome do Conjunto")
    ativo = models.BooleanField(default=False, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.ativo:
            with transaction.atomic():
                ConjuntoPadrao.objects.select_for_update().filter(ativo=True).exclude(
                    pk=self.pk
                ).update(ativo=False)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        status = " [ATIVO]" if self.ativo else ""
        return f"{self.nome}{status}"

    class Meta:
        verbose_name = "Conjunto de Padroes"
        verbose_name_plural = "Conjuntos de Padroes"
        ordering = ["-criado_em"]


class PadraoLaboratorio(models.Model):
    """
    Uma das 4 linhas de referência dentro de um ConjuntoPadrao.
    Campos químicos são opcionais: None aparece como '*' no PDF gerado.
    """

    TIPO_CHOICES = [
        ("padrao_a", "Padrão A"),
        ("padrao_b", "Padrão B"),
        ("p_labas_a", "P. Labas A"),
        ("p_labas_b", "P. Labas B"),
    ]
    TIPO_ORDEM = ["padrao_a", "padrao_b", "p_labas_a", "p_labas_b"]

    conjunto = models.ForeignKey(
        ConjuntoPadrao, on_delete=models.CASCADE, related_name="padroes"
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")

    ph_agua = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True, verbose_name="pH agua")
    ph_cacl2 = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True, verbose_name="pH CaCl2")
    ph_kcl = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True, verbose_name="pH KCl")
    p_m = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="P_M (Mehlich)")
    p_r = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="P_R (Resina)")
    p_rem = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="P-rem")
    mo = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Materia Organica")
    s = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Enxofre (S)")
    b = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Boro (B)")
    k = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Potassio (K)")
    na = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Sodio (Na)")
    ca = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Calcio (Ca)")
    mg = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Magnesio (Mg)")
    cu = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Cobre (Cu)")
    fe = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Ferro (Fe)")
    mn = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Manganes (Mn)")
    zn = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Zinco (Zn)")
    al = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Aluminio (Al3+)")
    h_al = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Acidez Potencial (H+Al)")
    sb = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="SB")
    t = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="t (CTC Efetiva)")
    T_maiusculo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="T (CTC pH 7.0)")
    V = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name="V%")
    m = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name="m%")
    ca_mg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Ca/Mg")
    ca_k = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Ca/K")
    mg_k = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Mg/K")
    c_org = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="C-org")

    @property
    def n_lab(self):
        return dict(self.TIPO_CHOICES)[self.tipo]

    @property
    def referencia(self):
        return "*"

    def __str__(self):
        return f"{self.conjunto.nome} — {self.get_tipo_display()}"

    class Meta:
        verbose_name = "Padrao do Laboratorio"
        verbose_name_plural = "Padroes do Laboratorio"
        constraints = [
            models.UniqueConstraint(
                fields=["conjunto", "tipo"], name="unique_tipo_por_conjunto"
            )
        ]
        ordering = ["tipo"]


class BateriaCalibracao(models.Model):
    """
    Representa a configuracao diaria dos equipamentos.
    Agrupa os pontos de calibracao e define as variaveis estequiometricas
    que serao utilizadas no calculo das amostras do dia.
    """

    EQUIPAMENTO_CHOICES = [
        ("AA", "Absorcao Atomica"),
        ("FC", "Fotometro de Chama"),
        ("ES", "Espectrofotometro"),
        ("TI", "Titulacao"),
        ("PH", "pHmetro"),
    ]
    ELEMENTO_CHOICES = [
        ("Ca", "Calcio"),
        ("Mg", "Magnesio"),
        ("Cu", "Cobre"),
        ("Fe", "Ferro"),
        ("Mn", "Manganes"),
        ("Zn", "Zinco"),
        ("K", "Potassio"),
        ("Na", "Sodio"),
        ("P_M", "Fosforo (Mehlich)"),
        ("P_R", "Fosforo (Resina)"),
        ("P_rem", "Fosforo Remanescente"),
        ("S", "Enxofre"),
        ("B", "Boro"),
        ("Al", "Aluminio"),
        ("H_Al", "Acidez Potencial"),
        ("ph_agua", "pH em Agua"),
        ("ph_cacl2", "pH em CaCl2"),
        ("ph_kcl", "pH em KCl"),
        ("MO", "Materia Organica"),
    ]

    volume_solo = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="Volume de Solo (cm3)",
    )
    volume_extrator = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Volume de Extrator (ml)",
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data da Calibracao"
    )
    equipamento = models.CharField(max_length=2, choices=EQUIPAMENTO_CHOICES)
    elemento = models.CharField(max_length=15, choices=ELEMENTO_CHOICES)

    # Coeficientes gerados dinamicamente pelo motor matematico
    coeficiente_angular_a = models.DecimalField(
        max_digits=15,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name="Inclinação (a) — slope",
    )
    coeficiente_linear_b = models.DecimalField(
        max_digits=15,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name="Intercepto (b) — intercept",
    )
    r_quadrado = models.DecimalField(
        max_digits=7, decimal_places=6, blank=True, null=True, verbose_name="R2"
    )
    leitura_branco = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Leitura do Branco",
    )
    @property
    def equacao_formada(self):
        """Gera a string visual da equacao da reta para os paineis."""
        if (
            self.coeficiente_angular_a is not None
            and self.coeficiente_linear_b is not None
        ):
            a, b = self.coeficiente_angular_a, self.coeficiente_linear_b
            sinal = "+" if b >= 0 else "-"
            return f"y = {a:.6f}x {sinal} {abs(b):.6f}"
        return "Equacao ainda nao gerada"

    def clean(self):
        """Valida obrigatoriedade de campos dependendo do equipamento escolhido."""
        erros = {}
        # MO usa fórmula fixa sem volumes (alinhado com o signal gatekeeper)
        if self.equipamento in ["AA", "FC", "ES"] and self.elemento != "MO":
            if self.volume_solo is None:
                erros["volume_solo"] = (
                    f"Obrigatorio informar o Volume de Solo para {self.get_equipamento_display()}."
                )
            if self.volume_extrator is None:
                erros["volume_extrator"] = (
                    f"Obrigatorio informar o Volume de Extrator para {self.get_equipamento_display()}."
                )

        if self.equipamento in ["AA", "TI"] and self.leitura_branco is None:
            erros["leitura_branco"] = (
                f"A Leitura do Branco e OBRIGATORIA para {self.get_equipamento_display()}."
            )

        if erros:
            raise ValidationError(erros)

    def __str__(self):
        data_formatada = self.data_criacao.strftime("%d/%m/%Y")
        instrucoes = {
            "ES": "a TRANSMITANCIA %",
            "AA": "a ABSORBANCIA",
            "FC": "a EMISSAO",
            "PH": "o pH DIRETO",
            "TI": "o volume a subtrair do BRANCO",
        }
        instrucao = instrucoes.get(self.equipamento, "")
        return f"{self.get_elemento_display()} - {data_formatada} ({self.get_equipamento_display()} -> Digite {instrucao})"

    class Meta:
        verbose_name = "Bateria de Calibracao"
        verbose_name_plural = "Baterias de Calibracao"


class LeituraEquipamento(models.Model):
    """
    Entidade intermediaria que registra as leituras brutas vindas do laboratorio
    e conecta a amostra (Laudo) com a bateria especifica do dia.
    """

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
        verbose_name="Fator de Diluicao (Opcional)",
    )

    def clean(self):
        """Valida integridade estequiometrica da leitura."""
        if hasattr(self, "bateria") and self.bateria is not None:
            # MO usa fórmula fixa sem diluição (alinhado com o signal gatekeeper)
            if self.bateria.equipamento in ["AA", "FC", "ES"] and self.bateria.elemento != "MO":
                if self.fator_diluicao is None:
                    raise ValidationError(
                        {
                            "fator_diluicao": f"O Fator de Diluicao e OBRIGATORIO na leitura de {self.bateria.get_equipamento_display()}."
                        }
                    )

    class Meta:
        verbose_name = "Leitura de Equipamento"
        verbose_name_plural = "Leituras de Equipamento"
        constraints = [
            models.UniqueConstraint(
                fields=["analise", "bateria"],
                name="unique_leitura_por_analise_bateria",
            )
        ]

    def __str__(self):
        return f"Laudo {self.analise.n_lab} | {self.bateria.get_elemento_display()}: {self.leitura_bruta}"


class PontoCalibracao(models.Model):
    """
    Representa os padroes de concentracao conhecidos utilizados
    para formar a curva de regressao linear da bateria do dia.
    """

    bateria = models.ForeignKey(
        BateriaCalibracao, on_delete=models.CASCADE, related_name="pontos"
    )
    concentracao = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Concentracao (Padrao)"
    )
    absorvancia = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Leitura Bruta (Transm % ou Abs)"
    )

    class Meta:
        verbose_name = "Ponto de Calibracao"
        verbose_name_plural = "Pontos de Calibracao"
        ordering = ["concentracao"]

    def __str__(self):
        return f"{self.concentracao} -> {self.absorvancia}"
