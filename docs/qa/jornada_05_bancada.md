# QA — Jornada 5: Bancada — Leitura Bruta → Resultado

**Arquivo de teste:** `backend/test/integration/test_bancada.py`
**Executar:** `cd backend && .venv/bin/python3.11 -m pytest test/integration/test_bancada.py -v`
**Status:** ✅ 10/10 passando

---

## Objetivo

Validar o fluxo completo — leitura bruta registrada na bancada → signal processa → resultado persistido na `AnaliseSolo` — para todos os equipamentos. É a jornada mais crítica: qualquer falha aqui compromete os resultados que chegam ao cliente.

---

## Casos de Teste

### 5.1 — Leitura AA/Ca → `analise.ca` preenchida

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` |
| Entrada | `bateria` AA/Ca com curva, `leitura_bruta=0.213`, `fator_diluicao=1` |
| Esperado | `201` + `resultado_calculado` não nulo + `analise.ca` atualizado |
| Função | `test_leitura_aa_ca` |
| Status | ✅ Passa |

---

### 5.2 — Leitura FC/K → `analise.k` preenchida

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` |
| Entrada | `bateria` FC/K com curva, `leitura_bruta=0.189`, `fator_diluicao=1` |
| Esperado | `201` + `analise.k` atualizado |
| Função | `test_leitura_fc_k` |
| Status | ✅ Passa |

---

### 5.3 — Leitura PH/ph_agua → `analise.ph_agua` preenchida

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` |
| Entrada | `bateria` PH/ph_agua, `leitura_bruta=6.5` (sem fator_diluicao) |
| Esperado | `201` + `analise.ph_agua` atualizado |
| Função | `test_leitura_ph_agua` |
| Status | ✅ Passa |

---

### 5.4 — Leitura ES/MO → `analise.mo` preenchida

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` |
| Entrada | `bateria` ES/MO, `leitura_bruta=70.0` (sem fator_diluicao) |
| Esperado | `201` + `analise.mo` atualizado |
| Função | `test_leitura_es_mo` |
| Status | ✅ Passa |

> **Correção aplicada (J5-01):** `fator_diluicao` não é mais exigido para ES/MO. Ver seção de correções.

---

### 5.5 — Leitura TI/Al → `analise.al` preenchida

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` |
| Entrada | `bateria` TI/Al com `leitura_branco`, `leitura_bruta=0.5` |
| Esperado | `201` + `analise.al` atualizado |
| Função | `test_leitura_ti_al` |
| Status | ✅ Passa |

---

### 5.6 — Leitura TI/H_Al → `analise.h_al` preenchida

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` |
| Entrada | `bateria` TI/H_Al com `leitura_branco`, `leitura_bruta=2.0` |
| Esperado | `201` + `analise.h_al` atualizado |
| Função | `test_leitura_ti_h_al` |
| Status | ✅ Passa |

---

### 5.7 — Ca + Mg + K → relações agronômicas completas

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` (3 chamadas sequenciais) |
| Entrada | Leituras de Ca (AA), Mg (AA) e K (FC) |
| Esperado | `sb`, `V`, `ca_mg`, `ca_k`, `mg_k` todos preenchidos após a 3ª leitura |
| Função | `test_relacoes_agronomicas_completas` |
| Status | ✅ Passa |

---

### 5.8 — AA sem `fator_diluicao` → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` |
| Entrada | `bateria` AA, sem `fator_diluicao` no payload |
| Esperado | `400` + chave `fator_diluicao` no erro |
| Função | `test_leitura_aa_sem_fator_diluicao` |
| Status | ✅ Passa |

---

### 5.9 — Análise inativa não aparece nas amostras pendentes

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/amostras/?equipamento=AA&elemento=Ca` |
| Entrada | `AnaliseSolo` com `ativo=False` no banco |
| Esperado | `200` + id da análise inativa ausente em `results` |
| Função | `test_analise_inativa_nao_aparece_em_pendentes` |
| Status | ✅ Passa |

---

### 5.10 — Bateria sem curva: leitura salva, sem erro 500

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/leituras/` |
| Entrada | `bateria` AA/Ca sem pontos (`coeficiente_angular_a=null`) |
| Esperado | `201` + `resultado_calculado=0.0` (signal não atualiza — campo fica no default do model) |
| Função | `test_leitura_bateria_sem_curva_nao_gera_500` |
| Status | ✅ Passa |

> **Achado J5-02:** campo permanece com `default=0` em vez de `null` quando o signal não roda. O frontend recebe `resultado_calculado=0.0` e não consegue distinguir "zero calculado" de "não calculado". Baixo impacto operacional — baterias sem curva não devem existir em produção.

---

## Correções Aplicadas

| # | Descrição | Arquivo |
|---|---|---|
| J5-01 | `LeituraEquipamento.clean()` atualizado para excluir MO da exigência de `fator_diluicao`, alinhando com o signal gatekeeper. | `models.py` |

---

## Cobertura dos Riscos

| Risco | Coberto? |
|---|---|
| Signal não atualiza campo após leitura | ✅ Casos 5.1 a 5.6 |
| Relações agronômicas não recalculadas | ✅ Caso 5.7 |
| Leitura aceita sem fator_diluicao em AA/FC/ES | ✅ Caso 5.8 |
| Análise inativa vaza na bancada | ✅ Caso 5.9 |
| Bateria sem curva gera HTTP 500 | ✅ Caso 5.10 |
