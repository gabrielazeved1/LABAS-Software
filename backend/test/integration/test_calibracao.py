"""
Jornada 3 — Calibração de Equipamentos
Valida criação de baterias, obrigatoriedade de campos por equipamento
e cálculo automático da curva via signal.
"""

import pytest
from src.infrastructure.database.models import BateriaCalibracao, PontoCalibracao


# ---------------------------------------------------------------------------
# 3.1 — Criar bateria AA/Ca com volumes e branco
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_bateria_aa_ca(client_autenticado):
    response = client_autenticado.post("/api/baterias/", {
        "equipamento": "AA",
        "elemento": "Ca",
        "volume_solo": 5.0,
        "volume_extrator": 50.0,
        "leitura_branco": 0.002,
    }, format="json")

    assert response.status_code == 201
    assert response.data["equipamento"] == "AA"
    assert response.data["elemento"] == "Ca"
    assert response.data["coeficiente_angular_a"] is None  # sem pontos ainda


# ---------------------------------------------------------------------------
# 3.2 — Criar bateria PH/ph_agua (sem volumes — PH não exige)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_bateria_ph(client_autenticado):
    response = client_autenticado.post("/api/baterias/", {
        "equipamento": "PH",
        "elemento": "ph_agua",
    }, format="json")

    assert response.status_code == 201
    assert response.data["equipamento"] == "PH"


# ---------------------------------------------------------------------------
# 3.3 — ES/MO: fórmula fixa, não exige volumes
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_bateria_es_mo_sem_volumes(client_autenticado):
    """ES/MO não exige volumes — fórmula fixa, alinhado com signal e clean()."""
    response = client_autenticado.post("/api/baterias/", {
        "equipamento": "ES",
        "elemento": "MO",
        "leitura_branco": 0.0,
    }, format="json")

    assert response.status_code == 201


# ---------------------------------------------------------------------------
# 3.4 — AA sem leitura_branco → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_bateria_aa_sem_branco(client_autenticado):
    response = client_autenticado.post("/api/baterias/", {
        "equipamento": "AA",
        "elemento": "Ca",
        "volume_solo": 5.0,
        "volume_extrator": 50.0,
    }, format="json")

    assert response.status_code == 400
    assert "leitura_branco" in response.data


# ---------------------------------------------------------------------------
# 3.5 — ES sem volume_solo → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_bateria_es_sem_volume_solo(client_autenticado):
    response = client_autenticado.post("/api/baterias/", {
        "equipamento": "ES",
        "elemento": "P_M",
        "volume_extrator": 50.0,
    }, format="json")

    assert response.status_code == 400
    assert "volume_solo" in response.data


# ---------------------------------------------------------------------------
# 3.6 — 1 ponto adicionado → curva permanece NULL
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_um_ponto_nao_gera_curva(client_autenticado, bateria_aa_ca):
    bateria_aa_ca.pontos.all().delete()
    bateria_aa_ca.refresh_from_db()
    assert bateria_aa_ca.coeficiente_angular_a is None

    response = client_autenticado.post(
        f"/api/baterias/{bateria_aa_ca.id}/pontos/",
        {"concentracao": 2.0, "absorvancia": 0.105},
        format="json",
    )

    assert response.status_code == 201
    bateria_aa_ca.refresh_from_db()
    assert bateria_aa_ca.coeficiente_angular_a is None


# ---------------------------------------------------------------------------
# 3.7 — 2º ponto → curva calculada automaticamente pelo signal
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_segundo_ponto_gera_curva(client_autenticado, bateria_aa_ca):
    bateria_aa_ca.pontos.all().delete()
    bateria_aa_ca.coeficiente_angular_a = None
    bateria_aa_ca.coeficiente_linear_b = None
    bateria_aa_ca.save()

    client_autenticado.post(
        f"/api/baterias/{bateria_aa_ca.id}/pontos/",
        {"concentracao": 2.0, "absorvancia": 0.105},
        format="json",
    )
    client_autenticado.post(
        f"/api/baterias/{bateria_aa_ca.id}/pontos/",
        {"concentracao": 4.0, "absorvancia": 0.210},
        format="json",
    )

    bateria_aa_ca.refresh_from_db()
    assert bateria_aa_ca.coeficiente_angular_a is not None
    assert bateria_aa_ca.coeficiente_linear_b is not None
    assert bateria_aa_ca.r_quadrado is not None


# ---------------------------------------------------------------------------
# 3.8 — Remover ponto → curva resetada para NULL
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_remover_ponto_reseta_curva(client_autenticado, bateria_aa_ca):
    assert bateria_aa_ca.coeficiente_angular_a is not None

    pontos = list(bateria_aa_ca.pontos.all())
    for p in pontos[1:]:
        client_autenticado.delete(f"/api/pontos/{p.id}/")

    bateria_aa_ca.refresh_from_db()
    assert bateria_aa_ca.coeficiente_angular_a is None


# ---------------------------------------------------------------------------
# 3.9 — Criar bateria sem autenticação → 401
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_criar_bateria_sem_autenticacao(client_anonimo):
    response = client_anonimo.post("/api/baterias/", {
        "equipamento": "PH",
        "elemento": "ph_agua",
    }, format="json")

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# 3.10 — Múltiplas baterias do mesmo elemento coexistem normalmente
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_multiplas_baterias_mesmo_elemento(client_autenticado, db):
    """Sem o campo ativo, múltiplas baterias podem existir para o mesmo par."""
    for _ in range(3):
        response = client_autenticado.post("/api/baterias/", {
            "equipamento": "AA",
            "elemento": "Ca",
            "volume_solo": 5,
            "volume_extrator": 50,
            "leitura_branco": 0.002,
        }, format="json")
        assert response.status_code == 201

    assert BateriaCalibracao.objects.filter(equipamento="AA", elemento="Ca").count() == 3
