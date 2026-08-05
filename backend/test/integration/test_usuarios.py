"""
Jornada 8 — Gestão de Técnicos (staff only)
Valida criação, listagem e remoção de técnicos, incluindo
validação de senha, unicidade e proteção contra auto-exclusão.
"""

import pytest
from django.contrib.auth.models import User


# ---------------------------------------------------------------------------
# 8.1 — Criar técnico com dados válidos → 201
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_tecnico_valido(client_autenticado):
    payload = {
        "username": "novo_tecnico",
        "email": "novo@labas.ufu.br",
        "nome": "Técnico Novo",
        "password": "SenhaForte@2026",
    }

    response = client_autenticado.post("/api/tecnicos/", payload, format="json")

    assert response.status_code == 201
    assert User.objects.filter(username="novo_tecnico").exists()


# ---------------------------------------------------------------------------
# 8.2 — Listar técnicos → 200 + lista com ao menos um elemento
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_listar_tecnicos(client_autenticado, tecnico):
    response = client_autenticado.get("/api/tecnicos/")

    assert response.status_code == 200
    usernames = [t["username"] for t in response.data["results"]]
    assert tecnico.username in usernames


# ---------------------------------------------------------------------------
# 8.3 — Senha fraca → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_tecnico_senha_fraca(client_autenticado):
    payload = {
        "username": "fraco_user",
        "email": "fraco@labas.ufu.br",
        "nome": "Usuário Fraco",
        "password": "123",
    }

    response = client_autenticado.post("/api/tecnicos/", payload, format="json")

    assert response.status_code == 400
    assert "password" in response.data


# ---------------------------------------------------------------------------
# 8.4 — Username duplicado → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_tecnico_username_duplicado(client_autenticado, tecnico):
    payload = {
        "username": tecnico.username,
        "email": "outro@labas.ufu.br",
        "nome": "Outro Técnico",
        "password": "SenhaForte@2026",
    }

    response = client_autenticado.post("/api/tecnicos/", payload, format="json")

    assert response.status_code == 400
    assert "username" in response.data


# ---------------------------------------------------------------------------
# 8.5 — E-mail duplicado → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_tecnico_email_duplicado(client_autenticado, tecnico):
    payload = {
        "username": "outro_user",
        "email": tecnico.email,
        "nome": "Outro Técnico",
        "password": "SenhaForte@2026",
    }

    response = client_autenticado.post("/api/tecnicos/", payload, format="json")

    assert response.status_code == 400
    assert "email" in response.data


# ---------------------------------------------------------------------------
# 8.6 — Técnico tenta remover a si mesmo → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_tecnico_nao_pode_remover_a_si_mesmo(client_autenticado, tecnico):
    response = client_autenticado.delete(f"/api/tecnicos/{tecnico.id}/")

    assert response.status_code == 400
    assert "detail" in response.data


# ---------------------------------------------------------------------------
# 8.7 — Remover outro técnico → 204
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_remover_outro_tecnico(client_autenticado):
    outro = User.objects.create_user(
        username="outro_tecnico", password="SenhaForte@2026",
        email="outro@labas.ufu.br", is_staff=True,
    )

    response = client_autenticado.delete(f"/api/tecnicos/{outro.id}/")

    assert response.status_code == 204
    assert not User.objects.filter(id=outro.id).exists()


# ---------------------------------------------------------------------------
# 8.8 — Acessar sem autenticação → 401
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_gestao_tecnicos_sem_autenticacao(client_anonimo):
    response = client_anonimo.get("/api/tecnicos/")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# 8.9 — Usuário autenticado sem is_staff tenta criar técnico → 403
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_tecnico_usuario_nao_staff(client_comum):
    payload = {
        "username": "tentativa_comum",
        "email": "comum@labas.ufu.br",
        "nome": "Usuário Comum",
        "password": "SenhaForte@2026",
    }

    response = client_comum.post("/api/tecnicos/", payload, format="json")

    assert response.status_code == 403
