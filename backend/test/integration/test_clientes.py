"""
Jornada 2 — Cadastro de Clientes
Valida o CRUD de clientes: unicidade de código, campos obrigatórios e
restrição de acesso a técnicos autenticados.
"""

import pytest


PAYLOAD_COMPLETO = {
    "codigo": "C-TEST",
    "nome": "Fazenda Boa Vista",
    "telefone": "34999990002",
    "email": "fazenda@boavista.com",
    "municipio": "Uberlândia",
    "area": "500 ha",
    "observacoes": "Cliente prioritário",
}


# ---------------------------------------------------------------------------
# 2.1 — Criar cliente com todos os campos
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_cliente_completo(client_autenticado):
    response = client_autenticado.post("/api/clientes/", PAYLOAD_COMPLETO, format="json")

    assert response.status_code == 201
    assert response.data["codigo"] == "C-TEST"
    assert response.data["nome"] == "Fazenda Boa Vista"
    assert response.data["municipio"] == "Uberlândia"


# ---------------------------------------------------------------------------
# 2.2 — Criar cliente com apenas campos obrigatórios
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_cliente_minimo(client_autenticado):
    response = client_autenticado.post("/api/clientes/", {
        "codigo": "C-MIN",
        "nome": "Cliente Mínimo",
    }, format="json")

    assert response.status_code == 201
    assert response.data["codigo"] == "C-MIN"
    assert response.data["telefone"] is None
    assert response.data["email"] is None


# ---------------------------------------------------------------------------
# 2.3 — Código duplicado é rejeitado
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_cliente_codigo_duplicado(client_autenticado, cliente):
    response = client_autenticado.post("/api/clientes/", {
        "codigo": "C-001",  # mesmo código do fixture `cliente`
        "nome": "Outro Nome",
    }, format="json")

    assert response.status_code == 400
    # O validador unique do Django levanta antes do validate_codigo custom
    assert "codigo" in response.data


# ---------------------------------------------------------------------------
# 2.4 — Payload sem campo `codigo`
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_cliente_sem_codigo(client_autenticado):
    response = client_autenticado.post("/api/clientes/", {
        "nome": "Sem Código",
    }, format="json")

    assert response.status_code == 400
    assert "codigo" in response.data


# ---------------------------------------------------------------------------
# 2.5 — Criar cliente sem autenticação
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_cliente_sem_autenticacao(client_anonimo):
    response = client_anonimo.post("/api/clientes/", PAYLOAD_COMPLETO, format="json")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# 2.6 — Listar clientes
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_listar_clientes(client_autenticado, cliente):
    response = client_autenticado.get("/api/clientes/")

    assert response.status_code == 200
    codigos = [c["codigo"] for c in response.data["results"]]
    assert "C-001" in codigos


# ---------------------------------------------------------------------------
# 2.6b — Buscar cliente por nome via ?search=
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_buscar_cliente_por_nome(client_autenticado, cliente):
    response = client_autenticado.get("/api/clientes/?search=João")

    assert response.status_code == 200
    assert response.data["results"][0]["codigo"] == "C-001"


@pytest.mark.django_db
def test_buscar_cliente_sem_resultado(client_autenticado, cliente):
    response = client_autenticado.get("/api/clientes/?search=inexistente_xyz")

    assert response.status_code == 200
    assert len(response.data["results"]) == 0


# ---------------------------------------------------------------------------
# 2.7 — Buscar cliente por código (detalhe)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_buscar_cliente_por_codigo(client_autenticado, cliente):
    response = client_autenticado.get("/api/clientes/C-001/")

    assert response.status_code == 200
    assert response.data["nome"] == "João da Silva"


@pytest.mark.django_db
def test_buscar_cliente_codigo_inexistente(client_autenticado):
    response = client_autenticado.get("/api/clientes/INEXISTENTE/")

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# 2.8 — Atualizar cliente (PATCH)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_atualizar_cliente(client_autenticado, cliente):
    response = client_autenticado.patch("/api/clientes/C-001/", {
        "telefone": "34988880001",
    }, format="json")

    assert response.status_code == 200
    assert response.data["telefone"] == "34988880001"


# ---------------------------------------------------------------------------
# 2.9 — Remover cliente
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_remover_cliente(client_autenticado, cliente):
    response = client_autenticado.delete("/api/clientes/C-001/")

    assert response.status_code == 204

    # Confirma que sumiu da listagem
    listagem = client_autenticado.get("/api/clientes/")
    codigos = [c["codigo"] for c in listagem.data["results"]]
    assert "C-001" not in codigos
