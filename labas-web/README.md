# LABAS Web — Frontend

> Interface do sistema de análise de solo e tecido vegetal do Laboratório UFU.  
> **Stack:** React 19 + TypeScript + Material UI v7 + Vite

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

| Ferramenta | Versão mínima | Como verificar |
| ---------- | ------------- | -------------- |
| Node.js    | 20.x          | `node -v`      |
| npm        | 10.x          | `npm -v`       |
| Git        | qualquer      | `git -v`       |

---

## Instalação e setup inicial

### 1. Clone o repositório

```bash
git clone https://github.com/gabrielazeved1/LABAS-Software.git
cd LABAS-Software/labas-web
```

### 2. Instale as dependências

```bash
npm install
```

Isso instalará automaticamente todas as dependências listadas no `package.json`:

- `react` + `react-dom` — biblioteca de UI
- `@mui/material` + `@mui/icons-material` — componentes de interface
- `@emotion/react` + `@emotion/styled` — engine de estilos do MUI
- `axios` — cliente HTTP para a API
- `react-router-dom` — roteamento

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz da pasta `labas-web/`:

```bash
cp .env.example .env
```

> Se o `.env.example` ainda não existir, crie o `.env` manualmente com o conteúdo abaixo:

```env
VITE_API_BASE_URL=http://localhost:8000/api/
```

### 4. Inicie o servidor de desenvolvimento

```bash
npm run dev
```

O app estará disponível em **http://localhost:5173**.

---

## Dependências que precisam ser instaladas manualmente

As dependências abaixo **ainda não estão no `package.json`** e serão adicionadas durante o desenvolvimento das features. Quando chegar na sprint correspondente, rode:

```bash
# Validação de formulários (Sprint 1 — LoginPage, RegisterPage, LaudoFormPage)
npm install react-hook-form zod @hookform/resolvers
```

---

## Scripts disponíveis

| Comando           | O que faz                              |
| ----------------- | -------------------------------------- |
| `npm run dev`     | Inicia o servidor local com hot-reload |
| `npm run build`   | Gera o build de produção em `dist/`    |
| `npm run preview` | Serve o build de produção localmente   |
| `npm run lint`    | Roda o ESLint em todos os arquivos     |

---

## Estrutura de pastas

```
labas-web/
└── src/
    ├── main.tsx              # Entry point
    ├── App.tsx               # Rotas da aplicação
    ├── theme/                # Configuração do MUI Theme (cores, tipografia)
    ├── types/                # Interfaces TypeScript por domínio
    ├── services/             # Chamadas HTTP (Axios) — um arquivo por recurso
    ├── hooks/                # Hooks customizados — um por domínio de negócio
    ├── contexts/             # Estado global (ex: AuthContext)
    ├── components/
    │   ├── layout/           # AppShell, AppSidebar, AppHeader
    │   └── shared/           # Componentes reutilizáveis (StatusChip, etc.)
    └── pages/
        ├── auth/             # LoginPage, RegisterPage
        ├── dashboard/        # DashboardPage
        ├── laudos/           # LaudosListPage, LaudoDetailPage, LaudoFormPage
        └── calibracao/       # CalibracaoListPage, CalibracaoFormPage
```

> Consulte o arquivo `copilot.md` para a arquitetura completa, convenções de código e guia de desenvolvimento.

---

## Fluxo de branches

```
main  ←  dev  ←  feat/gabriel/foundation
                ←  feat/sabrina/laudos
```

**Antes de começar a trabalhar todo dia:**

```bash
git checkout dev && git pull origin dev
git checkout feat/sua-branch && git merge dev
```

> Nunca faça push diretamente para `main` ou `dev`. Sempre abra um PR.

---

## Backend

O frontend consome a API Django REST Framework do backend localizado em `../backend/`.

Para rodar o backend localmente:

```bash
cd ../backend
python manage.py runserver
```

A API estará em **http://localhost:8000/api/**.

---

## Dúvidas?

Consulte o `copilot.md` na raiz desta pasta — ele é o contrato técnico completo do frontend.
