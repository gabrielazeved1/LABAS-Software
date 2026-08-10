import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class DatabaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.infrastructure.database"
    verbose_name = "Banco de Dados (LABAS)"

    def ready(self):
        logger.info("[SISTEMA] App de Banco de Dados carregado com sucesso.")
        try:
            import src.infrastructure.database.signals  # noqa: F401

            logger.info("[SISTEMA] Sinais de automacao registrados.")
        except ImportError as e:
            logger.error("[SISTEMA] Falha ao carregar sinais: %s", e)
