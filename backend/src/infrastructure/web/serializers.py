from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from src.infrastructure.database.models import (
    Cliente,
    AnaliseSolo,
    BateriaCalibracao,
    LeituraEquipamento,
    PontoCalibracao,
)


# Serializer para o processo de cadastro inicial no sistema
# Gerencia a criacao simultanea de credenciais e perfil do cliente
class UserRegistrationSerializer(serializers.Serializer):
    """
    Controlador de registro para novos produtores rurais
    Mantem a integridade entre a conta de acesso e os dados da fazenda
    """

    # Atributos de autenticacao do usuario
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    # Atributos de identificacao do cliente no laboratorio
    nome_cliente = serializers.CharField(max_length=255)
    codigo_cliente = serializers.CharField(max_length=50)
    municipio = serializers.CharField(max_length=100, required=False, allow_blank=True)
    area = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_username(self, value):
        """Impede a duplicidade de nomes de usuario no sistema"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuario ja existe")
        return value

    def validate_codigo_cliente(self, value):
        """Impede a duplicidade de codigo de cliente no sistema"""
        if Cliente.objects.filter(codigo=value).exists():
            raise serializers.ValidationError("Ja existe um cliente com este codigo")
        return value

    def create(self, validated_data):
        """Executa a persistencia de dados de forma protegida"""
        # Garante que ou ambos sao criados ou nenhum dado e salvo no banco
        with transaction.atomic():
            # Cria a conta de acesso com criptografia de senha automatica
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
            )

            try:
                # Vincula o perfil tecnico do cliente ao usuario recem criado
                Cliente.objects.create(
                    usuario=user,
                    nome=validated_data["nome_cliente"],
                    codigo=validated_data["codigo_cliente"],
                    municipio=validated_data.get("municipio", ""),
                    area=validated_data.get("area", ""),
                )
            except IntegrityError:
                raise serializers.ValidationError(
                    {"codigo_cliente": "Ja existe um cliente com este codigo"}
                )
        return validated_data


# Serializer simplificado para exibicao de dados do proprietario
class ClienteSerializer(serializers.ModelSerializer):
    """
    Formata as informacoes do cliente para consumo em laudos
    """

    class Meta:
        model = Cliente
        fields = ["codigo", "nome", "municipio", "area"]


class ClienteCadastroSerializer(serializers.ModelSerializer):
    """
    CRUD de clientes pelo staff.
    Nao cria conta de usuario — apenas dados cadastrais.
    O campo `codigo` e imutavel apos a criacao (read_only no update).
    """

    class Meta:
        model = Cliente
        fields = ["codigo", "nome", "contato", "municipio", "area", "observacoes"]

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
    Centraliza a logica de transformacao dos resultados laboratoriais
    Aplica as validacoes tecnicas necessarias para o padrao UFU
    """

    # Inclui os dados do cliente de forma aninhada apenas para leitura
    cliente = ClienteSerializer(read_only=True)

    # Campo de escrita: recebe o codigo do cliente para resolucao no create()
    cliente_codigo = serializers.CharField(write_only=True, required=True)

    # Aplica regra de formato e unicidade para o identificador do laboratorio
    n_lab = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{4}/.+$",
                message="O padrao do N Lab deve ser ANO/NUMERO ex 2026/001",
            ),
            UniqueValidator(
                queryset=AnaliseSolo.objects.all(),
                message="Ja existe um laudo registrado com este N Lab.",
            ),
        ]
    )

    def create(self, validated_data):
        cliente_codigo = validated_data.pop("cliente_codigo")
        try:
            cliente = Cliente.objects.get(codigo=cliente_codigo)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError(
                {"cliente_codigo": "Cliente nao encontrado com este codigo."}
            )
        return AnaliseSolo.objects.create(cliente=cliente, **validated_data)

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
        model = AnaliseSolo
        # Mapeia todos os atributos quimicos e fisicos para o formato JSON
        fields = [
            "n_lab",
            "cliente_codigo",
            "cliente",
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


# =============================================================================
# CALIBRACAO DE EQUIPAMENTOS
# =============================================================================


class PontoCalibracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PontoCalibracao
        fields = ["id", "bateria", "concentracao", "absorvancia"]
        read_only_fields = ["id"]


class BateriaCalibracaoSerializer(serializers.ModelSerializer):
    """Serializer de leitura — inclui pontos e equacao calculada."""

    pontos = PontoCalibracaoSerializer(many=True, read_only=True)
    equacao_formada = serializers.CharField(read_only=True)

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
            "ativo",
            "equacao_formada",
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
        """Delega validacao estequiometrica ao metodo clean() do model."""
        instance = BateriaCalibracao(**attrs)
        instance.clean()
        return attrs


class BateriaCalibracaoAtivoSerializer(serializers.ModelSerializer):
    """Serializer exclusivo para o PATCH de toggle ativo — aceita apenas o campo ativo."""

    class Meta:
        model = BateriaCalibracao
        fields = ["ativo"]


# =============================================================================
# OPERACAO EM LOTE (Bancada)
# =============================================================================


class AmostraPendenteSerializer(serializers.ModelSerializer):
    """
    Representacao minima de uma AnaliseSolo para a tela de Entrada em Lote.
    Expoe apenas os campos necessarios para identificar a amostra na bancada.
    """

    cliente_nome = serializers.CharField(source="cliente.nome", read_only=True)

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
