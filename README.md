# LABAS — Sistema de Análise de Solo

Sistema de gestão laboratorial desenvolvido como Projeto de Extensão em parceria com o curso de Agronomia da Universidade Federal de Uberlândia (UFU). O LABAS substitui o uso de planilhas manuais por uma plataforma digital integrada, cobrindo o ciclo completo: cadastro de amostras, calibração de equipamentos, cálculo agrônomico automatizado e geração de laudos técnicos em PDF.

**Status:** Em desenvolvimento ativo

---

## Indice

- [Visao Geral da Arquitetura](#visao-geral-da-arquitetura)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Equipe](#equipe)
- [Documentacao Tecnica](#documentacao-tecnica)
- [Como Executar](#como-executar)
- [Boas Praticas Aplicadas](#boas-praticas-aplicadas)
- [Fluxo de Branches](#fluxo-de-branches)

---

## Visao Geral da Arquitetura

O sistema e composto por duas aplicacoes independentes que se comunicam via API REST:

| Camada   | Tecnologia                                             | Pasta        |
| -------- | ------------------------------------------------------ | ------------ |
| Backend  | Python 3.11 + Django 5.2 + Django REST Framework + JWT | `backend/`   |
| Frontend | React 19 + TypeScript + Material UI v7 + Vite          | `labas-web/` |

A autenticacao e feita via JWT (SimpleJWT). O frontend consome a API em `http://localhost:8000/api/`. A geracao de laudos PDF utiliza WeasyPrint com templates HTML/CSS customizados.

---

## Estrutura de Pastas

```
LABAS-Software/
  backend/                  — API Django REST Framework
    config/                 — Configuracoes globais (settings, urls, wsgi)
    src/
      application/          — Regras de negocio puras (Use Cases, calculadoras)
      infrastructure/
        database/           — Models, migrations, signals
        web/                — Serializers, Views, Permissions, URLs
    static/css/             — Estilos dos laudos PDF
    templates/laudos/       — Template HTML para WeasyPrint
    test/                   — Testes automatizados por elemento quimico
  labas-web/                — Interface React
    src/
      types/                — Interfaces TypeScript
      services/             — Clientes Axios (uma responsabilidade por arquivo)
      hooks/                — Custom Hooks (logica de estado e API)
      schemas/              — Schemas de validacao Zod
      pages/                — Paginas por modulo (auth, laudos, calibracao, etc.)
      components/           — Componentes reutilizaveis (layout, shared)
      contexts/             — Contextos globais (Auth, Snackbar)
```

---

## Equipe

| Funcao                  | Responsavel      |
| ----------------------- | ---------------- |
| Arquitetura e Backend   | Gabriel Azevedo  |
| Arquitetura e Frontend  | Gabriel Azevedo  |
| Infraestrutura e Deploy | Sabrina Ferreira |

---

## Documentacao Tecnica

A documentacao detalhada de cada camada esta nos diretórios respectivos:

- **Backend** — [`backend/README.md`](backend/README.md): stack, arquitetura Clean Architecture, rotas da API, contratos de dados, autenticacao JWT, permissoes, geracao de PDF e instrucoes de execucao local.
- **Frontend** — [`labas-web/README.md`](labas-web/README.md): pre-requisitos, instalacao, variaveis de ambiente, estrutura de componentes e guia de desenvolvimento.

A API tambem expoe documentacao interativa via OpenAPI 3 (drf-spectacular) quando o servidor Django esta em execucao:

- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- Redoc: `http://localhost:8000/api/schema/redoc/`

---

## Como Executar

### Backend

Requer Python 3.11+ e [Poetry](https://python-poetry.org/).

```bash
cd backend
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

O servidor sobe em `http://localhost:8000`.

### Frontend

Requer Node.js 20+ e npm 10+.

```bash
cd labas-web
npm install
npm run dev
```

A interface sobe em `http://localhost:5173`.

---

## Boas Praticas Aplicadas

### Backend

- **Clean Architecture simplificada:** a camada `application/` contem os Use Cases e calculadoras de equipamentos sem nenhuma dependencia do Django, garantindo testabilidade isolada.
- **Principio da Responsabilidade Unica:** cada calculadora de equipamento (`equipamentos/`) trata exclusivamente de um elemento quimico.
- **Sinais Django (`signals`):** o recalculo de indices agronomicos (SB, CTC, V%, m%) e disparado automaticamente apos cada salvamento de `AnaliseSolo`, sem acoplamento entre a view e a logica de calculo.
- **Serializadores com validacao de negocio:** o `AnaliseSoloSerializer` valida unicidade global de `n_lab` e retorna erros de campo no formato padrao DRF, compativel com o tratamento de erros do frontend.
- **Permissoes granulares:** `IsAuthenticated` para leitura; `IsAdminUser` para operacoes de escrita. Clientes (`is_staff=False`) so acessam os proprios laudos via `IsOwnerOrStaff`.
- **Sem logica de negocio em Views:** as views sao finas — delegam processamento para Use Cases e serializers.
- **Testes por elemento:** cada elemento quimico possui um script de teste dedicado em `test/`, cobrindo o calculo da curva de calibracao e o resultado final.

### Frontend

- **Sem HTTP direto em componentes:** toda comunicacao com a API passa por `services/` e e orquestrada por Custom Hooks.
- **Separacao de responsabilidades (SOLID):** `types/` para contratos, `services/` para HTTP, `hooks/` para estado e efeitos, `components/` para UI pura.
- **Validacao com Zod + React Hook Form:** todos os formularios tem schema de validacao declarativo; erros de API (400) sao mapeados para campos do formulario.
- **Feedback consistente:** loading states, Skeleton MUI durante carregamento de dados e Snackbar global para erros de API.
- **Rotas protegidas:** `PrivateRoute` (autenticacao) e `StaffRoute` (permissao de staff) encapsulam o controle de acesso sem duplicar logica.
- **Grid v2 do MUI:** uso padrao de `Grid` com `size={{ xs, sm, md }}` sem dependencias de modulos instáveis.
- **Sem `any`:** tipagem TypeScript estrita em todo o projeto.

---

## Fluxo de Branches

| Branch   | Finalidade                                        |
| -------- | ------------------------------------------------- |
| `main`   | Producao — apenas merges de `dev` via PR revisado |
| `dev`    | Integracao — base para todas as features          |
| `feat/*` | Features individuais — criadas a partir de `dev`  |

Nenhum commit vai direto para `main` ou `dev`. Todo codigo passa por Pull Request com revisao obrigatoria.
