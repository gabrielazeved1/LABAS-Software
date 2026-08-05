# QA — Jornada 2: Cadastro de Clientes

**Arquivo de teste:** `backend/test/integration/test_clientes.py`
**Executar:** `cd backend && .venv/bin/python3.11 -m pytest test/integration/test_clientes.py -v`
**Status:** ✅ 12/12 passando

---

## Objetivo

Garantir o CRUD completo de clientes: unicidade do código, validação de campos obrigatórios, busca por nome/código e restrição de acesso a técnicos autenticados.

---

## Casos de Teste

### 2.1 — Criar cliente com todos os campos

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/clientes/` |
| Entrada | `codigo`, `nome`, `telefone`, `email`, `municipio`, `area`, `observacoes` |
| Esperado | `201` + objeto completo no corpo |
| Função | `test_criar_cliente_completo` |
| Status | ✅ Passa |

---

### 2.2 — Criar cliente com apenas campos obrigatórios

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/clientes/` |
| Entrada | Só `codigo` e `nome` |
| Esperado | `201` + campos opcionais como `null` |
| Função | `test_criar_cliente_minimo` |
| Status | ✅ Passa |

---

### 2.3 — Código duplicado é rejeitado

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/clientes/` |
| Entrada | `codigo` já existente no banco |
| Esperado | `400` + chave `"codigo"` no corpo do erro (mensagem gerada pelo Django a partir do `verbose_name` do campo) |
| Função | `test_criar_cliente_codigo_duplicado` |
| Status | ✅ Passa |

> **Nota de implementação:** para campos com `unique=True` no model, o DRF injeta um `UniqueValidator` automaticamente. Esse validador roda dentro de `field.run_validation()` — se ele falhar, o método `validate_codigo` do serializer nunca é chamado. O resultado é que `validate_codigo` é código morto: pode ser removido sem nenhum impacto no comportamento, tanto no create quanto no update.

---

### 2.4 — Payload sem campo `codigo`

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/clientes/` |
| Entrada | Payload sem `codigo` |
| Esperado | `400` + campo `codigo` no corpo do erro |
| Função | `test_criar_cliente_sem_codigo` |
| Status | ✅ Passa |

---

### 2.5 — Criar cliente sem autenticação

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/clientes/` |
| Entrada | Payload válido, sem token |
| Esperado | `401` |
| Função | `test_criar_cliente_sem_autenticacao` |
| Status | ✅ Passa |

---

### 2.6 — Listar clientes

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/clientes/` |
| Entrada | Token de staff |
| Esperado | `200` + `results` contendo o cliente criado |
| Função | `test_listar_clientes` |
| Status | ✅ Passa |

---

### 2.6b — Busca por nome via `?search=`

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/clientes/?search=João` |
| Entrada | Term com correspondência parcial no nome |
| Esperado | `200` + lista filtrada ao cliente correto |
| Função | `test_buscar_cliente_por_nome` |
| Status | ✅ Passa |

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/clientes/?search=inexistente_xyz` |
| Entrada | Term sem nenhuma correspondência |
| Esperado | `200` + lista vazia |
| Função | `test_buscar_cliente_sem_resultado` |
| Status | ✅ Passa |

---

### 2.7 — Buscar cliente por código (detalhe)

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/clientes/C-001/` |
| Entrada | Código válido |
| Esperado | `200` + objeto do cliente |
| Função | `test_buscar_cliente_por_codigo` |
| Status | ✅ Passa |

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/clientes/INEXISTENTE/` |
| Entrada | Código que não existe |
| Esperado | `404` |
| Função | `test_buscar_cliente_codigo_inexistente` |
| Status | ✅ Passa |

---

### 2.8 — Atualizar cliente (PATCH)

| Campo | Valor |
|---|---|
| Endpoint | `PATCH /api/clientes/C-001/` |
| Entrada | `{ "telefone": "34988880001" }` |
| Esperado | `200` + `telefone` atualizado no corpo |
| Função | `test_atualizar_cliente` |
| Status | ✅ Passa |

---

### 2.9 — Remover cliente

| Campo | Valor |
|---|---|
| Endpoint | `DELETE /api/clientes/C-001/` |
| Entrada | Código existente |
| Esperado | `204` + cliente ausente na listagem subsequente |
| Função | `test_remover_cliente` |
| Status | ✅ Passa |

---

## Cobertura dos Riscos

| Risco | Coberto? |
|---|---|
| Código de cliente duplicado | ✅ Caso 2.3 |
| Campo obrigatório ausente | ✅ Caso 2.4 |
| Acesso sem autenticação | ✅ Caso 2.5 |
| Busca retorna conjunto vazio sem erro | ✅ Caso 2.6b |
| Código inexistente retorna 404 (não 500) | ✅ Caso 2.7 |
| DELETE confirma remoção via listagem | ✅ Caso 2.9 |
