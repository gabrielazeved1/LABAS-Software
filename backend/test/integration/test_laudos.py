"""
Jornada 4 — Laudos e Análises
Valida criação de laudos com geração automática de código sequencial,
validação de n_lab (formato e unicidade global) e controle de acesso.
"""

import pytest


# ---------------------------------------------------------------------------
# 4.1 — Criar laudo vinculado a cliente existente
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_laudo(client_autenticado, cliente):
    response = client_autenticado.post("/api/laudos/", {
        "cliente_codigo": "C-001",
        "data_emissao": "2026-08-05",
    }, format="json")

    assert response.status_code == 201
    assert response.data["codigo_laudo"].startswith("L-2026/")
    assert response.data["cliente"]["codigo"] == "C-001"


# ---------------------------------------------------------------------------
# 4.2 — Segundo laudo no mesmo ano incrementa o sequencial
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_segundo_laudo_incrementa_sequencial(client_autenticado, cliente):
    r1 = client_autenticado.post("/api/laudos/", {
        "cliente_codigo": "C-001",
        "data_emissao": "2026-08-05",
    }, format="json")
    r2 = client_autenticado.post("/api/laudos/", {
        "cliente_codigo": "C-001",
        "data_emissao": "2026-08-05",
    }, format="json")

    assert r1.status_code == 201
    assert r2.status_code == 201

    n1 = int(r1.data["codigo_laudo"].split("/")[1])
    n2 = int(r2.data["codigo_laudo"].split("/")[1])
    assert n2 == n1 + 1


# ---------------------------------------------------------------------------
# 4.3 — Cliente inexistente → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_laudo_cliente_inexistente(client_autenticado):
    response = client_autenticado.post("/api/laudos/", {
        "cliente_codigo": "INEXISTENTE",
        "data_emissao": "2026-08-05",
    }, format="json")

    assert response.status_code == 400
    assert "cliente_codigo" in response.data


# ---------------------------------------------------------------------------
# 4.4 — Adicionar análise com n_lab válido
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_adicionar_analise(client_autenticado, laudo):
    response = client_autenticado.post(
        f"/api/laudos/{laudo.id}/analises/",
        {"n_lab": "2026/001"},
        format="json",
    )

    assert response.status_code == 201
    assert response.data["n_lab"] == "2026/001"
    assert response.data["laudo_id"] == laudo.id


# ---------------------------------------------------------------------------
# 4.5 — n_lab duplicado → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_n_lab_duplicado(client_autenticado, laudo, analise):
    # analise fixture já usa "2026/001"
    response = client_autenticado.post(
        f"/api/laudos/{laudo.id}/analises/",
        {"n_lab": "2026/001"},
        format="json",
    )

    assert response.status_code == 400
    assert "n_lab" in response.data


# ---------------------------------------------------------------------------
# 4.6 — n_lab com formato inválido (texto)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_n_lab_formato_invalido(client_autenticado, laudo):
    response = client_autenticado.post(
        f"/api/laudos/{laudo.id}/analises/",
        {"n_lab": "2026/abc"},
        format="json",
    )

    assert response.status_code == 400
    assert "n_lab" in response.data


# ---------------------------------------------------------------------------
# 4.7 — n_lab com espaço → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_n_lab_com_espaco(client_autenticado, laudo):
    response = client_autenticado.post(
        f"/api/laudos/{laudo.id}/analises/",
        {"n_lab": "2026/ 01"},
        format="json",
    )

    assert response.status_code == 400
    assert "n_lab" in response.data


# ---------------------------------------------------------------------------
# 4.8 — Listar análises de um laudo
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_listar_analises(client_autenticado, laudo, analise):
    response = client_autenticado.get(f"/api/laudos/{laudo.id}/analises/")

    assert response.status_code == 200
    n_labs = [a["n_lab"] for a in response.data]
    assert "2026/001" in n_labs


# ---------------------------------------------------------------------------
# 4.9 — Criar laudo sem autenticação → 401
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_laudo_sem_autenticacao(client_anonimo, cliente):
    response = client_anonimo.post("/api/laudos/", {
        "cliente_codigo": "C-001",
        "data_emissao": "2026-08-05",
    }, format="json")

    assert response.status_code == 401
