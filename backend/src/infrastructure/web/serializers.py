from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.contrib.auth.password_validation import validate_password
from src.infrastructure.database.models import (
    Cliente,
    ConjuntoPadrao,
    Laudo,
    AnaliseSolo,
    BateriaCalibracao,
    LeituraEquipamento,
    PontoCalibracao,
    PadraoLaboratorio,
)


# =============================================================================
# GESTAO DE TECNICOS (staff only)
# =============================================================================

class TecnicoSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "nome", "date_joined"]

    def get_nome(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class TecnicoCriarSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    nome = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Nome de usuario ja existe")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("E-mail ja esta em uso")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        nome_parts = validated_data["nome"].split(" ", 1)
        first_name = nome_parts[0]
        last_name = nome_parts[1] if len(nome_parts) > 1 else ""
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
        )


# Serializer simplificado para exibicao de dados do proprietario
class ClienteSerializer(serializers.ModelSerializer):
    """
    Formata as informacoes do cliente para consumo em laudos
    """

    class Meta:
        model = Cliente
        fields = ["codigo", "nome", "municipio", "area", "telefone", "email"]


class LaudoSerializer(serializers.ModelSerializer):
    """
    Serializer do cabeçalho do laudo.
    Leitura: retorna objeto cliente aninhado.
    Escrita: recebe cliente_codigo para resolucao.
    """

    cliente = ClienteSerializer(read_only=True)
    cliente_codigo = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        cliente_codigo = validated_data.pop("cliente_codigo")
        try:
            cliente = Cliente.objects.get(codigo=cliente_codigo)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError(
                {"cliente_codigo": "Cliente nao encontrado com este codigo."}
            )
        return Laudo.objects.create(cliente=cliente, **validated_data)

    def update(self, instance, validated_data):
        cliente_codigo = validated_data.pop("cliente_codigo", None)
        if cliente_codigo:
            try:
                instance.cliente = Cliente.objects.get(codigo=cliente_codigo)
            except Cliente.DoesNotExist:
                raise serializers.ValidationError(
                    {"cliente_codigo": "Cliente nao encontrado com este codigo."}
                )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Laudo
        fields = [
            "id",
            "codigo_laudo",
            "cliente_codigo",
            "cliente",
            "data_emissao",
            "data_saida",
            "observacoes",
        ]
        read_only_fields = ["id", "codigo_laudo"]


class ClienteCadastroSerializer(serializers.ModelSerializer):
    """
    CRUD de clientes pelo staff.
    Nao cria conta de usuario — apenas dados cadastrais.
    O campo `codigo` e imutavel apos a criacao (read_only no update).
    """

    class Meta:
        model = Cliente
        fields = [
            "codigo",
            "nome",
            "telefone",
            "email",
            "municipio",
            "area",
            "observacoes",
        ]

    def validate_codigo(self, value):
        # Na atualizacao (instance ja existe), ignora a validacao de unicidade
        if self.instance and self.instance.codigo == value:
            return value
        if Cliente.objects.filter(codigo=value).exists():
            raise serializers.ValidationError("Ja existe um cliente com este codigo.")
        return value


# Serializer principal para os resultados das analises quimicas
class AnaliseSoloSerializer(serializers.ModelSerializer):
    """
    Centraliza a logica de transformacao dos resultados laboratoriais.
    Analise e sempre filha de um Laudo — laudo_id e inferido pelo contexto da view.
    """

    laudo_id = serializers.IntegerField(read_only=True)

    # Mantém validacao de formato mas unicidade é por laudo (validada em validate())
    n_lab = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{4}/\d{3,}$",
                message="O padrão do N Lab deve ser ANO/NUMERO, ex: 2026/001",
            ),
        ]
    )

    def validate_n_lab(self, value):
        """N_Lab é o número de protocolo único da amostra no laboratório — nunca se repete."""
        qs = AnaliseSolo.objects.filter(n_lab=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f"Já existe uma amostra com N_Lab '{value}' cadastrada no sistema."
            )
        return value

    class Meta:
        model = AnaliseSolo
        fields = [
            "id",
            "laudo_id",
            "n_lab",
            "ativo",
            "referencia",
            "data_entrada",
            "data_saida",
            "ph_agua",
            "ph_cacl2",
            "ph_kcl",
            "p_m",
            "p_r",
            "p_rem",
            "mo",
            "s",
            "b",
            "k",
            "na",
            "ca",
            "mg",
            "cu",
            "fe",
            "mn",
            "zn",
            "al",
            "h_al",
            "areia",
            "argila",
            "silte",
            "sb",
            "t",
            "T_maiusculo",
            "V",
            "m",
            "ca_mg",
            "ca_k",
            "mg_k",
            "c_org",
        ]
        read_only_fields = [
            "id",
            "laudo_id",
            "sb",
            "t",
            "T_maiusculo",
            "V",
            "m",
            "ca_mg",
            "ca_k",
            "mg_k",
            "c_org",
        ]


