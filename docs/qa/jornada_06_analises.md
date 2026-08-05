# QA — Jornada 6: Revisar Análises (ativo/inativo)

**Arquivo de teste:** `backend/test/integration/test_analises.py`
**Executar:** `cd backend && .venv/bin/python3.11 -m pytest test/integration/test_analises.py -v`
**Status:** ✅ 4/4 passando

---

## Objetivo

Validar o ciclo de vida de uma `AnaliseSolo`: desativar, verificar invisibilidade na bancada, reativar, e confirmar que uma atualização manual de campo dispara o recálculo das relações agronômicas via signal `pre_save`.

---

## Casos de Teste

### 6.1 — Desativar análise (`ativo=False`)

| Campo | Valor |
|---|---|
| Endpoint | `PATCH /api/laudos/{laudo_id}/analises/{analise_id}/` |
| Entrada | `{"ativo": false}` |
| Esperado | `200` + `analise.ativo is False` no banco |
| Função | `test_desativar_analise` |
| Status | ✅ Passa |

---

### 6.2 — Análise inativa não aparece na bancada

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/amostras/?equipamento=AA&elemento=Ca` |
| Entrada | `AnaliseSolo` criada com `ativo=False` |
| Esperado | `200` + id da análise inativa ausente em `results` |
| Função | `test_analise_inativa_fora_da_bancada` |
| Status | ✅ Passa |

---

### 6.3 — Reativar análise (`ativo=True`)

| Campo | Valor |
|---|---|
| Endpoint | `PATCH /api/laudos/{laudo_id}/analises/{analise_id}/` |
| Entrada | `{"ativo": true}` |
| Esperado | `200` + `analise.ativo is True` + análise aparece novamente em `/api/amostras/` |
| Função | `test_reativar_analise` |
| Status | ✅ Passa |

---

### 6.4 — Atualizar campo manual → relações agronômicas recalculadas

| Campo | Valor |
|---|---|
| Endpoint | `PATCH /api/laudos/{laudo_id}/analises/{analise_id}/` |
| Entrada | `{"ca": 5.0}` (ca, mg, k pré-setados via ORM para garantir dados suficientes) |
| Esperado | `200` + `analise.sb` diferente do valor anterior ao PATCH |
| Função | `test_atualizar_campo_dispara_recalculo` |
| Status | ✅ Passa |

---

## Cobertura dos Riscos

| Risco | Coberto? |
|---|---|
| Análise desativada vaza na bancada | ✅ Casos 6.1 + 6.2 |
| Reativação não restaura visibilidade na bancada | ✅ Caso 6.3 |
| Edição manual de campo não dispara recálculo agronômico | ✅ Caso 6.4 |
