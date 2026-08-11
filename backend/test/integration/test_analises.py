"""
Jornada 6 — Revisar Análises (ativo/inativo)
Valida o toggle ativo, exclusão do fluxo de bancada e atualização manual
de campos com recálculo das relações agronômicas.
"""

import pytest
from src.infrastructure.database.models import AnaliseSolo


# ---------------------------------------------------------------------------
# 6.1 — Desativar análise (ativo=False)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_desativar_analise(client_autenticado, laudo, analise):
    response = client_autenticado.patch(
        f"/api/laudos/{laudo.id}/analises/{analise.id}/",
        {"ativo": False},
        format="json",
    )

    assert response.status_code == 200
    analise.refresh_from_db()
    assert analise.ativo is False


# ---------------------------------------------------------------------------
# 6.2 — Análise inativa não aparece na bancada
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_analise_inativa_fora_da_bancada(client_autenticado, laudo, bateria_aa_ca):
    analise_inativa = AnaliseSolo.objects.create(
        laudo=laudo, n_lab="2026/050", ativo=False,
    )

    response = client_autenticado.get(
        "/api/amostras/",
        {"equipamento": "AA", "elemento": "Ca"},
    )

    assert response.status_code == 200
    ids = [a["id"] for a in response.data["results"]]
    assert analise_inativa.id not in ids


# ---------------------------------------------------------------------------
# 6.3 — Reativar análise (ativo=True)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_reativar_analise(client_autenticado, laudo, bateria_aa_ca):
    analise_inativa = AnaliseSolo.objects.create(
        laudo=laudo, n_lab="2026/051", ativo=False,
    )

    response = client_autenticado.patch(
        f"/api/laudos/{laudo.id}/analises/{analise_inativa.id}/",
        {"ativo": True},
        format="json",
    )

    assert response.status_code == 200
    analise_inativa.refresh_from_db()
    assert analise_inativa.ativo is True

    # Confirma que voltou a aparecer na bancada
    pendentes = client_autenticado.get(
        "/api/amostras/",
        {"bateria_id": bateria_aa_ca.id},
    )
    ids = [a["id"] for a in pendentes.data["results"]]
    assert analise_inativa.id in ids


# ---------------------------------------------------------------------------
# 6.4 — Atualizar campo manual → relações agronômicas recalculadas
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_atualizar_campo_dispara_recalculo(client_autenticado, laudo, analise):
    # Seta ca, mg, k diretamente para garantir que o motor tem dados suficientes
    analise.ca = 3.5
    analise.mg = 1.2
    analise.k = 0.25
    analise.save()
    analise.refresh_from_db()
    sb_antes = analise.sb

    # Atualiza ca via API — signal pre_save deve recalcular
    response = client_autenticado.patch(
        f"/api/laudos/{laudo.id}/analises/{analise.id}/",
        {"ca": 5.0},
        format="json",
    )

    assert response.status_code == 200
    analise.refresh_from_db()
    assert analise.ca is not None
    # sb deve ter mudado pois ca entrou no cálculo
    assert analise.sb != sb_antes
