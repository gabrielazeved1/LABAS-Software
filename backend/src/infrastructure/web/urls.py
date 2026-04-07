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
    # 2 GESTAO DE LAUDOS — arquitetura 1:N
    # ---------------------------------------------------------
    path("laudos/", views.LaudoListCreateView.as_view(), name="laudo_list_create"),
    path("laudos/<int:pk>/", views.LaudoDetailView.as_view(), name="laudo_detail"),
    path("laudos/<int:pk>/pdf/", views.gerar_laudo_pdf, name="laudo_pdf"),
    path(
        "laudos/<int:laudo_pk>/analises/",
        views.AnaliseSoloListCreateView.as_view(),
        name="analise_list_create",
    ),
    path(
        "laudos/<int:laudo_pk>/analises/<int:pk>/",
        views.AnaliseSoloDetailView.as_view(),
        name="analise_detail",
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
    path(
        "leituras/<int:pk>/",
        views.LeituraEquipamentoDetailView.as_view(),
        name="leitura_detail",
    ),
    path(
        "analises/<int:analise_id>/leituras/",
        views.LeiturasPorAnaliseListView.as_view(),
        name="leituras_por_analise",
    ),
    # ---------------------------------------------------------
    # 5 GESTAO DE CLIENTES (staff only)
    # ---------------------------------------------------------
    path(
        "clientes/",
        views.ClienteListCreateView.as_view(),
        name="clientes_list_create",
    ),
    path(
        "clientes/<str:codigo>/",
        views.ClienteDetailView.as_view(),
        name="cliente_detail",
    ),
    # ---------------------------------------------------------
    # 6 DASHBOARD DO TÉCNICO
    # ---------------------------------------------------------
    path(
        "dashboard/stats/",
        views.DashboardStatsView.as_view(),
        name="dashboard_stats",
    ),
    path(
        "dashboard/laudos-recentes/",
        views.DashboardLaudosRecentesView.as_view(),
        name="dashboard_laudos_recentes",
    ),
]
