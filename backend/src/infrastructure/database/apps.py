from django.apps import AppConfig


class DatabaseConfig(AppConfig):
    """
    configuracao do App para a camada de infraestrutura de BD
    """

    default_auto_field = "django.db.models.BigAutoField"

    # deve corresponder ao caminho completo devido a estrutura de pastas personalizada
    name = "src.infrastructure.database"

    # nome de exibicao no django Admin
    verbose_name = "Banco de Dados (LABAS)"
