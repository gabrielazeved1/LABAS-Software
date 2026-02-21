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

    def ready(self):
        # Este print deve aparecer no terminal assim que você rodar o runserver
        print("✅ [SISTEMA] App de Banco de Dados carregado com sucesso!")
        try:
            import src.infrastructure.database.signals

            print("✅ [SISTEMA] Sinais de automação registrados!")
        except ImportError as e:
            print(f"❌ [ERRO] Falha ao carregar sinais: {e}")
