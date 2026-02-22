from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MeusLaudosAPIView

app_name = "web_api"

urlpatterns = [
    # Rota para login e obtencao do token
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Rota para renovar o acesso sem precisar logar novamente
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Rota protegida dos laudos
    path("meus-laudos/", MeusLaudosAPIView.as_view(), name="listar_meus_laudos"),
]
