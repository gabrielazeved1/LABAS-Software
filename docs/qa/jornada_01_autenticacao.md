# QA — Jornada 1: Autenticação

**Arquivo de teste:** `backend/test/integration/test_autenticacao.py`
**Executar:** `cd backend && .venv/bin/python3.11 -m pytest test/integration/test_autenticacao.py -v`
**Status:** ✅ 9/9 passando

---

## Objetivo

Garantir que nenhum técnico consegue operar o sistema sem se autenticar, que tokens inválidos são rejeitados e que o endpoint `/api/register/` não é mais publicamente acessível (regressão do bug crítico C-01).

---

## Casos de Teste

### 1.1 — Login com credenciais válidas

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/token/` |
| Entrada | `username` e `password` corretos |
| Esperado | `200` + corpo com `access` e `refresh` |
| Função | `test_login_credenciais_validas` |
| Status | ✅ Passa |

---

### 1.2 — Login com senha errada

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/token/` |
| Entrada | `username` correto, `password` errado |
| Esperado | `401` |
| Função | `test_login_senha_errada` |
| Status | ✅ Passa |

---

### 1.3 — Login com usuário inexistente

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/token/` |
| Entrada | `username` que não existe no banco |
| Esperado | `401` |
| Função | `test_login_usuario_inexistente` |
| Status | ✅ Passa |

---

### 1.4 — Acesso a endpoint protegido sem token

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/clientes/` |
| Entrada | Sem header `Authorization` |
| Esperado | `401` |
| Função | `test_endpoint_protegido_sem_token` |
| Status | ✅ Passa |

---

### 1.5 — Token adulterado é rejeitado

| Campo | Valor |
|---|---|
| Endpoint | `GET /api/clientes/` |
| Entrada | `Authorization: Bearer tokeninvalido.adulterado.aqui` |
| Esperado | `401` |
| Função | `test_token_adulterado` |
| Status | ✅ Passa |

---

### 1.6 — Refresh do access token

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/token/refresh/` |
| Entrada | `refresh` token obtido em um login real |
| Esperado | `200` + novo `access` token no corpo |
| Função | `test_refresh_token` |
| Status | ✅ Passa |

---

### 1.7 — Regressão C-01: `/api/register/` não é mais público

**Contexto:** antes da correção, `POST /api/register/` tinha `permission_classes = [AllowAny]`, permitindo que qualquer pessoa criasse usuários com `is_staff=True`. A correção alterou para `[IsAuthenticated, IsStaff]`.

#### 1.7a — Sem autenticação → 401 e nenhum usuário criado

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/register/` |
| Entrada | Payload completo, sem token |
| Esperado | `401` + `User.objects.filter(username="invasor").exists() == False` |
| Função | `test_register_sem_autenticacao_retorna_401` |
| Status | ✅ Passa |

#### 1.7b — Usuário autenticado sem `is_staff` → 403

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/register/` |
| Entrada | Token válido de usuário com `is_staff=False` |
| Esperado | `403` + nenhum usuário criado |
| Função | `test_register_usuario_nao_staff_retorna_403` |
| Status | ✅ Passa |

#### 1.7c — Staff registra novo técnico com sucesso

| Campo | Valor |
|---|---|
| Endpoint | `POST /api/register/` |
| Entrada | Token de staff + payload com `username`, `email`, `nome`, `password` |
| Esperado | `201` + usuário criado com `is_staff=True` |
| Função | `test_register_staff_cria_tecnico_com_sucesso` |
| Status | ✅ Passa |

---

## Cobertura dos Riscos

| Risco | Coberto? |
|---|---|
| Acesso anônimo a dados sensíveis | ✅ Casos 1.4 e 1.5 |
| Token forjado aceito | ✅ Caso 1.5 |
| Criação pública de usuários staff (C-01) | ✅ Casos 1.7a e 1.7b |
| Fluxo completo de sessão (login → refresh) | ✅ Casos 1.1 e 1.6 |
