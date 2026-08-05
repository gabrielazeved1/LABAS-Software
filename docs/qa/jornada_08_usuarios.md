# QA — Jornada 8: Gestão de Técnicos (staff only)

**Arquivo de teste:** `backend/test/integration/test_usuarios.py`
**Executar:** `cd backend && .venv/bin/python3.11 -m pytest test/integration/test_usuarios.py -v`
**Status:** ✅ 9/9 passando

---

## Objetivo

Validar o ciclo CRUD de técnicos: criação com validação de senha e unicidade, listagem, remoção com proteção contra auto-exclusão, e controle de acesso por permissão `is_staff`.

---

## Casos de Teste

### 8.1 — Criar técnico com dados válidos → 201

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/tecnicos/` |
| Entrada | `username`, `email`, `nome`, `password` forte |
| Esperado | `201` + usuário criado no banco |
| Função | `test_criar_tecnico_valido` |
| Status | ✅ Passa |

---

### 8.2 — Listar técnicos → 200 + lista paginada

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/tecnicos/` |
| Esperado | `200` + `results` contendo o técnico autenticado |
| Função | `test_listar_tecnicos` |
| Status | ✅ Passa |

---

### 8.3 — Senha fraca → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/tecnicos/` |
| Entrada | `password = "123"` |
| Esperado | `400` + chave `password` no erro |
| Função | `test_criar_tecnico_senha_fraca` |
| Status | ✅ Passa |

---

### 8.4 — Username duplicado → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/tecnicos/` |
| Entrada | `username` já existente no banco |
| Esperado | `400` + chave `username` no erro |
| Função | `test_criar_tecnico_username_duplicado` |
| Status | ✅ Passa |

---

### 8.5 — E-mail duplicado → 400

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/tecnicos/` |
| Entrada | `email` já existente no banco |
| Esperado | `400` + chave `email` no erro |
| Função | `test_criar_tecnico_email_duplicado` |
| Status | ✅ Passa |

---

### 8.6 — Técnico tenta remover a si mesmo → 400

| Campo | Valor |
|---|---|
| Endpoint | `DELETE /api/tecnicos/{proprio_id}/` |
| Esperado | `400` + chave `detail` no erro |
| Função | `test_tecnico_nao_pode_remover_a_si_mesmo` |
| Status | ✅ Passa |

---

### 8.7 — Remover outro técnico → 204

| Campo | Valor |
|---|---|
| Endpoint | `DELETE /api/tecnicos/{outro_id}/` |
| Esperado | `204` + usuário removido do banco |
| Função | `test_remover_outro_tecnico` |
| Status | ✅ Passa |

---

### 8.8 — Sem autenticação → 401

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/tecnicos/` |
| Entrada | Requisição sem token |
| Esperado | `401` |
| Função | `test_gestao_tecnicos_sem_autenticacao` |
| Status | ✅ Passa |

---

### 8.9 — Usuário sem `is_staff` tenta criar técnico → 403

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/tecnicos/` |
| Entrada | Token válido, `is_staff=False` |
| Esperado | `403` |
| Função | `test_criar_tecnico_usuario_nao_staff` |
| Status | ✅ Passa |

---

## Cobertura dos Riscos

| Risco | Coberto? |
|---|---|
| Técnico criado com senha fraca | ✅ Caso 8.3 |
| Username ou e-mail duplicado aceito | ✅ Casos 8.4 e 8.5 |
| Técnico remove a si mesmo | ✅ Caso 8.6 |
| Usuário comum acessa gestão de técnicos | ✅ Casos 8.8 e 8.9 |
