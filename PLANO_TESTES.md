# Plano de Testes de Integração — LABAS Software

> **Data:** 2026-08-04 — **Atualizado:** 2026-08-05
> **Escopo:** Testes focados na jornada do usuário — fluxo completo do sistema
> **Framework:** pytest + pytest-django + DRF APIClient
> **Banco de dados:** SQLite em memória (isolado por teste, sem interferir no banco de dev)
> **Status geral:** ✅ 68/68 passando (8 jornadas completas)

---

## 1. As mudanças da revisão alteram os resultados dos cálculos?

**Resposta direta: NÃO.** Os resultados matemáticos para baterias corretamente configuradas são idênticos antes e depois de todas as correções.

Análise item a item:

| Correção | Tipo de mudança | Impacto nos cálculos |
|---|---|---|
| C-01 Permissão no registro | Auth/permissões | Nenhum |
| C-02/C-03 SECRET_KEY, DEBUG via env | Configuração | Nenhum |
| C-04 Race condition codigo_laudo | Geração de código | Nenhum |
| C-05 Contexto do PDF por e-mail | Renderização PDF | Nenhum |
| C-06 MultipleObjectsReturned | Tratamento de erro | Nenhum |
| C-07 Signal FC com try/except | Tratamento de erro | Nenhum — se a bateria tem `a` e `b` válidos, o cálculo é idêntico. Se `coeficiente_linear_b` era `None`, antes travava com exceção; agora registra o erro e ignora. |
| C-08 Signal post_delete | Tratamento de erro | Nenhum |
| A-01 print → logger | Logging | Nenhum |
| A-02 n_lab unique | Integridade de dados | Nenhum |
| A-03 bateria read_only | Segurança | Nenhum |
| A-04 pH signal try/except | Tratamento de erro | Nenhum — leituras válidas calculam igual. Leituras inválidas (pH fora de 0-14) antes geravam HTTP 500; agora geram log de aviso. |
| A-05 ativo=True nas amostras | Filtro de exibição | Nenhum — não altera o cálculo, apenas quais amostras aparecem na bancada |
| A-06 validate_password | Validação de senha | Nenhum |
| **A-07 MO fora do gatekeeper** | **Correção de bug** | **Único com efeito:** antes, uma bateria ES/MO sem `volume_solo` ou `volume_extrator` tinha a leitura descartada silenciosamente. Agora MO calcula corretamente — o método `calcular_mo_disponivel` nunca usou volumes, então o resultado é matematicamente correto. Se sua bateria de MO já tinha volumes configurados, o resultado é IDÊNTICO. |
| A-08 list_editable admin | Interface admin | Nenhum |
| M-01 verbose_name coeficientes | Exibição no admin | Nenhum — só o label mudou, os valores `a` e `b` continuam sendo salvos e usados corretamente |
| M-02 validação pH todos campos | Validação | Nenhum — dados já salvos no banco não são revalidados |
| M-05/M-06/M-07/M-08/M-09 | Configuração/logging/validação | Nenhum |
| B-01 Unificação serializers | Refatoração | Nenhum |
| B-02 "Phagametro" → "pHmetro" | Exibição | Nenhum |

**Conclusão:** O motor matemático (`absorcao_atomica.py`, `espectrofotometro.py`, `fotometro_chama.py`, `phmetro.py`, `titulacao.py`, `use_cases.py`, `core_matematico.py`) **não foi tocado em nenhuma linha**. Os resultados que batiam antes continuam batendo.

---

## 2. Estrutura dos Testes

```
test/integration/
  conftest.py            — fixtures compartilhadas
  test_autenticacao.py   — Jornada 1: Login e controle de acesso          ✅  9 testes
  test_clientes.py       — Jornada 2: Cadastro de clientes                ✅ 12 testes
  test_calibracao.py     — Jornada 3: Calibração de equipamentos          ✅ 11 testes
  test_laudos.py         — Jornada 4: Laudos e análises                   ✅  9 testes
  test_bancada.py        — Jornada 5: Bancada — leitura bruta → resultado ✅ 10 testes
  test_analises.py       — Jornada 6: Revisar análises (ativo/inativo)    ✅  4 testes
  test_pdf.py            — Jornada 7: Geração de PDF                      ✅  4 testes
  test_usuarios.py       — Jornada 8: Gestão de técnicos (staff only)     ✅  9 testes
```

---

## 3. Jornadas e Casos de Teste

---

### Jornada 1 — Autenticação
**Arquivo:** `test_autenticacao.py`

