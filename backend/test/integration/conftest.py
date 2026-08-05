import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from src.infrastructure.database.models import (
    AnaliseSolo,
    BateriaCalibracao,
    Cliente,
    Laudo,
    PontoCalibracao,
)


# ---------------------------------------------------------------------------
# Usuários
# ---------------------------------------------------------------------------

@pytest.fixture
def tecnico(db):
    return User.objects.create_user(
        username="tecnico_teste",
        password="SenhaForte@2026",
        email="tecnico@labas.ufu.br",
        first_name="Técnico",
        last_name="Teste",
        is_staff=True,
    )


@pytest.fixture
def tecnico_comum(db):
    """Usuário autenticado mas sem is_staff — usado para testes de permissão 403."""
    return User.objects.create_user(
        username="usuario_comum",
        password="SenhaForte@2026",
        email="comum@labas.ufu.br",
        is_staff=False,
    )


@pytest.fixture
def client_autenticado(tecnico):
    """APIClient já autenticado como técnico (staff)."""
    client = APIClient()
    client.force_authenticate(user=tecnico)
    return client


@pytest.fixture
def client_comum(tecnico_comum):
    """APIClient autenticado como usuário sem is_staff."""
    client = APIClient()
    client.force_authenticate(user=tecnico_comum)
    return client


@pytest.fixture
def client_anonimo():
    """APIClient sem autenticação."""
    return APIClient()


# ---------------------------------------------------------------------------
# Entidades de domínio
# ---------------------------------------------------------------------------

@pytest.fixture
def cliente(db):
    return Cliente.objects.create(
        codigo="C-001",
        nome="João da Silva",
        telefone="34999990001",
        email="joao@fazenda.com",
        municipio="Uberlândia",
    )


@pytest.fixture
def laudo(db, cliente):
    return Laudo.objects.create(cliente=cliente)


@pytest.fixture
def analise(db, laudo):
    return AnaliseSolo.objects.create(
        laudo=laudo,
        n_lab="2026/001",
        ativo=True,
    )


# ---------------------------------------------------------------------------
# Baterias de calibração (uma por equipamento)
# ---------------------------------------------------------------------------

@pytest.fixture
def bateria_aa_ca(db):
    """Bateria AA/Ca com 6 pontos e curva calculada. Ativa."""
    bateria = BateriaCalibracao.objects.create(
        equipamento="AA",
        elemento="Ca",
        volume_solo=5.0,
        volume_extrator=50.0,
        leitura_branco=0.002,
        ativo=True,
    )
    pontos = [
        (0.5, 0.028),
        (1.0, 0.055),
        (2.0, 0.107),
        (4.0, 0.213),
        (6.0, 0.318),
        (8.0, 0.423),
    ]
    for conc, abs_ in pontos:
        PontoCalibracao.objects.create(
            bateria=bateria,
            concentracao=conc,
            absorvancia=abs_,
        )
    bateria.refresh_from_db()
    return bateria


@pytest.fixture
def bateria_fc_k(db):
    """Bateria FC/K com curva calculada. Ativa."""
    bateria = BateriaCalibracao.objects.create(
        equipamento="FC",
        elemento="K",
        volume_solo=5.0,
        volume_extrator=50.0,
        leitura_branco=0.0,
        ativo=True,
    )
    pontos = [
        (1.0, 0.048),
        (2.0, 0.095),
        (4.0, 0.189),
        (6.0, 0.282),
    ]
    for conc, abs_ in pontos:
        PontoCalibracao.objects.create(
            bateria=bateria,
            concentracao=conc,
            absorvancia=abs_,
        )
    bateria.refresh_from_db()
    return bateria


@pytest.fixture
def bateria_ph(db):
    """Bateria PH/ph_agua. Ativa. PH não usa curva de regressão."""
    return BateriaCalibracao.objects.create(
        equipamento="PH",
        elemento="ph_agua",
        leitura_branco=None,
        ativo=True,
    )


@pytest.fixture
def bateria_es_mo(db):
    """Bateria ES/MO com curva calculada. Ativa."""
    bateria = BateriaCalibracao.objects.create(
        equipamento="ES",
        elemento="MO",
        leitura_branco=0.0,
        ativo=True,
    )
    pontos = [
        (1.0, 0.150),
        (2.0, 0.290),
        (4.0, 0.570),
        (6.0, 0.850),
    ]
    for conc, abs_ in pontos:
        PontoCalibracao.objects.create(
            bateria=bateria,
            concentracao=conc,
            absorvancia=abs_,
        )
    bateria.refresh_from_db()
    return bateria


@pytest.fixture
def bateria_ti_al(db):
    """Bateria TI/Al com branco. Ativa."""
    return BateriaCalibracao.objects.create(
        equipamento="TI",
        elemento="Al",
        leitura_branco=0.0,
        ativo=True,
    )
