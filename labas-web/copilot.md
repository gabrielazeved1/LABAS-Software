# LABAS Frontend — Guia de Arquitetura

> **Tech Lead:** Gabriel Azevedo  
> **Devs:** Gabriel Azevedo & Sabrina  
> **Stack:** React 18 + TypeScript + Material UI (MUI) v6  
> **Paradigma:** SOLID aplicado a React  
> **API:** Django REST Framework + JWT (SimpleJWT)  
> **Base URL da API:** `http://localhost:8000/api/`

---

## Índice

| #   | Seção                                                                               |
| --- | ----------------------------------------------------------------------------------- |
| 0   | [Fluxo de Branches (Git)](#0-fluxo-de-branches-git)                                 |
| 1   | [Contexto do Sistema](#1-contexto-do-sistema)                                       |
| 2   | [Paleta de Cores (MUI Theme)](#2-paleta-de-cores-mui-theme)                         |
| 3   | [Arquitetura SOLID](#3-arquitetura-solid-aplicada-ao-react)                         |
| 4   | [Estrutura de Pastas](#4-estrutura-de-pastas)                                       |
| 5   | [Tipos TypeScript](#5-tipos-typescript-espelho-dos-models-django)                   |
| 6   | [Serviços de API](#6-serviços-de-api)                                               |
| 7   | [Mapa de Páginas](#7-mapa-de-páginas)                                               |
| 8   | [Roteamento e Proteção de Rotas](#8-roteamento-e-proteção-de-rotas)                 |
| 9   | [Autenticação — Fluxo Completo](#9-autenticação--fluxo-completo)                    |
| 10  | [Convenções de Código](#10-convenções-de-código)                                    |
| 11  | [Dependências Recomendadas](#11-dependências-recomendadas)                          |
| 12  | [Inicialização do Projeto](#12-inicialização-do-projeto)                            |
| 13  | [Mapeamento Backend → Frontend](#13-mapeamento-backend--frontend-referência-rápida) |
| 14  | [Checklist de Entrega por Feature](#14-checklist-de-entrega-por-feature)            |
| 15  | [Divisão de Responsabilidades](#15-divisão-de-responsabilidades)                    |
| 16  | [Estratégia de Integração com a API](#16-estratégia-de-integração-com-a-api)        |
| 17  | [Tratamento de Erros](#17-tratamento-de-erros)                                      |
| 18  | [Checklist de Entrega (Expandido)](#18-checklist-de-entrega-por-feature)            |

---

## Status das Sprints

### Sprint 0 — Fundação (`feat/gabriel/foundation`)

| Tarefa                     | Arquivo                                      | Status     |
| -------------------------- | -------------------------------------------- | ---------- |
| Estrutura de pastas `src/` | —                                            | ✅ Feito   |
| MUI Theme                  | `src/theme/index.ts`                         | ⬜ A fazer |
| Axios + interceptors JWT   | `src/services/api.ts`                        | ⬜ A fazer |
| Tipos base                 | `src/types/auth.ts` + `src/types/cliente.ts` | ⬜ A fazer |
| AuthContext                | `src/contexts/AuthContext.tsx`               | ⬜ A fazer |
| authService                | `src/services/authService.ts`                | ⬜ A fazer |

### Sprint 1 — Autenticação e Layout

| Tarefa                                                            | Arquivo                           | Status     |
| ----------------------------------------------------------------- | --------------------------------- | ---------- |
| LoginPage                                                         | `src/pages/auth/LoginPage.tsx`    | ⬜ A fazer |
| RegisterPage                                                      | `src/pages/auth/RegisterPage.tsx` | ⬜ A fazer |
| Roteamento + PrivateRoute + StaffRoute                            | `src/App.tsx`                     | ⬜ A fazer |
| AppShell + AppSidebar + AppHeader                                 | `src/components/layout/*.tsx`     | ⬜ A fazer |
| StatusChip, ConfirmDialog, LoadingOverlay, EmptyState, PageHeader | `src/components/shared/*.tsx`     | ⬜ A fazer |

---

## 0. Fluxo de Branches (Git)

```
main          ← produção / código estável e validado
  └── dev     ← integração contínua (PRs de feature entram aqui)
        ├── feat/gabriel/foundation   ← Gabriel: infraestrutura + autenticação
        └── feat/sabrina/laudos       ← Sabrina: features de negócio
```

### Regras de branch

| Branch           | Quem faz push       | Como entra na próxima                         |
| ---------------- | ------------------- | --------------------------------------------- |
| `main`           | Ninguém diretamente | PR a partir de `dev` (revisão obrigatória)    |
| `dev`            | Ninguém diretamente | PR a partir de `feat/*`                       |
| `feat/gabriel/*` | Gabriel             | PR para `dev` quando a feature estiver pronta |
| `feat/sabrina/*` | Sabrina             | PR para `dev` quando a feature estiver pronta |

### Convenção de commits

Usar **Conventional Commits** para manter o histórico limpo:

```
feat: adiciona página de login
fix: corrige validação do campo n_lab
chore: instala dependências do MUI
refactor: extrai useLaudos para hook próprio
style: ajusta espaçamento do AppHeader
test: adiciona testes do hook useAuth
```

### Saúde das branches (rotina)

```bash
# Antes de começar a trabalhar todo dia:
git checkout dev && git pull origin dev
git checkout feat/gabriel/foundation && git merge dev  # manter atualizada
```

---

## 1. Contexto do Sistema

O LABAS é um sistema do Laboratório de Análise de Solo e Tecido Vegetal — UFU (Universidade Federal de Uberlândia), desenvolvido como projeto de extensão em parceria com o curso de Agronomia.

**O que o sistema faz:**

- Cadastra amostras de solo trazidas por produtores rurais
- Registra leituras brutas dos equipamentos do laboratório (pH-metro, Espectrofotômetro, Absorção Atômica, Fotômetro de Chama, Titulação)
- Calcula automaticamente relações agronômicas (SB, CTC, V%, m%, etc.)
- Gera laudos técnicos em PDF no padrão oficial UFU

**Dois tipos de usuário:**
| Tipo | Papel | Acesso |
|---|---|---|
| `is_staff = true` | Técnico do laboratório | CRUD completo em todos os laudos + calibração de equipamentos |
| `is_staff = false` | Cliente / Produtor Rural | Leitura dos próprios laudos + download de PDF |

---

## 2. Paleta de Cores (MUI Theme)

A identidade visual é institucional/científica, baseada nas cores da UFU e do agronegócio.

```ts
// src/theme/index.ts
// src/theme/index.ts
import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "light",

    primary: {
      main: "#233b1a",       // base institucional
      light: "#476546",      // variação suave
      dark: "#1a2c14",       // versão mais escura
      contrastText: "#FFFFFF",
    },

    secondary: {
      main: "#476546",       // apoio visual (cards, elementos secundários)
      light: "#6d8262",
      dark: "#2f4430",
      contrastText: "#FFFFFF",
    },

    success: {
      main: "#2e7d32",
    },

    warning: {
      main: "#ed6c02",
    },

    error: {
      main: "#d32f2f",
    },

    info: {
      main: "#0288d1",
    },

    background: {
      default: "#F5F5F3",    // fundo neutro leve
      paper: "#FFFFFF",
    },

    text: {
      primary: "#1F1F1F",
      secondary: "#6d8262",  // muted
    },

    divider: "#a7b698",

    grey: {
      300: "#a7b698",
      500: "#6d8262",
    },
  },

  typography: {
    fontFamily: '"Inter", "Roboto", "Arial", sans-serif',

    h4: { fontWeight: 700 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },

    body1: {
      color: "#1F1F1F",
    },

    body2: {
      color: "#6d8262",
    },
  },

  shape: {
    borderRadius: 8,
  },

  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: 600,
          borderRadius: 8,
        },
      },
    },

    MuiTableHead: {
      styleOverrides: {
        root: {
          "& th": {
            backgroundColor: "#233b1a",
            color: "#FFFFFF",
            fontWeight: 700,
          },
        },
      },
    },

    MuiTableCell: {
      styleOverrides: {
        root: {
          borderColor: "#a7b698",
        },
      },
    },

    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
        },
      },
    },

    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          "& fieldset": {
            borderColor: "#a7b698",
          },
          "&:hover fieldset": {
            borderColor: "#336006",
          },
          "&.Mui-focused fieldset": {
            borderColor: "#233b1a",
          },
        },
      },
    },

    MuiAlert: {
      styleOverrides: {
        standardSuccess: {
          backgroundColor: "#2e7d32",
          color: "#fff",
        },
        standardWarning: {
          backgroundColor: "#ed6c02",
          color: "#fff",
        },
        standardError: {
          backgroundColor: "#d32f2f",
          color: "#fff",
        },
        standardInfo: {
          backgroundColor: "#0288d1",
          color: "#fff",
        },
      },
    },
  },
});

### Referência Rápida de Cores

| Token                | Hex       | Usar em                                    |
| -------------------- | --------- | ------------------------------------------ |
| `primary.main`       | `#1A5276` | Botões primários, AppBar, links ativos     |
| `primary.dark`       | `#0E2F44` | Sidebar, header                            |
| `secondary.main`     | `#2E7D32` | Status "Laudo pronto", badges OK           |
| `warning.main`       | `#F9A825` | Laudos pendentes, alertas                  |
| `error.main`         | `#C62828` | Valores fora do padrão, erros de validação |
| `background.default` | `#F4F6F8` | Fundo de páginas                           |
| `background.paper`   | `#FFFFFF` | Cards, tabelas, formulários                |

---

## 3. Arquitetura SOLID Aplicada ao React

### S — Single Responsibility (Responsabilidade Única)

> Cada arquivo faz **uma única coisa**.

- Um componente renderiza uma parte da UI — **não faz chamadas de API diretamente**
- Um hook gerencia **um único domínio** de estado/efeito
- Um service contém **apenas as chamadas HTTP** de um recurso
- Um arquivo de types contém **apenas as interfaces** de um domínio

```

❌ ERRADO: Componente que faz fetch E renderiza E valida formulário
✅ CERTO: useLaudos() faz o fetch | LaudoForm renderiza | validators/laudo.ts valida

````

### O — Open/Closed (Aberto/Fechado)

> Componentes são **abertos para extensão via props**, fechados para modificação interna.

```tsx
// ✅ Extensível via props — nunca altere o componente base para um caso específico
<StatusChip status="pendente" />
<StatusChip status="concluido" />
<StatusChip status="cancelado" />
````

### L — Liskov Substitution (Substituição de Liskov)

> Qualquer implementação de uma interface pode substituir outra **sem quebrar o sistema**.

```ts
// ✅ O serviço depende de interface, não de implementação concreta
// Permite trocar por Mock facilmente nos testes
interface ILaudoService {
  listar(): Promise<AnaliseSolo[]>;
  criar(data: AnaliseSoloPayload): Promise<AnaliseSolo>;
  buscar(nLab: string): Promise<AnaliseSolo>;
}
```

### I — Interface Segregation (Segregação de Interfaces)

> Componentes recebem **apenas as props de que precisam**. Não crie interfaces "gordas".

```ts
// ❌ ERRADO: Prop com tudo do modelo
type LaudoCardProps = { laudo: AnaliseSolo }; // passa 30+ campos

// ✅ CERTO: Só o que o card precisa exibir
type LaudoCardProps = {
  nLab: string;
  clienteNome: string;
  dataEntrada: string;
  status: "pendente" | "concluido";
};
```

### D — Dependency Inversion (Inversão de Dependência)

> Componentes e hooks dependem de **abstrações (interfaces)**, nunca de implementações concretas.

```ts
// hooks/useLaudos.ts depende de ILaudoService
// não de laudoService.ts diretamente
// Isso permite injeção de mock em testes sem alterar o hook

const useLaudos = (service: ILaudoService = laudoService) => { ... }
```

---

## 4. Estrutura de Pastas

```
front/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── src/
    ├── main.tsx                    # Entry point — aplica ThemeProvider e Router
    ├── App.tsx                     # Define as rotas protegidas e públicas
    │
    ├── theme/
    │   └── index.ts                # [S] Configuração única do MUI Theme
    │
    ├── types/                      # [I] Interfaces TypeScript por domínio
    │   ├── auth.ts                 # User, TokenPair, LoginPayload
    │   ├── cliente.ts              # Cliente (espelho do model Django)
    │   ├── analise.ts              # AnaliseSolo completo + payloads parciais
    │   └── calibracao.ts           # BateriaCalibracao, LeituraEquipamento, PontoCalibracao
    │
    ├── services/                   # [S] Chamadas HTTP — um arquivo por recurso
    │   ├── api.ts                  # Instância Axios + interceptors JWT
    │   ├── authService.ts          # login(), refreshToken()
    │   ├── laudoService.ts         # listar(), buscar(), criar(), atualizar(), remover()
    │   └── calibracaoService.ts    # baterias, leituras, pontos
    │
    ├── hooks/                      # [S] Um hook por domínio de negócio
    │   ├── useAuth.ts              # login, logout, isStaff, token
    │   ├── useLaudos.ts            # lista, paginação, filtros
    │   ├── useLaudo.ts             # laudo individual (CRUD)
    │   └── useCalibracao.ts        # baterias do dia
    │
    ├── contexts/                   # Apenas estado verdadeiramente global
    │   └── AuthContext.tsx         # Usuário autenticado + JWT
    │
    ├── components/                 # [O] Componentes reutilizáveis
    │   ├── layout/
    │   │   ├── AppShell.tsx        # Container com Sidebar + Header + outlet
    │   │   ├── AppSidebar.tsx      # Navegação lateral (diferente por role)
    │   │   └── AppHeader.tsx       # TopBar com usuário e logout
    │   └── shared/
    │       ├── StatusChip.tsx      # Chip colorido para status do laudo
    │       ├── ConfirmDialog.tsx   # Dialog genérico de confirmação
    │       ├── LoadingOverlay.tsx  # Spinner centralizado
    │       ├── EmptyState.tsx      # Tela de lista vazia
    │       └── PageHeader.tsx      # Título + breadcrumb + ação primária
    │
    └── pages/                      # [S] Uma pasta por feature/domínio
        ├── auth/
        │   ├── LoginPage.tsx       # Formulário de login JWT
        │   └── RegisterPage.tsx    # Cadastro de novo cliente
        │
        ├── dashboard/
        │   └── DashboardPage.tsx   # Resumo (só staff vê estatísticas completas)
        │
        ├── laudos/
        │   ├── LaudosListPage.tsx  # Tabela de laudos (staff = todos | cliente = próprios)
        │   ├── LaudoDetailPage.tsx # Visualização detalhada do laudo + botão PDF
        │   └── LaudoFormPage.tsx   # Criação e edição (só staff) — formulário com Stepper
        │
        └── calibracao/
            ├── CalibracaoListPage.tsx  # Baterias do dia por equipamento
            └── CalibracaoFormPage.tsx  # Criar bateria + adicionar pontos de calibração
```

---

## 5. Tipos TypeScript (Espelho dos Models Django)

```ts
// src/types/auth.ts
export interface TokenPair {
  access: string;
  refresh: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}

export interface RegisterPayload {
  username: string;
  password: string;
  email: string;
  nome_cliente: string;
  codigo_cliente: string;
  municipio?: string;
  area?: string;
}

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  is_staff: boolean;
}
```

```ts
// src/types/cliente.ts
export interface Cliente {
  codigo: string;
  nome: string;
  municipio: string;
  area: string;
}
```

```ts
// src/types/analise.ts

export interface AnaliseSolo {
  n_lab: string; // formato: "2026/001"
  cliente: Cliente;
  data_entrada: string; // ISO date
  data_saida: string | null;

  // pH-metro
  ph_agua: number | null;
  ph_cacl2: number | null;
  ph_kcl: number | null;

  // Espectrofotômetro
  p_m: number | null; // Fósforo Mehlich
  p_r: number | null; // Fósforo Resina
  p_rem: number | null; // Fósforo Remanescente
  mo: number | null; // Matéria Orgânica
  s: number | null; // Enxofre
  b: number | null; // Boro

  // Fotômetro de Chama
  k: number | null; // Potássio
  na: number | null; // Sódio

  // Absorção Atômica
  ca: number | null; // Cálcio
  mg: number | null; // Magnésio
  cu: number | null; // Cobre
  fe: number | null; // Ferro
  mn: number | null; // Manganês
  zn: number | null; // Zinco

  // Titulação
  al: number | null; // Alumínio
  h_al: number | null; // Acidez Potencial

  // Granulometria
  areia: number | null;
  argila: number | null;
  silte: number | null;

  // Calculados automaticamente pelo backend
  sb: number | null; // Soma de Bases
  t: number | null; // CTC Efetiva
  T_maiusculo: number | null; // CTC pH 7.0
  V: number | null; // Saturação por Bases %
  m: number | null; // Saturação por Alumínio %
  ca_mg: number | null;
  ca_k: number | null;
  mg_k: number | null;
  c_org: number | null;
}

// Payload para criar/editar (sem campos read-only)
export type AnaliseSoloPayload = Omit<
  AnaliseSolo,
  | "cliente"
  | "sb"
  | "t"
  | "T_maiusculo"
  | "V"
  | "m"
  | "ca_mg"
  | "ca_k"
  | "mg_k"
  | "c_org"
> & {
  cliente_codigo: string;
};
```

```ts
// src/types/calibracao.ts

export type Equipamento = "AA" | "FC" | "ES" | "TI" | "PH";
export type Elemento =
  | "Ca"
  | "Mg"
  | "Cu"
  | "Fe"
  | "Mn"
  | "Zn"
  | "K"
  | "Na"
  | "P_M"
  | "P_R"
  | "P_rem"
  | "S"
  | "B"
  | "Al"
  | "H_Al"
  | "ph_agua"
  | "ph_cacl2"
  | "ph_kcl"
  | "MO";

export interface BateriaCalibracao {
  id: number;
  equipamento: Equipamento;
  elemento: Elemento;
  volume_solo: number | null;
  volume_extrator: number | null;
  data_criacao: string;
  coeficiente_angular_a: number | null;
  coeficiente_linear_b: number | null;
  r_quadrado: number | null;
  leitura_branco: number | null;
  ativo: boolean;
  equacao_formada: string; // propriedade calculada (read-only)
}

export interface PontoCalibracao {
  id: number;
  bateria: number;
  concentracao: number;
  absorvancia: number;
}

export interface LeituraEquipamento {
  id: number;
  bateria: number;
  leitura_bruta: number;
  fator_diluicao: number | null;
}
```

---

## 6. Serviços de API

```ts
// src/services/api.ts
// Regra: Toda chamada HTTP passa por aqui — nunca use fetch/axios direto nas páginas

import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/",
  headers: { "Content-Type": "application/json" },
});

// Injeta Bearer token automaticamente
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Renova token expirado automaticamente (401)
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) {
        const { data } = await api.post("token/refresh/", { refresh });
        localStorage.setItem("access_token", data.access);
        original.headers.Authorization = `Bearer ${data.access}`;
        return api(original);
      }
    }
    return Promise.reject(error);
  },
);
```

```ts
// src/services/laudoService.ts

import { api } from "./api";
import type { AnaliseSolo, AnaliseSoloPayload } from "../types/analise";

export const laudoService = {
  listar: (page = 1) =>
    api.get<{ results: AnaliseSolo[]; count: number }>(
      `meus-laudos/?page=${page}`,
    ),

  buscar: (nLab: string) => api.get<AnaliseSolo>(`meus-laudos/${nLab}/`),

  criar: (data: AnaliseSoloPayload) =>
    api.post<AnaliseSolo>("meus-laudos/", data),

  atualizar: (nLab: string, data: Partial<AnaliseSoloPayload>) =>
    api.patch<AnaliseSolo>(`meus-laudos/${nLab}/`, data),

  remover: (nLab: string) => api.delete(`meus-laudos/${nLab}/`),

  urlPdf: (nLab: string) => `${api.defaults.baseURL}meus-laudos/${nLab}/pdf/`,
};
```

```ts
// src/services/authService.ts

import { api } from "./api";
import type { LoginPayload, TokenPair, RegisterPayload } from "../types/auth";

export const authService = {
  login: (data: LoginPayload) => api.post<TokenPair>("token/", data),

  refresh: (refresh: string) =>
    api.post<{ access: string }>("token/refresh/", { refresh }),

  register: (data: RegisterPayload) => api.post("register/", data),
};
```

---

## 7. Mapa de Páginas

### 7.1 Login — `/login`

- Formulário com `username` e `password`
- Chama `authService.login()` → guarda tokens no `localStorage`
- Redireciona para `/dashboard` após sucesso
- **Componentes MUI:** `TextField`, `Button`, `Alert`, `Paper`

### 7.2 Register — `/register`

- Formulário em 2 etapas com `MUI Stepper`:
  - **Step 1:** Credenciais (username, email, senha)
  - **Step 2:** Dados do cliente (nome, código, município, área)
- Apenas para novos clientes (produtores rurais)
- **Componentes MUI:** `Stepper`, `Step`, `StepLabel`, `TextField`

### 7.3 Dashboard — `/dashboard`

- **Staff:** Cards com contadores (total laudos, laudos do mês, aguardando conclusão) + tabela dos 5 últimos laudos
- **Cliente:** Mensagem de boas-vindas + link rápido para "Meus Laudos"
- **Componentes MUI:** `Grid`, `Card`, `CardContent`, `Typography`, `Divider`

### 7.4 Lista de Laudos — `/laudos`

- Tabela paginada (10 itens por página — espelha o `PAGE_SIZE` do backend)
- Colunas: N Lab | Solicitante | Data Entrada | Data Saída | Ações
- **Staff:** vê todos + botão "Novo Laudo"
- **Cliente:** vê apenas os próprios, sem poder criar
- Filtro por N Lab (search)
- **Componentes MUI:** `Table`, `TablePagination`, `TextField` (search), `Button`, `IconButton`

### 7.5 Detalhe do Laudo — `/laudos/:nLab`

- Exibe todos os grupos de análise em `Accordion` por equipamento:
  - **pH-metro:** ph_agua, ph_cacl2, ph_kcl
  - **Espectrofotômetro:** p_m, p_r, p_rem, mo, s, b
  - **Fotômetro de Chama:** k, na
  - **Absorção Atômica:** ca, mg, cu, fe, mn, zn
  - **Titulação:** al, h_al
  - **Granulometria:** areia, argila, silte
  - **Calculados:** sb, t, T_maiusculo, V, m, ca_mg, ca_k, mg_k, c_org
- Botão "Baixar PDF" — abre `laudoService.urlPdf(nLab)` em nova aba com token no header
- **Staff:** botões Editar e Excluir
- **Componentes MUI:** `Accordion`, `AccordionSummary`, `AccordionDetails`, `Chip`, `Button`

### 7.6 Formulário de Laudo — `/laudos/novo` e `/laudos/:nLab/editar`

> **Acesso restrito: apenas staff**

- `MUI Stepper` horizontal em 6 etapas (mapeadas nos fieldsets do admin):
  1. **Identificação:** N Lab, Cliente (search/autocomplete), datas
  2. **pH-metro:** ph_agua, ph_cacl2, ph_kcl
  3. **Espectrofotômetro + MO:** p_m, p_r, p_rem, mo, s, b
  4. **Fotômetro + A. Atômica:** k, na, ca, mg, cu, fe, mn, zn
  5. **Titulação + Granulometria:** al, h_al, areia, argila, silte
  6. **Revisão:** exibe resumo e botão "Salvar"
- Validação por step com `react-hook-form` + `zod`
- Campos numéricos usam `type="number"` com `inputProps={{ step: 0.0001 }}`
- **Componentes MUI:** `Stepper`, `TextField`, `Autocomplete`, `Button`, `Alert`

### 7.7 Calibração de Equipamentos — `/calibracao`

> **Acesso restrito: apenas staff**

- Lista das Baterias de Calibração do dia, agrupadas por equipamento
- Cada bateria exibe: elemento, equação gerada, R², status (ativa/inativa)
- Botão "Nova Bateria"
- **Componentes MUI:** `Tabs` (por equipamento), `Table`, `Chip`, `Button`

### 7.8 Formulário de Bateria — `/calibracao/nova`

> **Acesso restrito: apenas staff**

- Seleção de equipamento e elemento
- Campos condicionais (volume_solo, volume_extrator aparecem conforme equipamento)
- Tabela inline para adicionar pontos de calibração (concentração + leitura bruta)
- Exibe equação gerada e R² em tempo real após ≥ 2 pontos
- **Componentes MUI:** `Select`, `TextField`, `Table`, `Alert`

---

## 8. Roteamento e Proteção de Rotas

```tsx
// src/App.tsx

// Rotas públicas: /login, /register
// Rotas privadas (autenticado): /dashboard, /laudos, /laudos/:nLab
// Rotas staff-only: /laudos/novo, /laudos/:nLab/editar, /calibracao

// Padrão:
// <PrivateRoute> → verifica token válido
// <StaffRoute>   → verifica is_staff === true
```

```
/ ──────────────── redireciona para /dashboard (se logado) ou /login
/login ──────────── LoginPage (pública)
/register ───────── RegisterPage (pública)
/dashboard ──────── DashboardPage (privada)
/laudos ─────────── LaudosListPage (privada)
/laudos/novo ────── LaudoFormPage (staff only)
/laudos/:nLab ───── LaudoDetailPage (privada)
/laudos/:nLab/editar ── LaudoFormPage (staff only)
/calibracao ─────── CalibracaoListPage (staff only)
/calibracao/nova ── CalibracaoFormPage (staff only)
* ───────────────── 404 NotFoundPage
```

---

## 9. Autenticação — Fluxo Completo

```
1. Usuário preenche login
2. POST /api/token/ → recebe { access, refresh }
3. Guarda em localStorage: 'access_token', 'refresh_token'
4. api.ts injeta Bearer token em todas as requisições
5. Se 401 → interceptor tenta POST /api/token/refresh/
6. Se refresh falhar → limpa tokens e redireciona para /login
7. Logout → limpa localStorage e redireciona para /login
```

> **Segurança:** Nunca expor o token em URLs. Sempre usar headers `Authorization: Bearer`.  
> Para o PDF, usar `window.open(url, '_blank')` com o token injetado via Axios e receber como blob, ou gerar URL temporária autenticada.

---

## 10. Convenções de Código

### Nomenclatura

| Elemento          | Convenção             | Exemplo                  |
| ----------------- | --------------------- | ------------------------ |
| Componentes       | PascalCase            | `LaudoDetailPage.tsx`    |
| Hooks             | camelCase + `use`     | `useLaudos.ts`           |
| Services          | camelCase + `Service` | `laudoService.ts`        |
| Types/Interfaces  | PascalCase            | `AnaliseSolo`, `Cliente` |
| Constantes        | UPPER_SNAKE_CASE      | `MAX_PAGE_SIZE`          |
| Variáveis/funções | camelCase             | `fetchLaudos()`          |

### Regras de Ouro

1. **Nunca** fazer chamadas HTTP diretamente em componentes — sempre via hooks
2. **Nunca** usar `any` — tipar com os modelos em `src/types/`
3. **Nunca** duplicar lógica de permissão — usar o contexto `AuthContext`
4. **Sempre** validar formulários antes de enviar ao backend
5. **Sempre** tratar erros da API e exibir feedback via `Alert` do MUI
6. **Sempre** mostrar `LoadingOverlay` durante operações assíncronas
7. Campos calculados (`sb`, `t`, `V`, `m`, etc.) são **somente leitura** no frontend — nunca incluir em formulários de criação/edição
8. O formato do `n_lab` é sempre `AAAA/NNN` (ex: `2026/001`) — validar com regex no frontend também

### Tratamento de Erros da API

```ts
// Padrão de tratamento de erros em hooks
try {
  const { data } = await laudoService.criar(payload);
  // sucesso
} catch (err) {
  if (axios.isAxiosError(err)) {
    // err.response.data contém os erros do DRF no formato { campo: ["mensagem"] }
    setError(err.response?.data ?? "Erro desconhecido");
  }
}
```

---

## 11. Dependências Recomendadas

```json
{
  "dependencies": {
    "@mui/material": "^6.x",
    "@mui/icons-material": "^6.x",
    "@emotion/react": "^11.x",
    "@emotion/styled": "^11.x",
    "axios": "^1.x",
    "react": "^18.x",
    "react-dom": "^18.x",
    "react-router-dom": "^6.x",
    "react-hook-form": "^7.x",
    "zod": "^3.x",
    "@hookform/resolvers": "^3.x"
  },
  "devDependencies": {
    "typescript": "^5.x",
    "vite": "^5.x",
    "@vitejs/plugin-react": "^4.x",
    "vitest": "^1.x",
    "@testing-library/react": "^14.x"
  }
}
```

---

## 12. Inicialização do Projeto

```bash
# Criar frontend com Vite + React + TypeScript
npm create vite@latest front -- --template react-ts
cd front
npm install

# Instalar dependências do projeto
npm install @mui/material @mui/icons-material @emotion/react @emotion/styled
npm install axios react-router-dom react-hook-form zod @hookform/resolvers

# Instalar Inter font (typography)
# Adicionar no index.html:
# <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

---

## 13. Mapeamento Backend → Frontend (Referência Rápida)

| Backend (Django)                         | Frontend (React)                                           |
| ---------------------------------------- | ---------------------------------------------------------- |
| `Model Cliente`                          | `types/cliente.ts → Cliente`                               |
| `Model AnaliseSolo`                      | `types/analise.ts → AnaliseSolo`                           |
| `Model BateriaCalibracao`                | `types/calibracao.ts → BateriaCalibracao`                  |
| `GET /meus-laudos/`                      | `laudoService.listar()` → `useLaudos()` → `LaudosListPage` |
| `POST /meus-laudos/`                     | `laudoService.criar()` → `useLaudo()` → `LaudoFormPage`    |
| `GET /meus-laudos/:nLab/`                | `laudoService.buscar()` → `useLaudo()` → `LaudoDetailPage` |
| `PATCH /meus-laudos/:nLab/`              | `laudoService.atualizar()` → `LaudoFormPage (edição)`      |
| `DELETE /meus-laudos/:nLab/`             | `laudoService.remover()` → `LaudoDetailPage`               |
| `GET /meus-laudos/:nLab/pdf/`            | `laudoService.urlPdf()` → botão "Baixar PDF"               |
| `is_staff = true`                        | `AuthContext → isStaff` → `StaffRoute`                     |
| `pre_save signal` (cálculos automáticos) | Campos calculados exibidos como somente leitura            |
| Paginação `PAGE_SIZE: 10`                | `TablePagination` com page/count                           |

---

## 14. Checklist de Entrega por Feature

Antes de dar PR como pronto, verificar:

- [ ] Tipagem completa (sem `any`)
- [ ] Hook isolado para chamadas de API
- [ ] Componente sem acesso direto ao `axios`/`fetch`
- [ ] Formulário validado com `zod` + `react-hook-form`
- [ ] Erros da API exibidos via `Alert`
- [ ] Loading state durante operações assíncronas
- [ ] Rotas protegidas corretamente (`PrivateRoute` ou `StaffRoute`)
- [ ] Responsividade com `Grid` e breakpoints do MUI
- [ ] Props tipadas (sem props desnecessárias — respeitar ISP)
- [ ] Tema MUI aplicado (sem cores hardcoded fora do theme)
- [ ] Testes automatizados para a feature (unitários e/ou de integração)

---

## 15. Divisão de Responsabilidades

### Por que dividir assim?

Gabriel constrói a **fundação técnica** primeiro (autenticação, rotas, infraestrutura de API, tema). Sabrina depende dessa fundação para trabalhar. Por isso, há uma **dependência de sequência** na Sprint 0, mas após isso **ambos trabalham em paralelo sem conflito**, pois atuam em arquivos completamente diferentes.

---

### Gabriel — Branch: `feat/gabriel/foundation`

**Domínio:** Infraestrutura, autenticação e setup global

| Sprint | Entrega                                            | Arquivos                                                                                        |
| ------ | -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 0      | Setup do projeto Vite + instalação de dependências | `package.json`, `vite.config.ts`, `tsconfig.json`                                               |
| 0      | Configuração do MUI Theme                          | `src/theme/index.ts`                                                                            |
| 0      | Todos os tipos TypeScript                          | `src/types/*.ts`                                                                                |
| 0      | Instância Axios com interceptors JWT               | `src/services/api.ts`                                                                           |
| 0      | AuthContext + useAuth hook                         | `src/contexts/AuthContext.tsx`, `src/hooks/useAuth.ts`                                          |
| 0      | `authService.ts` (login, refresh, register)        | `src/services/authService.ts`                                                                   |
| 1      | Página de Login com validação                      | `src/pages/auth/LoginPage.tsx`                                                                  |
| 1      | Página de Register (Stepper 2 etapas)              | `src/pages/auth/RegisterPage.tsx`                                                               |
| 1      | Roteamento completo + PrivateRoute + StaffRoute    | `src/App.tsx`                                                                                   |
| 1      | AppShell (layout base: sidebar + header)           | `src/components/layout/*.tsx`                                                                   |
| 1      | Componentes compartilhados                         | `src/components/shared/*.tsx`                                                                   |
| 2      | Página de Calibração de Equipamentos (staff)       | `src/pages/calibracao/*.tsx`, `src/hooks/useCalibracao.ts`, `src/services/calibracaoService.ts` |

**Sprint 0 é bloqueante para Sabrina** — Gabriel deve entregar o PR da Sprint 0 para `dev` antes de Sabrina iniciar.

---

### Sabrina — Branch: `feat/sabrina/laudos`

**Domínio:** Features de negócio (laudos, dashboard, visualização)

> **Pré-requisito:** PR da Sprint 0 do Gabriel mergeado em `dev` e Sabrina deve fazer `git merge dev` em sua branch antes de começar.

| Sprint | Entrega                                                    | Arquivos                                          |
| ------ | ---------------------------------------------------------- | ------------------------------------------------- |
| 1      | `laudoService.ts` (listar, buscar, criar, editar, deletar) | `src/services/laudoService.ts`                    |
| 1      | `useLaudos.ts` e `useLaudo.ts` hooks                       | `src/hooks/useLaudos.ts`, `src/hooks/useLaudo.ts` |
| 1      | Dashboard (cards de resumo + últimos laudos)               | `src/pages/dashboard/DashboardPage.tsx`           |
| 1      | Lista de Laudos com paginação e filtro por N Lab           | `src/pages/laudos/LaudosListPage.tsx`             |
| 2      | Detalhe do Laudo (Accordions por equipamento + PDF)        | `src/pages/laudos/LaudoDetailPage.tsx`            |
| 2      | Formulário de Laudo com Stepper 6 etapas (staff)           | `src/pages/laudos/LaudoFormPage.tsx`              |

---

### Zonas de trabalho — sem conflito de arquivos

```
Gabriel trabalha em:              Sabrina trabalha em:
├── src/theme/                    ├── src/services/laudoService.ts
├── src/types/                    ├── src/hooks/useLaudos.ts
├── src/services/api.ts           ├── src/hooks/useLaudo.ts
├── src/services/authService.ts   ├── src/pages/dashboard/
├── src/contexts/                 ├── src/pages/laudos/
├── src/hooks/useAuth.ts          └── (usa os types e services do Gabriel)
├── src/pages/auth/
├── src/components/layout/
├── src/components/shared/
├── src/App.tsx
└── src/pages/calibracao/
```

**Arquivos compartilhados (apenas leitura para Sabrina):**

- `src/types/*.ts` — Sabrina importa, Gabriel mantém
- `src/services/api.ts` — Sabrina importa, Gabriel mantém
- `src/contexts/AuthContext.tsx` — Sabrina consume via hook `useAuth()`

---

## 16. Estratégia de Integração com a API

### Resposta direta: integração incremental, não no final

**Não faça todas as telas primeiro para integrar só no fim.** Isso cria uma dívida técnica enorme e torna os bugs muito mais difíceis de rastrear. A abordagem correta é:

```
Tela nova → conecta na API real → valida → PR → próxima tela
```

### Fluxo recomendado por feature

```
1. Gabriel entrega api.ts (Axios + JWT) → dev
2. Sabrina puxa dev na sua branch
3. Sabrina implementa laudoService.ts com as chamadas reais
4. Sabrina implementa useLaudos.ts consumindo o service
5. Sabrina implementa LaudosListPage.tsx consumindo o hook
6. Testa com o backend rodando localmente
7. PR para dev
```

### Quando o backend não estiver disponível

Use um **mock local** no próprio service para não travar o desenvolvimento:

```ts
// src/services/laudoService.ts — modo mock (temporário)
const USE_MOCK = false; // mude para true se o backend não estiver rodando

export const laudoService = {
  listar: async (page = 1) => {
    if (USE_MOCK) {
      return { data: { results: MOCK_LAUDOS, count: 2 } };
    }
    return api.get(`meus-laudos/?page=${page}`);
  },
  // ...
};

// Mock data local — usar apenas para desenvolvimento
const MOCK_LAUDOS: AnaliseSolo[] = [
  {
    n_lab: "2026/001",
    cliente: {
      codigo: "CLI001",
      nome: "João da Silva",
      municipio: "Uberlândia",
      area: "Fazenda Boa Vista",
    },
    data_entrada: "2026-04-01",
    data_saida: null,
    ph_agua: 6.2,
    ph_cacl2: 5.8,
    ph_kcl: 5.5,
    // ... restante dos campos como null
  },
];
```

### Ordem de integração recomendada

| #   | Quem    | Feature                                   | Depende de |
| --- | ------- | ----------------------------------------- | ---------- |
| 1   | Gabriel | `POST /token/` (login)                    | —          |
| 2   | Gabriel | `POST /register/` (cadastro)              | —          |
| 3   | Gabriel | Rotas protegidas com token                | Item 1     |
| 4   | Sabrina | `GET /meus-laudos/` (listar)              | Item 3     |
| 5   | Sabrina | `GET /meus-laudos/:nLab/` (detalhe)       | Item 4     |
| 6   | Gabriel | `POST/PATCH/DELETE /meus-laudos/` (staff) | Item 3     |
| 7   | Sabrina | `GET /meus-laudos/:nLab/pdf/` (PDF)       | Item 5     |
| 8   | Gabriel | Baterias de calibração                    | Item 3     |

---

## 17. Tratamento de Erros

### Categorias de erro

| Categoria                             | Origem                         | Como tratar                                                   |
| ------------------------------------- | ------------------------------ | ------------------------------------------------------------- |
| **Validação de formulário**           | Frontend (zod)                 | Mensagem em vermelho embaixo do campo (`helperText` no MUI)   |
| **Erro de API (4xx)**                 | Backend retorna JSON com erros | `Alert` vermelho com a mensagem do DRF                        |
| **Erro de rede (500 / sem internet)** | Axios não consegue conectar    | `Alert` genérico "Erro de conexão. Tente novamente."          |
| **Token expirado (401)**              | Axios interceptor              | Renova automaticamente; se falhar → logout + redirect         |
| **Acesso negado (403)**               | Backend                        | Redireciona para `/dashboard` com `Alert` de permissão negada |
| **Não encontrado (404)**              | Backend                        | Exibe página `NotFound` ou mensagem inline                    |

---

### Padrão de tratamento em hooks

```ts
// src/hooks/useLaudos.ts — padrão de estado de erro

import { useState, useEffect } from "react";
import axios from "axios";
import { laudoService } from "../services/laudoService";
import type { AnaliseSolo } from "../types/analise";

interface UseLaudosState {
  laudos: AnaliseSolo[];
  loading: boolean;
  error: string | null;
  total: number;
}

export const useLaudos = (page = 1) => {
  const [state, setState] = useState<UseLaudosState>({
    laudos: [],
    loading: true,
    error: null,
    total: 0,
  });

  useEffect(() => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    laudoService
      .listar(page)
      .then(({ data }) => {
        setState({
          laudos: data.results,
          loading: false,
          error: null,
          total: data.count,
        });
      })
      .catch((err) => {
        const msg = axios.isAxiosError(err)
          ? (err.response?.data?.detail ?? "Erro ao carregar laudos.")
          : "Erro de conexão.";
        setState((prev) => ({ ...prev, loading: false, error: msg }));
      });
  }, [page]);

  return state;
};
```

---

### Padrão de exibição de erro em páginas

```tsx
// Exibição padronizada — use sempre este padrão
import { Alert, CircularProgress, Box } from "@mui/material";

const LaudosListPage = () => {
  const { laudos, loading, error } = useLaudos();

  if (loading) return <LoadingOverlay />;

  if (error)
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );

  // ... render normal
};
```

---

### Erros de formulário — formato DRF

O Django REST Framework retorna erros neste formato:

```json
{
  "n_lab": ["O padrão do N Lab deve ser ANO/NUMERO ex 2026/001"],
  "ph_agua": ["O pH deve estar entre 0 e 14."],
  "non_field_errors": ["Erro geral não associado a campo."]
}
```

Para exibir os erros por campo no formulário:

```ts
// Utilitário para converter erros do DRF para react-hook-form
export function applyDrfErrors<T extends Record<string, unknown>>(
  errors: Record<string, string[]>,
  setError: (field: keyof T, error: { message: string }) => void,
) {
  Object.entries(errors).forEach(([field, messages]) => {
    if (field !== "non_field_errors") {
      setError(field as keyof T, { message: messages[0] });
    }
  });
}

// Uso em LaudoFormPage.tsx:
try {
  await laudoService.criar(payload);
} catch (err) {
  if (axios.isAxiosError(err) && err.response?.status === 400) {
    applyDrfErrors(err.response.data, setError);
  }
}
```

---

### Feedback visual obrigatório

Todo fluxo assíncrono deve ter **3 estados visuais**:

```
estado: loading  → <CircularProgress /> ou <Skeleton />
estado: success  → conteúdo normal ou <Alert severity="success">
estado: error    → <Alert severity="error"> com a mensagem
```

**Nunca deixe a tela sem resposta** durante uma operação — o usuário precisa saber o que está acontecendo.

---

## 18. Checklist de Entrega por Feature

Antes de dar PR como pronto, verificar:

- [ ] Tipagem completa (sem `any`)
- [ ] Hook isolado para chamadas de API
- [ ] Componente sem acesso direto ao `axios`/`fetch`
- [ ] Formulário validado com `zod` + `react-hook-form`
- [ ] Erros da API exibidos via `Alert` (erro 4xx, erro de rede, 403, 404)
- [ ] Erros de campo mapeados do DRF para `react-hook-form`
- [ ] Loading state durante operações assíncronas
- [ ] Rotas protegidas corretamente (`PrivateRoute` ou `StaffRoute`)
- [ ] Responsividade com `Grid` e breakpoints do MUI
- [ ] Props tipadas (sem props desnecessárias — respeitar ISP)
- [ ] Tema MUI aplicado (sem cores hardcoded fora do theme)
- [ ] Branch atualizada com `dev` antes de abrir PR (`git merge dev`)
- [ ] Sem conflito com os arquivos da outra dev

---

_Este arquivo é o contrato técnico do frontend do LABAS. Qualquer mudança de arquitetura deve ser discutida com o tech lead antes de implementar._