| # | Caso | Tipo | Dados | Resposta esperada |
|---|---|---|---|---|
| 1.1 | Login com credenciais válidas | ✅ Happy path | username/password corretos | 200 + `access` e `refresh` tokens |
| 1.2 | Login com senha errada | ❌ Falha | username correto, senha errada | 401 `No active account found` |
| 1.3 | Login com usuário inexistente | ❌ Falha | username inexistente | 401 |
| 1.4 | Acesso a endpoint protegido sem token | ❌ Falha | GET /api/clientes/ sem Authorization | 401 |
| 1.5 | Acesso com token inválido (adulterado) | ❌ Falha | Header `Bearer tokeninvalido` | 401 |
| 1.6 | Refresh do access token | ✅ Happy path | `refresh` token válido | 200 + novo `access` token |
| 1.7 | Registrar usuário via `/api/register/` cria `is_staff=False` | ✅ Regressão C-01 | payload com username/password válidos | 201 + `user.is_staff == False` |

**O que valida:** Nenhum técnico consegue operar sem se autenticar. Token adulterado é rejeitado.

---

### Jornada 2 — Cadastrar Cliente
**Arquivo:** `test_clientes.py`

| # | Caso | Tipo | Dados | Resposta esperada |
|---|---|---|---|---|
| 2.1 | Criar cliente com todos os campos | ✅ Happy path | código, nome, telefone, email, município, área | 201 + objeto criado |
| 2.2 | Criar cliente com campos opcionais vazios | ✅ Happy path | só código e nome obrigatórios | 201 |
| 2.3 | Criar cliente com código duplicado | ❌ Falha | código já existente | 400 `Já existe um cliente com este codigo` |
| 2.4 | Criar cliente sem campo código | ❌ Falha | payload sem `codigo` | 400 |
| 2.5 | Criar cliente sem autenticação | ❌ Falha | sem token | 401 |
| 2.6 | Listar clientes | ✅ Happy path | GET /api/clientes/ | 200 + lista paginada |
| 2.7 | Buscar cliente por código | ✅ Happy path | GET /api/clientes/{codigo}/ | 200 + objeto |
| 2.8 | Atualizar cliente | ✅ Happy path | PATCH com novo telefone | 200 + dado atualizado |
| 2.9 | Remover cliente | ✅ Happy path | DELETE /api/clientes/{codigo}/ | 204 |

**O que valida:** Código do cliente é único. Campos obrigatórios são validados. Acesso restrito a técnicos autenticados.

---

### Jornada 3 — Calibrar Equipamento
**Arquivo:** `test_calibracao.py`

| # | Caso | Tipo | Dados | Resposta esperada |
|---|---|---|---|---|
| 3.1 | Criar bateria AA/Ca com volumes e branco | ✅ Happy path | equipamento=AA, elemento=Ca, vol_solo, vol_extrator, leitura_branco | 201 |
| 3.2 | Criar bateria PH/ph_agua (sem volumes) | ✅ Happy path | equipamento=PH, elemento=ph_agua | 201 — PH não requer volumes |
| 3.3 | Criar bateria ES/MO (sem volumes) | ✅ Happy path | equipamento=ES, elemento=MO sem volumes | 201 — `clean()` corrigido (A-07b) para excluir MO, alinhado com o signal |
| 3.4 | Criar bateria AA sem leitura_branco | ❌ Falha | AA sem branco | 400 `Leitura do Branco é OBRIGATORIA` |
| 3.5 | Criar bateria ES sem volume_solo | ❌ Falha | ES sem vol_solo | 400 |
| 3.6 | Adicionar 1 ponto à bateria | ✅ Parcial | 1 par (concentracao, absorvancia) | 201 — curva ainda NULL (precisa de mínimo 2 pontos) |
| 3.7 | Adicionar 2º ponto → curva calculada automaticamente | ✅ Happy path | 2º ponto salvo | Verificar que `coeficiente_angular_a`, `coeficiente_linear_b` e `r_quadrado` são preenchidos automaticamente |
| 3.8 | Ativar bateria → desativa outras do mesmo elemento | ✅ Happy path | PATCH ativo=True em bateria B com bateria A já ativa | Bateria A passa a ativo=False automaticamente |
| 3.9 | Remover ponto → curva resetada | ✅ Happy path | DELETE no único ponto restante | `coeficiente_angular_a` volta a NULL |
| 3.10 | Criar bateria sem autenticação | ❌ Falha | sem token | 401 |
| 3.11 | Ativar bateria já ativa (idempotência) | ✅ Happy path | PATCH ativo=True em bateria que já é ativo=True | 200 — estado permanece ativo, sem efeito colateral |

**O que valida:** Signal de calibração funciona. Unicidade da bateria ativa é garantida. Regras de campos obrigatórios por equipamento funcionam.

---

### Jornada 4 — Criar Laudo e Análises
**Arquivo:** `test_laudos.py`

