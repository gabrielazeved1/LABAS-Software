"""
Jornada 1 — Autenticação
Valida que nenhum técnico consegue operar sem se autenticar e que
o endpoint /api/register/ não é mais publicamente acessível (fix C-01).
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


# ---------------------------------------------------------------------------
# 1.1 — Login com credenciais válidas
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_login_credenciais_validas(tecnico):
    client = APIClient()
    response = client.post("/api/token/", {
        "username": "tecnico_teste",
        "password": "SenhaForte@2026",
    }, format="json")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


# ---------------------------------------------------------------------------
# 1.2 — Login com senha errada
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_login_senha_errada(tecnico):
    client = APIClient()
    response = client.post("/api/token/", {
        "username": "tecnico_teste",
        "password": "senha_errada",
    }, format="json")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# 1.3 — Login com usuário inexistente
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_login_usuario_inexistente(db):
    client = APIClient()
    response = client.post("/api/token/", {
        "username": "nao_existe",
        "password": "qualquer",
    }, format="json")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# 1.4 — Acesso a endpoint protegido sem token
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_endpoint_protegido_sem_token(db):
    client = APIClient()
    response = client.get("/api/clientes/")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# 1.5 — Acesso com token adulterado
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_token_adulterado(db):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer tokeninvalido.adulterado.aqui")
    response = client.get("/api/clientes/")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# 1.6 — Refresh do access token
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_refresh_token(tecnico):
    client = APIClient()
    login = client.post("/api/token/", {
        "username": "tecnico_teste",
        "password": "SenhaForte@2026",
    }, format="json")

    refresh_token = login.data["refresh"]
    response = client.post("/api/token/refresh/", {
        "refresh": refresh_token,
    }, format="json")

    assert response.status_code == 200
    assert "access" in response.data


# ---------------------------------------------------------------------------
# 1.7 — Regressão C-01: /api/register/ não é mais público
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_register_sem_autenticacao_retorna_401(db):
    """
    C-01: endpoint /api/register/ era AllowAny e criava usuários como is_staff=True.
    Após a correção deve exigir autenticação (IsAuthenticated + IsStaff).
    """
    client = APIClient()
    response = client.post("/api/register/", {
        "username": "invasor",
        "email": "invasor@mal.com",
        "nome": "Invasor",
        "password": "SenhaForte@2026",
    }, format="json")

    assert response.status_code == 401
    assert not User.objects.filter(username="invasor").exists()


@pytest.mark.django_db
def test_register_usuario_nao_staff_retorna_403(tecnico_comum):
    """Usuário autenticado mas sem is_staff não pode registrar técnicos."""
    client = APIClient()
    client.force_authenticate(user=tecnico_comum)
    response = client.post("/api/register/", {
        "username": "novo",
        "email": "novo@labas.com",
        "nome": "Novo Técnico",
        "password": "SenhaForte@2026",
    }, format="json")

    assert response.status_code == 403
    assert not User.objects.filter(username="novo").exists()


@pytest.mark.django_db
def test_register_staff_cria_tecnico_com_sucesso(tecnico):
    """Técnico staff pode registrar novos técnicos via /api/register/."""
    client = APIClient()
    client.force_authenticate(user=tecnico)
    response = client.post("/api/register/", {
        "username": "novo_tecnico",
        "email": "novo@labas.com",
        "nome": "Novo Técnico",
        "password": "SenhaForte@2026",
    }, format="json")

    assert response.status_code == 201
    novo = User.objects.get(username="novo_tecnico")
    assert novo.is_staff is True
