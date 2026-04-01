# LABAS — Backend

API do Laboratório de Análise de Solo (LABAS), desenvolvida como Projeto de Extensão em parceria com o curso de Agronomia da Universidade Federal de Uberlândia (UFU).

O sistema moderniza as operações laboratoriais de análise de solo, substituindo planilhas manuais por uma infraestrutura automatizada de cadastro de amostras, cálculo agrônomico e geração de laudos técnicos em PDF.

---

## Indice

- [Stack e Arquitetura](#stack-e-arquitetura)
- [Como Executar Localmente](#como-executar-localmente)
- [Documentacao da API](#documentacao-da-api)
- [Autenticacao](#autenticacao)
- [Mapa de Rotas](#mapa-de-rotas)
- [Contratos de Dados](#contratos-de-dados)
- [Regras de Permissao](#regras-de-permissao)
- [Geracao de PDF](#geracao-de-pdf)
- [Motor de Calculos Automaticos](#motor-de-calculos-automaticos)
- [Executar Testes](#executar-testes)

---

## Stack e Arquitetura

| Camada                 | Tecnologia                                       |
| ---------------------- | ------------------------------------------------ |
| Linguagem              | Python 3.11                                      |
| Framework Web          | Django 5.2 + Django Rest Framework               |
| Autenticacao           | JWT (SimpleJWT) + Session                        |
| Documentacao           | drf-spectacular (OpenAPI 3)                      |
| Geracao de PDF         | WeasyPrint                                       |
| Banco de Dados         | SQLite (desenvolvimento) / PostgreSQL (producao) |
| Gerenciador de Pacotes | Poetry                                           |

A arquitetura segue o padrao **Clean Architecture** simplificado:

```
config/              — Configuracoes globais do Django
src/
  application/       — Regras de negocio puras (Use Cases, calculadoras de equipamentos)
  infrastructure/
    database/        — Models, migrations, signals (efeitos colaterais)
    web/             — Serializers, views, permissions, URLs (camada HTTP)
static/              — CSS para os laudos PDF
templates/           — Templates HTML para o WeasyPrint
test/                — Testes automatizados por elemento quimico
```

Os Use Cases e as calculadoras de equipamentos **nao importam nada do Django**, garantindo que a logica de negocio seja completamente testavel de forma isolada.

---

## Como Executar Localmente

**Pre-requisitos:** Python 3.11+ e Poetry instalados.

```bash
# 1. Instalar dependencias
poetry install

# 2. Aplicar migrations
poetry run python manage.py migrate

# 3. Criar superusuario (tecnico/admin)
poetry run python manage.py createsuperuser

# 4. Iniciar o servidor
poetry run python manage.py runserver
```

Com o servidor rodando, os seguintes enderecos estarao disponiveis:

| Interface                  | URL                               |
| -------------------------- | --------------------------------- |
| API (raiz)                 | http://localhost:8000/api/        |
| Swagger UI (interativo)    | http://localhost:8000/api/docs/   |
| ReDoc (referencia)         | http://localhost:8000/api/redoc/  |
| Schema OpenAPI (JSON/YAML) | http://localhost:8000/api/schema/ |
| Painel Admin               | http://localhost:8000/admin/      |

---

## Documentacao da API

A documentacao completa e interativa de todos os endpoints, incluindo exemplos de requisicao e resposta, esta disponivel em:

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/

A Swagger UI permite autenticar com o token JWT diretamente na interface e testar todos os endpoints sem precisar de Postman ou Insomnia.

---

## Autenticacao

O sistema utiliza autenticacao por **JWT (Bearer Token)** para o frontend/mobile e **Session** para acesso via navegador.

### Fluxo de autenticacao para o frontend

**1. Obter token:**

```
POST /api/token/
Content-Type: application/json

{
  "username": "nome_de_usuario",
  "password": "senha"
}
```

Resposta:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**2. Usar o token nas requisicoes:**

```
Authorization: Bearer <access_token>
```

**3. Renovar o token (antes de expirar em 60 minutos):**

```
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

O `refresh_token` expira em **1 dia**.

---

## Mapa de Rotas

| Metodo      | Endpoint                        | Autenticacao  | Permissao     | Descricao                           |
| ----------- | ------------------------------- | ------------- | ------------- | ----------------------------------- |
| POST        | `/api/register/`                | Nenhuma       | Publica       | Cadastro de novo produtor rural     |
| POST        | `/api/token/`                   | Nenhuma       | Publica       | Obter access + refresh token        |
| POST        | `/api/token/refresh/`           | Nenhuma       | Publica       | Renovar access token                |
| GET         | `/api/meus-laudos/`             | JWT / Session | Autenticado   | Listar laudos (filtrado por perfil) |
| POST        | `/api/meus-laudos/`             | JWT / Session | Somente staff | Criar novo laudo                    |
| GET         | `/api/meus-laudos/<n_lab>/`     | JWT / Session | Dono ou staff | Detalhe de um laudo                 |
| PUT / PATCH | `/api/meus-laudos/<n_lab>/`     | JWT / Session | Somente staff | Editar laudo                        |
| DELETE      | `/api/meus-laudos/<n_lab>/`     | JWT / Session | Somente staff | Excluir laudo                       |
| GET         | `/api/meus-laudos/<n_lab>/pdf/` | JWT / Session | Dono ou staff | Gerar PDF do laudo                  |

**Observacao sobre o `n_lab`:** O identificador do laudo contem `/` (ex: `2026/001`). Nas URLs, utilize o valor completo: `/api/meus-laudos/2026/001/`.

---

## Contratos de Dados

### POST `/api/register/` — Cadastro de novo cliente

**Corpo da requisicao:**

```json
{
  "username": "fazenda_verde",
  "password": "senha_segura_123",
  "email": "produtor@email.com",
  "nome_cliente": "Joao da Silva",
  "codigo_cliente": "CLI-001",
  "municipio": "Uberlandia",
  "area": "Fazenda Boa Vista"
}
```

`municipio` e `area` sao opcionais.

**Resposta (201):**

```json
{
  "message": "Usuario e perfil de Cliente criados com sucesso"
}
```

---

### GET `/api/meus-laudos/` — Listagem de laudos

A resposta e paginada (10 itens por pagina).

**Resposta (200):**

```json
{
  "count": 42,
  "next": "http://localhost:8000/api/meus-laudos/?page=2",
  "previous": null,
  "results": [
    {
      "n_lab": "2026/001",
      "cliente": {
        "codigo": "CLI-001",
        "nome": "Joao da Silva",
        "municipio": "Uberlandia",
        "area": "Fazenda Boa Vista"
      },
      "data_entrada": "2026-04-01",
      "data_saida": null,
      "ph_agua": "6.5000",
      "ph_cacl2": "5.8000",
      "ph_kcl": "5.2000",
      "p_m": "12.5000",
      "p_r": "0.0000",
      "p_rem": "0.0000",
      "mo": "3.2000",
      "s": "0.0000",
      "b": "0.0000",
      "k": "180.0000",
      "na": "0.0000",
      "ca": "2.5000",
      "mg": "1.2000",
      "cu": "0.0000",
      "fe": "0.0000",
      "mn": "0.0000",
      "zn": "0.0000",
      "al": "0.0000",
      "h_al": "3.0000",
      "areia": "45.00",
      "argila": "35.00",
      "silte": "20.00",
      "sb": "4.16",
      "t": "4.16",
      "T_maiusculo": "7.16",
      "V": "58.1",
      "m": "0.0",
      "ca_mg": "2.08",
      "ca_k": "5.40",
      "mg_k": "2.59",
      "c_org": "1.86"
    }
  ]
}
```

**Campos calculados automaticamente pelo sistema (nao enviar no POST):**

`sb`, `t`, `T_maiusculo`, `V`, `m`, `ca_mg`, `ca_k`, `mg_k`, `c_org`

Esses campos sao calculados automaticamente no momento em que o laudo e salvo, a partir de `k`, `ca`, `mg`, `al`, `h_al` e `mo`.

**Campos de leitura direta (lidos dos equipamentos pelos tecnicos):**

| Campo      | Equipamento        | Unidade   | Descricao            |
| ---------- | ------------------ | --------- | -------------------- |
| `ph_agua`  | pHmetro            | —         | pH em agua           |
| `ph_cacl2` | pHmetro            | —         | pH em CaCl2          |
| `ph_kcl`   | pHmetro            | —         | pH em KCl            |
| `p_m`      | Espectrofotometro  | mg/dm3    | Fosforo Mehlich      |
| `p_r`      | Espectrofotometro  | mg/dm3    | Fosforo Resina       |
| `p_rem`    | Espectrofotometro  | mg/L      | Fosforo Remanescente |
| `mo`       | Espectrofotometro  | dag/kg    | Materia Organica     |
| `s`        | Espectrofotometro  | mg/dm3    | Enxofre              |
| `b`        | Espectrofotometro  | mg/dm3    | Boro                 |
| `k`        | Fotometro de Chama | mg/dm3    | Potassio             |
| `na`       | Fotometro de Chama | mg/dm3    | Sodio                |
| `ca`       | Absorcao Atomica   | cmolc/dm3 | Calcio               |
| `mg`       | Absorcao Atomica   | cmolc/dm3 | Magnesio             |
| `cu`       | Absorcao Atomica   | mg/dm3    | Cobre                |
| `fe`       | Absorcao Atomica   | mg/dm3    | Ferro                |
| `mn`       | Absorcao Atomica   | mg/dm3    | Manganes             |
| `zn`       | Absorcao Atomica   | mg/dm3    | Zinco                |
| `al`       | Titulacao          | cmolc/dm3 | Aluminio             |
| `h_al`     | Titulacao          | cmolc/dm3 | Acidez Potencial     |
| `areia`    | Granulometria      | %         | Fracao areia         |
| `argila`   | Granulometria      | %         | Fracao argila        |
| `silte`    | Granulometria      | %         | Fracao silte         |

Todos os campos numericos aceitam `null` e tem `default = 0`.

---

### GET `/api/meus-laudos/<n_lab>/pdf/`

Retorna o arquivo PDF do laudo diretamente no corpo da resposta.

```
Content-Type: application/pdf
Content-Disposition: inline; filename="relatorio_2026-001.pdf"
```

Para abrir no navegador ou forcar download, ajuste o cabecalho no frontend conforme necessario.

---

## Regras de Permissao

O sistema possui dois perfis distintos:

**Staff (tecnico de laboratorio):**

- `is_staff = True` no Django Admin
- Acesso total: visualiza todos os laudos, cria, edita, exclui e gera PDFs

**Cliente (produtor rural):**

- `is_staff = False`
- Visualiza somente os laudos vinculados ao seu proprio cadastro
- Nao pode criar, editar nem excluir laudos via API
- Pode acessar o PDF do proprio laudo

A matriz de permissoes completa:

| Operacao                     | Cliente          | Staff       |
| ---------------------------- | ---------------- | ----------- |
| Listar proprios laudos (GET) | Sim              | Sim (todos) |
| Ver detalhe de laudo (GET)   | Apenas o proprio | Qualquer    |
| Criar laudo (POST)           | Nao              | Sim         |
| Editar laudo (PUT/PATCH)     | Nao              | Sim         |
| Excluir laudo (DELETE)       | Nao              | Sim         |
| Gerar PDF                    | Apenas o proprio | Qualquer    |

---

## Geracao de PDF

A rota `GET /api/meus-laudos/<n_lab>/pdf/` gera o laudo oficial do laboratorio com:

- Dados completos do cliente
- Os 5 laudos mais recentes do mesmo cliente (para comparativo historico)
- Todos os parametros quimicos e fisicos da amostra
- Layout oficial do LABAS-UFU renderizado com WeasyPrint

---

## Motor de Calculos Automaticos

O backend processa os dados dos equipamentos de forma automatica via Django Signals, sem nenhuma intervencao manual do tecnico apos a insercao das leituras brutas.

**Fluxo interno:**

```
1. Tecnico insere PontoCalibracao
        Recalcula a equacao da reta (regressao linear) da BateriaCalibracao

2. Tecnico insere LeituraEquipamento (valor bruto do visor)
        Roteado para a calculadora correta:
        - Absorcao Atomica   -> Ca, Mg, Cu, Fe, Mn, Zn
        - Fotometro de Chama -> K, Na
        - Espectrofotometro  -> P_M, P_R, P_rem, S, B, MO
        - Titulacao          -> Al, H+Al
        - pHmetro            -> pH agua, pH CaCl2, pH KCl
        Resultado gravado diretamente no campo correspondente do laudo

3. Laudo e salvo (qualquer motivo)
        Recalcula automaticamente: SB, t, T (CTC pH 7), V%, m%, Ca/Mg, Ca/K, Mg/K, C-org
```

O frontend **nao precisa enviar os campos calculados**. O backend os processa e retorna na resposta.

---

## Executar Testes

Os testes cobrem os calculos de cada elemento quimico de forma isolada.

```bash
poetry run pytest
```

Os arquivos de teste estao na pasta `test/`, organizados por elemento (ex: `testar_quimica_ca.py`, `testar_phmetro.py`).

---

## Configuracoes de Ambiente

| Variavel                 | Descricao               | Padrao                   |
| ------------------------ | ----------------------- | ------------------------ |
| `SECRET_KEY`             | Chave secreta do Django | hardcoded (somente dev)  |
| `DEBUG`                  | Modo debug              | `True` (somente dev)     |
| `ALLOWED_HOSTS`          | Hosts permitidos        | `localhost`, `127.0.0.1` |
| `CORS_ALLOW_ALL_ORIGINS` | Liberar CORS            | `True` (somente dev)     |

Em producao, todas essas variaveis devem ser configuradas via arquivo `.env` usando `python-decouple`.

---
