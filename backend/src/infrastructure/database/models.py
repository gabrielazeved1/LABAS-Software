from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Cliente(models.Model):
    """
    Representa a entidade Cliente (Produtor Rural, Fazenda ou Empresa).
    Armazena dados cadastrais basicos e vinculo com o usuario do sistema.
    """

    nome = models.CharField(max_length=255, verbose_name="Solicitante")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Codigo Cliente")
    contato = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Contato"
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


class AnaliseSolo(models.Model):
    """
    Entidade central do sistema (O Laudo).
    Armazena todos os macronutrientes, micronutrientes, atributos fisicos
    e as relacoes agronomicas calculadas pelo Use Case.
    """

    n_lab = models.CharField(max_length=50, unique=True, verbose_name="N Lab")
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="analises"
    )
    data_entrada = models.DateField(default=timezone.now, verbose_name="Data Entrada")
    data_saida = models.DateField(blank=True, null=True, verbose_name="Data Saida")

    # [PHMETRO] Atributos de Acidez Ativa
    ph_agua = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH agua"
    )
    ph_cacl2 = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH CaCl2"
    )
    ph_kcl = models.DecimalField(
        max_digits=8, decimal_places=4, blank=True, null=True, verbose_name="pH KCl"
    )

    # [ESPECTROFOTOMETRO] Elementos de Extracao Otica
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
        verbose_name="Materia Organica",
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

    # [FOTOMETRO DE CHAMA] Emissao Direta
    k = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Potassio (K)",
    )
    na = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Sodio (Na)",
    )

    # [ABSORCAO ATOMICA] Macronutrientes Secundarios e Micronutrientes
    ca = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Calcio (Ca)",
    )
    mg = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Magnesio (Mg)",
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
        verbose_name="Manganes (Mn)",
    )
    zn = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Zinco (Zn)",
    )

    # [TITULACAO] Volumetria
    al = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Aluminio (Al3+)",
    )
    h_al = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Acidez Potencial (H+Al)",
    )

    # Granulometria Fisica
    areia = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Areia %"
    )
    argila = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Argila %"
    )
    silte = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Silte %"
    )

    # Relacoes Agronomicas (Processadas pelo Use Case)
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
        verbose_name="V% (Saturacao por Bases)",
    )
    m = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name="m% (Saturacao por Al)",
    )
    ca_mg = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Relacao Ca/Mg",
    )
    ca_k = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Relacao Ca/K",
    )
    mg_k = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Relacao Mg/K",
    )
    c_org = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="C-org"
    )

    def clean(self):
        """Validacao de integridade antes do salvamento no banco."""
        if self.ph_agua and (self.ph_agua < 0 or self.ph_agua > 14):
            raise ValidationError({"ph_agua": "O pH deve estar entre 0 e 14."})

    def __str__(self):
        return f"Laudo {self.n_lab} - {self.cliente.nome}"

    class Meta:
        verbose_name = "Analise de Solo"
        verbose_name_plural = "Analises de Solo"


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
        ("PH", "Phagametro"),
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
        verbose_name="Inclinacao (b)",
    )
    coeficiente_linear_b = models.DecimalField(
        max_digits=15,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name="Intercepto (a)",
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
    ativo = models.BooleanField(default=True, verbose_name="Bateria Ativa no Dia?")

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
        if self.equipamento in ["AA", "FC", "ES"]:
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
            if self.bateria.equipamento in ["AA", "FC", "ES"]:
                if self.fator_diluicao is None:
                    raise ValidationError(
                        {
                            "fator_diluicao": f"O Fator de Diluicao e OBRIGATORIO na leitura de {self.bateria.get_equipamento_display()}."
                        }
                    )

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