| # | Caso | Tipo | Dados | Resposta esperada |
|---|---|---|---|---|
| 4.1 | Criar laudo vinculado a cliente existente | ✅ Happy path | `cliente_codigo` válido | 201 + `codigo_laudo` gerado no formato `L-AAAA/N` |
| 4.2 | Criar segundo laudo no mesmo ano | ✅ Happy path | mesmo cliente | 201 + `codigo_laudo` = `L-2026/2` (sequência incrementada) |
| 4.3 | Criar laudo com cliente inexistente | ❌ Falha | `cliente_codigo` = "INEXISTENTE" | 400 `Cliente não encontrado` |
| 4.4 | Adicionar análise ao laudo com n_lab único | ✅ Happy path | `n_lab` = "2026/001" | 201 |
| 4.5 | Adicionar análise com n_lab duplicado | ❌ Falha | mesmo `n_lab` já existente | 400 `Já existe uma amostra com N_Lab` |
| 4.6 | n_lab com formato inválido | ❌ Falha | `n_lab` = "2026/abc" | 400 `padrão do N Lab deve ser ANO/NUMERO` |
| 4.7 | n_lab com formato inválido (espaço) | ❌ Falha | `n_lab` = "2026/ 01" | 400 |
| 4.8 | Listar análises de um laudo | ✅ Happy path | GET /api/laudos/{id}/analises/ | 200 + lista de análises |
| 4.9 | Criar laudo sem autenticação | ❌ Falha | sem token | 401 |

**O que valida:** Código do laudo é gerado automaticamente e sequencial. N_Lab é único globalmente. Formato do N_Lab é validado.

---

### Jornada 5 — Bancada: Leitura Bruta → Resultado (fluxo principal)
**Arquivo:** `test_bancada.py`

Esta é a jornada mais importante. Valida que o signal processa a leitura e atualiza o campo correto na `AnaliseSolo`.

| # | Caso | Tipo | Equipamento/Elemento | O que verifica |
|---|---|---|---|---|
| 5.1 | Leitura AA/Ca | ✅ Happy path | Absorção Atômica — Cálcio | `analise.ca` preenchido com valor calculado |
| 5.2 | Leitura FC/K | ✅ Happy path | Fotômetro de Chama — Potássio | `analise.k` preenchido. Como K alimenta as relações, verificar também `analise.sb` e `analise.V` |
| 5.3 | Leitura PH/ph_agua | ✅ Happy path | pHmetro — pH em Água | `analise.ph_agua` preenchido |
| 5.4 | Leitura ES/MO | ✅ Happy path | Espectrofotômetro — Matéria Orgânica | `analise.mo` preenchido + `analise.c_org` calculado automaticamente |
| 5.5 | Leitura TI/Al | ✅ Happy path | Titulação — Alumínio | `analise.al` preenchido |
| 5.6 | Leitura TI/H_Al | ✅ Happy path | Titulação — Acidez Potencial | `analise.h_al` preenchido. Verificar `analise.T_maiusculo` (CTC pH 7) recalculado |
| 5.7 | Leitura AA/Ca + Mg + K → relações agronômicas completas | ✅ Happy path | Sequência de 3 leituras | Verificar `sb`, `t`, `T_maiusculo`, `V`, `m`, `ca_mg`, `ca_k`, `mg_k` todos preenchidos corretamente |
| 5.8 | Leitura sem fator_diluicao em equipamento que exige | ❌ Falha | AA sem fator_diluicao | 400 `Fator de Diluição é OBRIGATÓRIO` |
| 5.9 | Análise inativa não aparece na lista de amostras pendentes | ✅ Happy path | GET amostras pendentes com analise.ativo = False | 200 — lista não contém a análise inativa |
| 5.10 | Leitura com bateria sem curva calculada | ✅ Gracioso | bateria sem pontos suficientes | Leitura é salva (201), mas campo da análise permanece null — sem erro 500 |

**O que valida:** O fluxo completo signal → cálculo → persistência funciona para todos os equipamentos. Nenhuma leitura válida gera HTTP 500. Relações agronômicas são recalculadas corretamente.

---

### Jornada 6 — Revisar Análises (ativo/inativo)
**Arquivo:** `test_analises.py`

| # | Caso | Tipo | Dados | Resposta esperada |
|---|---|---|---|---|
| 6.1 | Desativar análise (ativo=False) | ✅ Happy path | PATCH `ativo=False` | 200 — análise desativada |
| 6.2 | Análise inativa não aparece na bancada | ✅ Happy path | GET amostras pendentes | Lista não contém a análise inativa |
| 6.3 | Reativar análise (ativo=True) | ✅ Happy path | PATCH `ativo=True` | 200 — análise volta a aparecer na bancada |
| 6.4 | Atualizar campo manual da análise | ✅ Happy path | PATCH `ph_agua=6.5` | 200 + relações agronômicas recalculadas se aplicável |

