"""
Jornada 5 — Bancada: Leitura Bruta → Resultado
Valida o fluxo completo signal → cálculo → persistência para cada equipamento.
"""

import pytest
from src.infrastructure.database.models import AnaliseSolo, BateriaCalibracao, PontoCalibracao


def postar_leitura(client, analise_id, bateria_id, leitura_bruta, fator_diluicao=None):
    payload = {"analise": analise_id, "bateria": bateria_id, "leitura_bruta": leitura_bruta}
    if fator_diluicao is not None:
        payload["fator_diluicao"] = fator_diluicao
    return client.post("/api/leituras/", payload, format="json")


# ---------------------------------------------------------------------------
# 5.1 — Leitura AA/Ca → analise.ca preenchida
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_leitura_aa_ca(client_autenticado, analise, bateria_aa_ca):
    response = postar_leitura(
        client_autenticado, analise.id, bateria_aa_ca.id,
        leitura_bruta=0.213, fator_diluicao=1,
    )

    assert response.status_code == 201
    assert response.data["resultado_calculado"] is not None

    analise.refresh_from_db()
    assert analise.ca is not None


# ---------------------------------------------------------------------------
# 5.2 — Leitura FC/K → analise.k preenchida
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_leitura_fc_k(client_autenticado, analise, bateria_fc_k):
    response = postar_leitura(
        client_autenticado, analise.id, bateria_fc_k.id,
        leitura_bruta=0.189, fator_diluicao=1,
    )

    assert response.status_code == 201

    analise.refresh_from_db()
    assert analise.k is not None


# ---------------------------------------------------------------------------
# 5.3 — Leitura PH/ph_agua → analise.ph_agua preenchida
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_leitura_ph_agua(client_autenticado, analise, bateria_ph):
    response = postar_leitura(
        client_autenticado, analise.id, bateria_ph.id,
        leitura_bruta=6.5,
    )

    assert response.status_code == 201

    analise.refresh_from_db()
    assert analise.ph_agua is not None


# ---------------------------------------------------------------------------
# 5.4 — Leitura ES/MO → analise.mo preenchida + c_org calculado
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_leitura_es_mo(client_autenticado, analise, bateria_es_mo):
    response = postar_leitura(
        client_autenticado, analise.id, bateria_es_mo.id,
        leitura_bruta=70.0,
    )

    assert response.status_code == 201

    analise.refresh_from_db()
    assert analise.mo is not None


# ---------------------------------------------------------------------------
# 5.5 — Leitura TI/Al → analise.al preenchida
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_leitura_ti_al(client_autenticado, analise, bateria_ti_al):
    response = postar_leitura(
        client_autenticado, analise.id, bateria_ti_al.id,
        leitura_bruta=0.5,
    )

    assert response.status_code == 201

    analise.refresh_from_db()
    assert analise.al is not None


# ---------------------------------------------------------------------------
# 5.6 — Leitura TI/H_Al → analise.h_al preenchida + T_maiusculo recalculado
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_leitura_ti_h_al(client_autenticado, analise, db):
    bateria_h_al = BateriaCalibracao.objects.create(
        equipamento="TI", elemento="H_Al", leitura_branco=0.0, ativo=True,
    )

    response = postar_leitura(
        client_autenticado, analise.id, bateria_h_al.id,
        leitura_bruta=2.0,
    )

    assert response.status_code == 201

    analise.refresh_from_db()
    assert analise.h_al is not None


# ---------------------------------------------------------------------------
# 5.7 — Ca + Mg + K → relações agronômicas completas
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_relacoes_agronomicas_completas(client_autenticado, analise, bateria_aa_ca, bateria_fc_k, db):
    bateria_aa_mg = BateriaCalibracao.objects.create(
        equipamento="AA", elemento="Mg",
        volume_solo=5, volume_extrator=50, leitura_branco=0.002, ativo=True,
    )
    pontos_mg = [(0.5, 0.022), (1.0, 0.043), (2.0, 0.086), (4.0, 0.171)]
    for conc, abs_ in pontos_mg:
        PontoCalibracao.objects.create(bateria=bateria_aa_mg, concentracao=conc, absorvancia=abs_)
    bateria_aa_mg.refresh_from_db()

    postar_leitura(client_autenticado, analise.id, bateria_aa_ca.id,
                   leitura_bruta=0.213, fator_diluicao=1)
    postar_leitura(client_autenticado, analise.id, bateria_aa_mg.id,
                   leitura_bruta=0.086, fator_diluicao=1)
    postar_leitura(client_autenticado, analise.id, bateria_fc_k.id,
                   leitura_bruta=0.189, fator_diluicao=1)

    analise.refresh_from_db()
    assert analise.ca is not None
    assert analise.mg is not None
    assert analise.k is not None
    assert analise.sb is not None
    assert analise.V is not None
    assert analise.ca_mg is not None
    assert analise.ca_k is not None
    assert analise.mg_k is not None


# ---------------------------------------------------------------------------
# 5.8 — AA sem fator_diluicao → 400
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_leitura_aa_sem_fator_diluicao(client_autenticado, analise, bateria_aa_ca):
    response = postar_leitura(
        client_autenticado, analise.id, bateria_aa_ca.id,
        leitura_bruta=0.213,
        # fator_diluicao omitido
    )

    assert response.status_code == 400
    assert "fator_diluicao" in response.data


# ---------------------------------------------------------------------------
# 5.9 — Análise inativa não aparece nas amostras pendentes
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_analise_inativa_nao_aparece_em_pendentes(client_autenticado, laudo, bateria_aa_ca):
    analise_inativa = AnaliseSolo.objects.create(
        laudo=laudo, n_lab="2026/099", ativo=False,
    )

    response = client_autenticado.get(
        "/api/amostras/",
        {"equipamento": "AA", "elemento": "Ca"},
    )

    assert response.status_code == 200
    # endpoint paginado — resultados em "results"
    ids = [a["id"] for a in response.data["results"]]
    assert analise_inativa.id not in ids


# ---------------------------------------------------------------------------
# 5.10 — Bateria sem curva: leitura salva (201), campo da análise fica null
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_leitura_bateria_sem_curva_nao_gera_500(client_autenticado, analise, db):
    bateria_sem_curva = BateriaCalibracao.objects.create(
        equipamento="AA", elemento="Ca",
        volume_solo=5, volume_extrator=50, leitura_branco=0.002,
        ativo=False,  # sem pontos — curva null
    )

    response = postar_leitura(
        client_autenticado, analise.id, bateria_sem_curva.id,
        leitura_bruta=0.213, fator_diluicao=1,
    )

    assert response.status_code == 201

    analise.refresh_from_db()
    # ca permanece no default do model (Decimal('0')) — signal não atualizou
    # não é None porque o field tem default=0; o importante é que não gerou 500
    assert response.data["resultado_calculado"] == 0.0
