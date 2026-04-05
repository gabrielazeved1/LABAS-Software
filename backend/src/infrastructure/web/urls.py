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
    path("register/", views.RegisterUserView.as_view(), name="user_register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.MeView.as_view(), name="me"),
    # ---------------------------------------------------------
    # 2 GESTAO DE LAUDOS RECURSOS PROTEGIDOS
    # ---------------------------------------------------------
    path("meus-laudos/<path:n_lab>/pdf/", views.gerar_laudo_pdf, name="laudo_pdf"),
    path("meus-laudos/", views.MeusLaudosAPIView.as_view(), name="listar_criar_laudos"),
    path(
        "meus-laudos/<path:n_lab>/",
        views.LaudoDetailAPIView.as_view(),
        name="laudo_detalhe",
    ),
    # ---------------------------------------------------------
    # 3 CALIBRACAO DE EQUIPAMENTOS (staff only)
    # ---------------------------------------------------------
    path(
        "baterias/",
        views.BateriaCalibracaoListCreateView.as_view(),
        name="baterias_list_create",
    ),
    path(
        "baterias/<int:pk>/",
        views.BateriaCalibracaoDetailView.as_view(),
        name="bateria_detail",
    ),
    path(
        "baterias/<int:bateria_id>/pontos/",
        views.PontoCalibracaoCreateView.as_view(),
        name="ponto_create",
    ),
    path(
        "pontos/<int:pk>/",
        views.PontoCalibracaoDestroyView.as_view(),
        name="ponto_destroy",
    ),
    # ---------------------------------------------------------
    # 4 OPERACAO EM LOTE (bancada) — staff only
    # ---------------------------------------------------------
    path(
        "amostras/",
        views.AmostrasPendentesListView.as_view(),
        name="amostras_pendentes",
    ),
    path(
        "leituras/",
        views.LeituraEquipamentoCreateView.as_view(),
        name="leitura_create",
    ),
]
