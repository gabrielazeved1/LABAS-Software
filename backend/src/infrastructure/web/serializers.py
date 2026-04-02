from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from src.infrastructure.database.models import Cliente, AnaliseSolo


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


# Serializer principal para os resultados das analises quimicas
class AnaliseSoloSerializer(serializers.ModelSerializer):
    """
    Centraliza a logica de transformacao dos resultados laboratoriais
    Aplica as validacoes tecnicas necessarias para o padrao UFU
    """

    # Inclui os dados do cliente de forma aninhada apenas para leitura
    cliente = ClienteSerializer(read_only=True)

    # Aplica regra de formato para o identificador do laboratorio
    n_lab = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{4}/.+$",
                message="O padrao do N Lab deve ser ANO/NUMERO ex 2026/001",
            )
        ]
    )

    class Meta:
        model = AnaliseSolo
        # Mapeia todos os atributos quimicos e fisicos para o formato JSON
        fields = [
            "n_lab",
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
