# QA — Jornada 4: Laudos e Análises

**Arquivo de teste:** `backend/test/integration/test_laudos.py`
**Executar:** `cd backend && .venv/bin/python3.11 -m pytest test/integration/test_laudos.py -v`
**Status:** ✅ 9/9 passando

---

## Objetivo

Validar criação de laudos com geração automática de código sequencial, vínculo com cliente, validação de `n_lab` (formato e unicidade global) e controle de acesso.

---

## Casos de Teste

### 4.1 — Criar laudo vinculado a cliente existente

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/laudos/` |
| Entrada | `cliente_codigo` válido + `data_emissao` |
| Esperado | `201` + `codigo_laudo` no formato `L-2026/N` |
| Função | `test_criar_laudo` |
| Status | ✅ Passa |

---

### 4.2 — Segundo laudo no mesmo ano incrementa o sequencial

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/laudos/` (2ª chamada) |
| Entrada | Mesmo cliente |
| Esperado | `codigo_laudo` com número maior que o primeiro |
| Função | `test_segundo_laudo_incrementa_sequencial` |
| Status | ✅ Passa |

---

### 4.3 — Cliente inexistente → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/laudos/` |
| Entrada | `cliente_codigo` que não existe no banco |
| Esperado | `400` + chave `cliente_codigo` no erro |
| Função | `test_criar_laudo_cliente_inexistente` |
| Status | ✅ Passa |

---

### 4.4 — Adicionar análise com n_lab válido

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/laudos/{id}/analises/` |
| Entrada | `n_lab=2026/001` |
| Esperado | `201` + `laudo_id` correto no corpo |
| Função | `test_adicionar_analise` |
| Status | ✅ Passa |

---

### 4.5 — n_lab duplicado → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/laudos/{id}/analises/` |
| Entrada | `n_lab` já existente no sistema |
| Esperado | `400` + chave `n_lab` no erro |
| Função | `test_n_lab_duplicado` |
| Status | ✅ Passa |

> **Nota:** a unicidade de `n_lab` é global — não é por laudo. Duas análises em laudos diferentes não podem ter o mesmo `n_lab`. A validação é feita pelo `validate_n_lab` do serializer (não pelo `UniqueValidator` automático, pois a constraint é `unique=True` no model mas o serializer sobrescreve com mensagem customizada).

---

### 4.6 — n_lab com formato inválido → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/laudos/{id}/analises/` |
| Entrada | `n_lab=2026/abc` |
| Esperado | `400` + chave `n_lab` no erro |
| Função | `test_n_lab_formato_invalido` |
| Status | ✅ Passa |

---

### 4.7 — n_lab com espaço → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/laudos/{id}/analises/` |
| Entrada | `n_lab=2026/ 01` |
| Esperado | `400` + chave `n_lab` no erro |
| Função | `test_n_lab_com_espaco` |
| Status | ✅ Passa |

---

### 4.8 — Listar análises de um laudo

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/laudos/{id}/analises/` |
| Entrada | Token de staff |
| Esperado | `200` + lista contendo a análise criada |
| Função | `test_listar_analises` |
| Status | ✅ Passa |

---

### 4.9 — Criar laudo sem autenticação → 401

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/laudos/` |
| Entrada | Payload válido, sem token |
| Esperado | `401` |
| Função | `test_criar_laudo_sem_autenticacao` |
| Status | ✅ Passa |

---

## Cobertura dos Riscos

| Risco | Coberto? |
|---|---|
| Código do laudo gerado incorretamente | ✅ Casos 4.1 e 4.2 |
| Sequencial não incrementa no mesmo ano | ✅ Caso 4.2 |
| Cliente inexistente aceito | ✅ Caso 4.3 |
| n_lab duplicado aceito globalmente | ✅ Caso 4.5 |
| Formato inválido de n_lab aceito | ✅ Casos 4.6 e 4.7 |
| Acesso sem autenticação | ✅ Caso 4.9 |
