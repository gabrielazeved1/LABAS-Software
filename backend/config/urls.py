"""
URL configuration for setup project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Rota padrao do painel de administracao (Uso interno do laboratorio)
    path("admin/", admin.site.urls),
    # Rota raiz da nossa API (Uso externo pelos clientes)
    # Delega o roteamento para a camada de infraestrutura web
    path("api/", include("src.infrastructure.web.urls")),
]
