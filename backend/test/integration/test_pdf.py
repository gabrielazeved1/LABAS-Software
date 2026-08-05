"""
Jornada 7 — Gerar PDF do Laudo
Valida o endpoint de geração de PDF: autenticação, 404 para laudo inexistente
e resposta correta para laudo existente com análises ativas.
WeasyPrint é mockado para não depender de libs de sistema no CI.
"""

import pytest
from unittest.mock import patch


# ---------------------------------------------------------------------------
# 7.1 — PDF de laudo com análises ativas → 200 + application/pdf
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_gerar_pdf_laudo_existente(client_autenticado, laudo, analise):
    with patch("src.infrastructure.web.views.HTML") as mock_html:
        mock_html.return_value.write_pdf.return_value = b"%PDF-1.4 fake"

        response = client_autenticado.get(f"/api/laudos/{laudo.id}/pdf/")

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"
    assert "Content-Disposition" in response


# ---------------------------------------------------------------------------
# 7.2 — PDF inclui apenas análises ativas (ativo=True)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_pdf_usa_apenas_analises_ativas(client_autenticado, laudo, analise):
    from src.infrastructure.database.models import AnaliseSolo

    analise_inativa = AnaliseSolo.objects.create(
        laudo=laudo, n_lab="2026/099", ativo=False,
    )

    captured = {}

    def capturar_html(string, base_url):
        captured["html"] = string
        m = _FakeHTML()
        return m

    class _FakeHTML:
        def write_pdf(self):
            return b"%PDF-1.4 fake"

    with patch("src.infrastructure.web.views.HTML", side_effect=capturar_html):
        response = client_autenticado.get(f"/api/laudos/{laudo.id}/pdf/")

    assert response.status_code == 200
    # n_lab da análise inativa não deve aparecer no HTML enviado ao WeasyPrint
    assert analise_inativa.n_lab not in captured.get("html", "")


# ---------------------------------------------------------------------------
# 7.3 — PDF de laudo inexistente → 404
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_gerar_pdf_laudo_inexistente(client_autenticado):
    response = client_autenticado.get("/api/laudos/99999/pdf/")

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# 7.4 — PDF sem autenticação → 401
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_gerar_pdf_sem_autenticacao(client_anonimo, laudo):
    response = client_anonimo.get(f"/api/laudos/{laudo.id}/pdf/")

    # SessionAuthentication é o primeiro da lista — retorna 403 em vez de 401
    assert response.status_code in (401, 403)
