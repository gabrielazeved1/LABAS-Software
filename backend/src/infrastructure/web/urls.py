from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

# Namespace para identificacao das rotas do modulo web
app_name = "web_api"

urlpatterns = [
    # ---------------------------------------------------------
    # 1 AUTENTICACAO E ACESSO PUBLICO
    # ---------------------------------------------------------
    # Rota para criacao de conta de novos clientes e seus perfis
    path("register/", views.RegisterUserView.as_view(), name="user_register"),
    # Endpoints do SimpleJWT para geracao e renovacao de tokens de acesso
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ---------------------------------------------------------
    # 2 GESTAO DE LAUDOS RECURSOS PROTEGIDOS
    # ---------------------------------------------------------
    # Rota de geracao de PDF posicionada estrategicamente no topo
    # Previne que o identificador path capture o sufixo pdf como parte do n_lab
    path("meus-laudos/<path:n_lab>/pdf/", views.gerar_laudo_pdf, name="laudo_pdf"),
    # Listagem geral e criacao de novos laudos por tecnicos
    path("meus-laudos/", views.MeusLaudosAPIView.as_view(), name="listar_criar_laudos"),
    # Operacoes detalhadas de busca edicao ou exclusao via identificador unico
    path(
        "meus-laudos/<path:n_lab>/",
        views.LaudoDetailAPIView.as_view(),
        name="laudo_detalhe",
    ),
]
