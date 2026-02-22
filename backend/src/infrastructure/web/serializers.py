from rest_framework import serializers
from src.infrastructure.database.models import Cliente, AnaliseSolo


# funciona como um dto em java
class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para a entidade Cliente.
    Filtra e transforma os dados cadastrais publicos em formato JSON para a API.
    """

    class Meta:
        model = Cliente
        fields = ["codigo", "nome", "municipio", "area"]


class AnaliseSoloSerializer(serializers.ModelSerializer):
    """
    Serializer principal do sistema para entrega do Laudo final ao cliente.
    Responsavel por empacotar os resultados quimicos, fisicos e as
    relacoes agronomicas processadas pelo Use Case.
    """

    # Nested Serializer: Traz os dados do cliente aninhados dentro do laudo,
    # evitando que o frontend precise fazer duas requisicoes de rede separadas.
    cliente = ClienteSerializer(read_only=True)

    class Meta:
        model = AnaliseSolo
        # A declaracao explicita de fields funciona como uma lista de permissao (allowlist).
        # Garante que dados internos de infraestrutura do sistema nunca vazem na API.
        fields = [
            "n_lab",
            "cliente",
            "data_entrada",
            "data_saida",
            # Acidez Ativa
            "ph_agua",
            "ph_cacl2",
            "ph_kcl",
            # Extracao Otica
            "p_m",
            "p_r",
            "p_rem",
            "mo",
            "s",
            "b",
            # Fotometria e Absorcao
            "k",
            "na",
            "ca",
            "mg",
            "cu",
            "fe",
            "mn",
            "zn",
            # Volumetria
            "al",
            "h_al",
            # Fisica do Solo
            "areia",
            "argila",
            "silte",
            # Resultados Agronomicos Calculados (Gerados pelo Use Case)
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
