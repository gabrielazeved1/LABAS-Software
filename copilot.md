# LABAS Frontend — Guia de Arquitetura

> **Tech Lead:** Gabriel Azevedo  
> **Devs:** Gabriel Azevedo & Sabrina  
> **Stack:** React 18 + TypeScript + Material UI (MUI) v6  
> **Paradigma:** SOLID aplicado a React  
> **API:** Django REST Framework + JWT (SimpleJWT)  
> **Base URL da API:** `http://localhost:8000/api/`

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
import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1A5276", // Azul UFU profundo
      light: "#2E86C1", // Azul médio — botões hover
      dark: "#0E2F44", // Azul escuro — sidebar, header
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#2E7D32", // Verde agrônomo
      light: "#4CAF50", // Verde claro — badges de status OK
      dark: "#1B5E20", // Verde escuro — ênfase
      contrastText: "#FFFFFF",
    },
    warning: {
      main: "#F9A825", // Âmbar terra — alertas e destaques
    },
    error: {
      main: "#C62828", // Vermelho — valores críticos
    },
    background: {
      default: "#F4F6F8", // Cinza claríssimo — fundo geral
      paper: "#FFFFFF", // Branco — cards, tabelas
    },
    text: {
      primary: "#1C2833", // Quase preto — texto principal
      secondary: "#5D6D7E", // Cinza médio — labels, subtítulos
    },
    divider: "#D5D8DC", // Cinza divisor (similar ao #f2f2f2 do PDF)
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Arial", sans-serif',
    h4: { fontWeight: 700 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    body2: { color: "#5D6D7E" },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: { textTransform: "none", fontWeight: 600 },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          "& th": {
            backgroundColor: "#1A5276",
            color: "#FFFFFF",
            fontWeight: 700,
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { fontWeight: 600 },
      },
    },
  },
});
```

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
✅ CERTO:  useLaudos() faz o fetch | LaudoForm renderiza | validators/laudo.ts valida
```

### O — Open/Closed (Aberto/Fechado)

> Componentes são **abertos para extensão via props**, fechados para modificação interna.

```tsx
// ✅ Extensível via props — nunca altere o componente base para um caso específico
<StatusChip status="pendente" />
<StatusChip status="concluido" />
<StatusChip status="cancelado" />
```

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

---

_Este arquivo é o contrato técnico do frontend do LABAS. Qualquer mudança de arquitetura deve ser discutida com o tech lead antes de implementar._
