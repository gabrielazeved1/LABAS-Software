# QA — Jornada 7: Gerar PDF do Laudo

**Arquivo de teste:** `backend/test/integration/test_pdf.py`
**Executar:** `cd backend && .venv/bin/python3.11 -m pytest test/integration/test_pdf.py -v`
**Status:** ✅ 4/4 passando

---

## Objetivo

Validar o endpoint `GET /api/laudos/{id}/pdf/`: autenticação obrigatória, 404 para laudo inexistente, resposta com `Content-Type: application/pdf` e uso exclusivo de análises ativas na geração.

WeasyPrint é mockado para não depender de libs de sistema no CI — o render do template Django é exercitado normalmente.

---

## Casos de Teste

### 7.1 — PDF de laudo existente → 200 + `application/pdf`

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/laudos/{id}/pdf/` |
| Entrada | Laudo com análise ativa (`ativo=True`) |
| Esperado | `200` + `Content-Type: application/pdf` + header `Content-Disposition` presente |
| Função | `test_gerar_pdf_laudo_existente` |
| Status | ✅ Passa |

---

### 7.2 — PDF filtra apenas análises ativas

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/laudos/{id}/pdf/` |
| Entrada | Laudo com 1 análise ativa e 1 inativa (`ativo=False`) |
| Esperado | `200` + n_lab da análise inativa ausente no HTML passado ao WeasyPrint |
| Função | `test_pdf_usa_apenas_analises_ativas` |
| Status | ✅ Passa |

---

### 7.3 — Laudo inexistente → 404

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/laudos/99999/pdf/` |
| Esperado | `404` |
| Função | `test_gerar_pdf_laudo_inexistente` |
| Status | ✅ Passa |

---

### 7.4 — Sem autenticação → 401/403

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/laudos/{id}/pdf/` |
| Entrada | Requisição sem token |
| Esperado | `401` ou `403` (`SessionAuthentication` primeiro na lista retorna 403) |
| Função | `test_gerar_pdf_sem_autenticacao` |
| Status | ✅ Passa |

> **Nota:** O endpoint usa `@authentication_classes([SessionAuthentication, JWTAuthentication])`. Como `SessionAuthentication` não emite cabeçalho `WWW-Authenticate`, o DRF retorna `403` em vez de `401` para requisições anônimas via APIClient. O assert aceita ambos.

---

## Cobertura dos Riscos

| Risco | Coberto? |
|---|---|
| PDF gerado com análises inativas incluídas | ✅ Caso 7.2 |
| Laudo inexistente gera erro 500 | ✅ Caso 7.3 (retorna 404) |
| Acesso não autenticado ao PDF | ✅ Caso 7.4 |
| WeasyPrint falha por ausência de libs de sistema no CI | ✅ Mockado em todos os casos |