# =============================================================================
# PADROES DO LABORATORIO
# =============================================================================

CAMPOS_QUIMICOS_PADRAO = [
    "ph_agua", "ph_cacl2", "ph_kcl",
    "p_m", "p_r", "p_rem", "mo", "s", "b",
    "k", "na", "ca", "mg", "cu", "fe", "mn", "zn",
    "al", "h_al", "sb", "t", "T_maiusculo", "V", "m",
    "ca_mg", "ca_k", "mg_k", "c_org",
]


class PadraoLaboratorioSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model = PadraoLaboratorio
        fields = ["id", "tipo", "tipo_display"] + CAMPOS_QUIMICOS_PADRAO
        read_only_fields = ["id", "tipo", "tipo_display"]


class ConjuntoPadraoSerializer(serializers.ModelSerializer):
    padroes = PadraoLaboratorioSerializer(many=True, read_only=True)

    class Meta:
        model = ConjuntoPadrao
        fields = ["id", "nome", "ativo", "criado_em", "atualizado_em", "padroes"]
        read_only_fields = ["id", "ativo", "criado_em", "atualizado_em"]


# =============================================================================
# CALIBRACAO DE EQUIPAMENTOS
# =============================================================================


class PontoCalibracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PontoCalibracao
        fields = ["id", "bateria", "concentracao", "absorvancia"]
        read_only_fields = ["id", "bateria"]


class BateriaCalibracaoSerializer(serializers.ModelSerializer):
    """Serializer de leitura — inclui pontos e equacao calculada."""

    pontos = PontoCalibracaoSerializer(many=True, read_only=True)
    equacao_formada = serializers.CharField(read_only=True)
    leituras_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BateriaCalibracao
        fields = [
            "id",
            "equipamento",
            "elemento",
            "volume_solo",
            "volume_extrator",
            "data_criacao",
            "coeficiente_angular_a",
            "coeficiente_linear_b",
            "r_quadrado",
            "leitura_branco",
            "equacao_formada",
            "leituras_count",
            "pontos",
        ]
        read_only_fields = [
            "id",
            "data_criacao",
            "coeficiente_angular_a",
            "coeficiente_linear_b",
            "r_quadrado",
            "equacao_formada",
        ]

    def validate(self, attrs):
        """Delega validação estequiométrica ao clean() do model."""
        from django.core.exceptions import ValidationError as DjangoValidationError
        instance = self.instance or BateriaCalibracao()
        for k, v in attrs.items():
            setattr(instance, k, v)
        try:
            instance.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs


# =============================================================================
# OPERACAO EM LOTE (Bancada)
# =============================================================================


class AmostraPendenteSerializer(serializers.ModelSerializer):
    """
    Representacao minima de uma AnaliseSolo para a tela de Entrada em Lote.
    Expoe apenas os campos necessarios para identificar a amostra na bancada.
    """

    cliente_nome = serializers.CharField(source="laudo.cliente.nome", read_only=True)

    class Meta:
        model = AnaliseSolo
        fields = ["id", "n_lab", "cliente_nome", "data_entrada"]


class LeituraEquipamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de leituras brutas vindas da bancada.
    Apos o save, o signal automaticamente calcula e persiste o resultado
    no campo correspondente da AnaliseSolo.
    """

    class Meta:
        model = LeituraEquipamento
        fields = ["id", "analise", "bateria", "leitura_bruta", "fator_diluicao"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        """Delega validacao estequiometrica ao metodo clean() do model."""
        instance = LeituraEquipamento(**attrs)
        instance.clean()
        return attrs


class LeituraEquipamentoDetalheSerializer(serializers.ModelSerializer):
    """
    Serializer de leitura para visualizacao e correcao.
    Expoe elemento e equipamento da bateria para o frontend poder
    rotular cada linha sem precisar de chamadas adicionais.
    """

    elemento = serializers.CharField(source="bateria.elemento", read_only=True)
    elemento_display = serializers.CharField(
        source="bateria.get_elemento_display", read_only=True
    )
    equipamento = serializers.CharField(source="bateria.equipamento", read_only=True)
    resultado_calculado = serializers.SerializerMethodField()

    class Meta:
        model = LeituraEquipamento
        fields = [
            "id",
            "bateria",
            "elemento",
            "elemento_display",
            "equipamento",
            "leitura_bruta",
            "fator_diluicao",
            "resultado_calculado",
        ]
        read_only_fields = [
            "id",
            "bateria",
            "elemento",
            "elemento_display",
            "equipamento",
            "resultado_calculado",
        ]

    def get_resultado_calculado(self, obj):
        campo = obj.bateria.elemento.lower()
        valor = getattr(obj.analise, campo, None)
        return float(valor) if valor is not None else None