**O que valida:** O toggle ativo funciona corretamente. Análises inativas são excluídas do fluxo de bancada.

---

### Jornada 7 — Gerar PDF
**Arquivo:** `test_pdf.py`

| # | Caso | Tipo | Dados | Resposta esperada |
|---|---|---|---|---|
| 7.1 | Gerar PDF de laudo com análises ativas | ✅ Happy path | GET /api/laudos/{id}/pdf/ | 200 + `Content-Type: application/pdf` + header `Content-Disposition` presente |
| 7.2 | PDF inclui apenas análises com ativo=True | ✅ Happy path | Laudo com 1 análise ativa e 1 inativa | n_lab da análise inativa ausente no HTML enviado ao WeasyPrint |
| 7.3 | Gerar PDF de laudo inexistente | ❌ Falha | GET /api/laudos/99999/pdf/ | 404 |
| 7.4 | Gerar PDF sem autenticação | ❌ Falha | sem token | 401 ou 403 (SessionAuthentication primeiro na lista retorna 403) |

> **Nota de implementação:** WeasyPrint é mockado nos testes para não depender de libs de sistema no CI. O render do template Django é exercitado normalmente.

**O que valida:** Endpoint de PDF responde corretamente. Análises inativas não entram no PDF. Laudos inexistentes retornam 404. Acesso restrito.

---

### Jornada 8 — Gestão de Técnicos (staff only)
**Arquivo:** `test_usuarios.py`

| # | Caso | Tipo | Dados | Resposta esperada |
|---|---|---|---|---|
| 8.1 | Criar técnico com senha forte | ✅ Happy path | username, email, nome, password forte | 201 + usuário criado no banco |
| 8.2 | Listar técnicos | ✅ Happy path | GET /api/tecnicos/ | 200 + `results` paginado com ao menos o técnico autenticado |
| 8.3 | Criar técnico com senha fraca | ❌ Falha | password = "123" | 400 + chave `password` no erro |
| 8.4 | Criar técnico com username duplicado | ❌ Falha | username já existente | 400 + chave `username` no erro |
| 8.5 | Criar técnico com e-mail duplicado | ❌ Falha | e-mail já existente | 400 + chave `email` no erro |
| 8.6 | Técnico tentar remover a si mesmo | ❌ Falha | DELETE /api/tecnicos/{proprio_id}/ | 400 + chave `detail` no erro |
| 8.7 | Remover outro técnico | ✅ Happy path | DELETE /api/tecnicos/{outro_id}/ | 204 + usuário removido do banco |
| 8.8 | Acessar gestão de técnicos sem autenticação | ❌ Falha | sem token | 401 |
| 8.9 | Usuário autenticado sem is_staff tenta criar técnico | ❌ Falha | token válido, is_staff=False | 403 |

**O que valida:** Criação de técnicos exige senha forte. Unicidade de username e e-mail. Técnico não remove a si mesmo. Acesso restrito a staff.

---

## 4. Fixtures do conftest.py

```python
# Dados que todos os testes compartilham

tecnico          → User staff criado para autenticar
client           → APIClient autenticado com JWT do técnico
cliente          → Cliente criado no banco
laudo            → Laudo vinculado ao cliente
analise          → AnaliseSolo vinculada ao laudo
bateria_aa_ca    → BateriaCalibracao(AA, Ca) com volumes e branco, ativa, com 6 pontos e curva calculada
bateria_ph       → BateriaCalibracao(PH, ph_agua) ativa
bateria_es_mo    → BateriaCalibracao(ES, MO) ativa
bateria_ti_al    → BateriaCalibracao(TI, Al) com branco, ativa
bateria_fc_k     → BateriaCalibracao(FC, K) com volumes e equação, ativa
```

---

## 5. O que NÃO será testado aqui

| Item | Motivo |
|---|---|
| Conteúdo visual do PDF | Requer inspeção manual ou biblioteca de parsing de PDF |
| Entrega do e-mail ao servidor SMTP | Teste de infraestrutura externa — usar `django.test.utils.override_settings` com backend de console |
| Desempenho / carga | Fora do escopo para 5 usuários |
| Frontend React | Testes de frontend ficam no repositório do labas-web |

---

## 6. Como executar

```bash
cd backend
.venv/bin/python3.11 -m pytest test/integration/ -v
```

Para ver output dos signals durante os testes:
```bash
.venv/bin/python3.11 -m pytest test/integration/ -v -s
```

Para rodar apenas um arquivo:
```bash
.venv/bin/python3.11 -m pytest test/integration/test_bancada.py -v
```
