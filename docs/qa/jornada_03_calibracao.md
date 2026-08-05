# QA — Jornada 3: Calibração de Equipamentos

**Arquivo de teste:** `backend/test/integration/test_calibracao.py`
**Executar:** `cd backend && .venv/bin/python3.11 -m pytest test/integration/test_calibracao.py -v`
**Status:** ✅ 12/12 passando

---

## Objetivo

Validar criação de baterias com regras de campos por equipamento, cálculo automático da curva via signal após adição/remoção de pontos, e unicidade da bateria ativa por elemento.

---

## Casos de Teste

### 3.1 — Criar bateria AA/Ca com volumes e branco

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/baterias/` |
| Entrada | `equipamento=AA`, `elemento=Ca`, `volume_solo`, `volume_extrator`, `leitura_branco` |
| Esperado | `201` + `coeficiente_angular_a=null` (sem pontos ainda) |
| Função | `test_criar_bateria_aa_ca` |
| Status | ✅ Passa |

---

### 3.2 — Criar bateria PH/ph_agua sem volumes

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/baterias/` |
| Entrada | `equipamento=PH`, `elemento=ph_agua` — sem volumes |
| Esperado | `201` (PH não está na lista de equipamentos que exigem volumes) |
| Função | `test_criar_bateria_ph` |
| Status | ✅ Passa |

---

### 3.3 — Criar bateria ES/MO sem volumes

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/baterias/` |
| Entrada | `equipamento=ES`, `elemento=MO` — sem volumes |
| Esperado | `201` (MO usa fórmula fixa, volumes não são usados no cálculo) |
| Função | `test_criar_bateria_es_mo_sem_volumes` |
| Status | ✅ Passa |

> **Correção aplicada (A-07b):** o `clean()` do model foi atualizado para excluir `MO` da exigência de volumes, espelhando o que o signal já fazia. A condição passou de `self.equipamento in ["AA", "FC", "ES"]` para `self.equipamento in ["AA", "FC", "ES"] and self.elemento != "MO"`.

---

### 3.4 — AA sem `leitura_branco` → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/baterias/` |
| Entrada | `equipamento=AA` sem `leitura_branco` |
| Esperado | `400` com erro em `leitura_branco` |
| Função | `test_criar_bateria_aa_sem_branco` |
| Status | ✅ Passa |

---

### 3.5 — ES sem `volume_solo` → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/baterias/` |
| Entrada | `equipamento=ES` sem `volume_solo` |
| Esperado | `400` com erro em `volume_solo` |
| Função | `test_criar_bateria_es_sem_volume_solo` |
| Status | ✅ Passa |

---

### 3.6 — 1 ponto não gera curva

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/baterias/{id}/pontos/` |
| Entrada | 1 par `(concentracao, absorvancia)` |
| Esperado | `201` + `coeficiente_angular_a=null` na bateria |
| Função | `test_um_ponto_nao_gera_curva` |
| Status | ✅ Passa |

---

### 3.7 — 2º ponto gera curva automaticamente via signal

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/baterias/{id}/pontos/` (2ª chamada) |
| Entrada | 2º par `(concentracao, absorvancia)` |
| Esperado | `coeficiente_angular_a`, `coeficiente_linear_b` e `r_quadrado` preenchidos |
| Função | `test_segundo_ponto_gera_curva` |
| Status | ✅ Passa |

---

### 3.8 — Ativar bateria B desativa bateria A do mesmo elemento

| Campo | Valor |
|---|---|
| Endpoint | `PATCH /api/baterias/{id}/` |
| Entrada | `{ "ativo": true }` em bateria B, com bateria A já ativa |
| Esperado | `200` + bateria A passa para `ativo=False` automaticamente |
| Função | `test_ativar_bateria_desativa_outra_do_mesmo_elemento` |
| Status | ✅ Passa |

---

### 3.9 — Remover ponto reseta a curva

| Campo | Valor |
|---|---|
| Endpoint | `DELETE /api/pontos/{id}/` |
| Entrada | Remoção de pontos até restar apenas 1 |
| Esperado | `coeficiente_angular_a=null` após a remoção |
| Função | `test_remover_ponto_reseta_curva` |
| Status | ✅ Passa |

---

### 3.10 — Criar bateria sem autenticação → 401

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/baterias/` |
| Entrada | Payload válido, sem token |
| Esperado | `401` |
| Função | `test_criar_bateria_sem_autenticacao` |
| Status | ✅ Passa |

---

### 3.11 — Ativar bateria já ativa é idempotente

| Campo | Valor |
|---|---|
| Endpoint | `PATCH /api/baterias/{id}/` |
| Entrada | `{ "ativo": true }` em bateria que já está ativa |
| Esperado | `200` + estado permanece `ativo=True` sem efeito colateral |
| Função | `test_ativar_bateria_ja_ativa_e_idempotente` |
| Status | ✅ Passa |

---

## Correções Aplicadas

| # | Descrição | Arquivo |
|---|---|---|
| A-07b | `clean()` do model atualizado para excluir `MO` da exigência de volumes, alinhando com o signal gatekeeper. | `models.py` |

---

## Cobertura dos Riscos

| Risco | Coberto? |
|---|---|
| Bateria criada sem campos obrigatórios por equipamento | ✅ Casos 3.4 e 3.5 |
| Curva calculada com apenas 1 ponto | ✅ Caso 3.6 |
| Signal de curva dispara corretamente no 2º ponto | ✅ Caso 3.7 |
| Signal de unicidade da bateria ativa | ✅ Caso 3.8 |
| Signal de reset de curva no delete de ponto | ✅ Caso 3.9 |
| Acesso sem autenticação | ✅ Caso 3.10 |
| Idempotência do toggle ativo | ✅ Caso 3.11 |
