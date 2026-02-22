from rest_framework import serializers
from django.core.validators import RegexValidator
from src.infrastructure.database.models import Cliente, AnaliseSolo


class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para a entidade Cliente.
    Focado nos dados basicos para exibicao no laudo.
    """

    class Meta:
        model = Cliente
        fields = ["codigo", "nome", "municipio", "area"]


class AnaliseSoloSerializer(serializers.ModelSerializer):
    """
    Serializer principal da API LABAS.
    Transforma os dados da AnaliseSolo em JSON, garantindo que o padrao
    de identificacao seja respeitado.
    """

    cliente = ClienteSerializer(read_only=True)

    # Validacao de negocio: Impede IDs invalidos como "teste"
    # Aceita apenas o padrao: 4 digitos / qualquer coisa (Ex: 2026/001)
    n_lab = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{4}/.+$",
                message="O padrao do N. Lab deve ser ANO/NUMERO (ex: 2026/001)",
            )
        ]
    )

    class Meta:
        model = AnaliseSolo
        # Listamos todos os campos para que a API seja completa para o Frontend
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
            # Calculos Agronomicos
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
