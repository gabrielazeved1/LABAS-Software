"""
URL configuration for setup project.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Rota padrao do painel de administracao (Uso interno do laboratorio)
    path("admin/", admin.site.urls),
    # Rota raiz da nossa API (Uso externo pelos clientes)
    # Delega o roteamento para a camada de infraestrutura web
    path("api/", include("src.infrastructure.web.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
