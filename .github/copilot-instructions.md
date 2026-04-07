# LABAS Frontend — Guia de Arquitetura

> **Tech Lead:** Gabriel Azevedo | **Dev:** Sabrina  
> **Stack:** React 19 + TypeScript + MUI v7 + React Hook Form + Zod + Axios  
> **API:** Django REST Framework + JWT (SimpleJWT) — `http://localhost:8000/api/`  
> **Última atualização:** 07/04/2026

---

## Indice

1. Contexto e escopo
2. Fluxo real de usabilidade
3. Principios de arquitetura (SOLID)
4. Estrutura do projeto
5. Rotas e acessos
6. Integracao com backend
7. Padroes de codigo
8. Testes automatizados
9. Checklist unico de entrega
10. Fluxo de branches e Boas Praticas (Git)
11. Sprints e responsabilidades
12. **Arquitetura 1:N (Laudo → Análises)** ← REGRA CORE
13. Diretrizes finais

---

## Diretrizes do Assistente: Projeto LABAS (Front-end / React)

Você é um Engenheiro de Software Sênior atuando no projeto **LABAS** (stack: React, Vite, MUI, React Hook Form, Zod e Axios).
Sua prioridade máxima é a **eficiência de tokens** e a **precisão técnica**.

### 1. Otimização Estrita de Tokens (Regras de Ouro)

Para evitar o esgotamento da janela de contexto e o corte de respostas:

- **Sem Boilerplate:** Não inicie as respostas com saudações longas ("Olá!", "Claro, vou ajudar!"). Vá direto para a solução técnica ou para o código.
- **Respostas Curtas e Focadas:** Explicações teóricas só devem ser fornecidas se explicitamente solicitadas. Foque no código e em comentários objetivos dentro do próprio código.
- **Evite Reescrever Código Intacto:** Se a alteração for em apenas uma função de um arquivo grande, forneça apenas a função alterada indicando onde ela deve ser encaixada, em vez de cuspir o arquivo de 300 linhas novamente.

### 2. Protocolo de Agrupamento Funcional (Entrega Modular)

**NUNCA** gere uma feature inteira (múltiplos arquivos) em um único prompt. Se for solicitado o desenvolvimento de uma tela ou módulo completo, você deve obrigatoriamente fatiar a entrega nos seguintes blocos e pedir autorização para avançar:

- **Bloco 1: Infraestrutura de Dados.** Apenas tipagens TypeScript (`.ts`) e serviços Axios (`Service.ts`).
- **Bloco 2: Lógica e Estado.** Apenas Schemas de validação (`Zod`) e Hooks customizados (`useFeature.ts`).
- **Bloco 3: Interface de Usuário (UI).** Apenas os componentes React e páginas MUI (`.tsx`).

Ao finalizar um bloco, encerre a resposta com: _"Bloco [X] concluído. Diga 'avançar' para gerar o Bloco [Y]."_

### 3. Gestão de Escopo e UX do Laboratório

Lembre-se sempre da regra de negócio do LABAS:

- **Dupla Persistência:** Leituras brutas são inseridas em lote na "Bancada" (via DataGrid) para rastreabilidade (`LeituraEquipamento`). O sistema usa a Bateria Ativa do dia para calcular o valor, que é salvo em `AnaliseSolo`.
- **Planilha Mestra:** A tela de detalhe do laudo apenas _exibe_ os dados já consolidados e calculados. Não possui campos de digitação de leitura bruta.

### 4. Padrões de Código

- Componentes `.tsx` não devem conter regras de requisição HTTP ou validação complexa; delegue tudo para Custom Hooks.
- Trate erros de API (400) achatando o retorno do Django e exibindo no `SnackbarContext`.

---

## 1. Contexto e escopo

Este guia define a arquitetura e os padroes do frontend do LABAS. Ele deve ser usado como referencia tecnica e guia de decisao. Evite duplicar logica e mantenha a implementacao sempre alinhada com este documento.

O sistema:

- Registra amostras e leituras do laboratorio
- Calcula indices agronomicos automaticamente
- Gera laudos em PDF

Tipos de usuario:

- `is_staff = true`: tecnico (CRUD completo)
- `is_staff = false`: cliente (consulta e download)

---

## 2. Fluxo real de usabilidade

Este fluxo guida todas as decisoes de UX e arquitetura. As telas devem seguir a rotina fisica do laboratorio.

1. **Preparo (Calibracao)**
   - Cria bateria, insere branco e padroes
   - Sistema gera $y=ax+b$ e $R^2$, tecnico ativa

2. **Operacao em Lote (antiga bancada)**
   - Tela de digitacao em lote para amostras
   - Filtro por elemento e exibicao da curva ativa
   - Tabela com: N_Lab, Fator de Diluicao, Leitura Bruta, Resultado calculado
   - Enter avanca linha e grava leitura em background

3. **Planilha Mestra (Detalhe do Laudo)**
   - Oculta leituras brutas
   - Destaca indices agronomicos (SB, CTC, V%, m%)
   - Download de PDF

---

## 3. Principios de arquitetura (SOLID)

- Cada arquivo tem responsabilidade unica
- Extensao via props, sem modificar componentes base
- Interfaces permitem substituicao sem quebrar o sistema
- Sem interfaces gordas
- Hooks e componentes dependem de abstracoes

---

## 4. Estrutura do projeto

```
src/
  main.tsx
  App.tsx
  theme/
  types/
  services/
  hooks/
  contexts/
  components/
    layout/
    shared/
  pages/
    auth/
    dashboard/
    laudos/
    calibracao/
    operacao-lote/
```

Tema MUI ja esta implementado em [labas-web/src/theme/index.ts](labas-web/src/theme/index.ts).

---

## 5. Rotas e acessos

- /login (publica)
- /register (publica)
- /dashboard (privada)
- /laudos (privada)
- /laudos/novo (staff)
- /laudos/:id (privada)
- /laudos/:id/editar (staff)
- /calibracao (staff)
- /calibracao/nova (staff)
- /entrada-lote (staff) — nome de tela: Operacao em Lote

Sempre proteger rotas sensiveis com PrivateRoute e StaffRoute.

---

## 6. Integracao com backend

- Toda chamada HTTP passa por [labas-web/src/services/api.ts](labas-web/src/services/api.ts)
- Nao usar fetch/axios direto em paginas
- Erros 400 do DRF vem como `{ campo: ["mensagem"] }`
- Usar Snackbar global para feedback de erro
- Dupla persistencia: LeituraEquipamento (rastreio) e AnaliseSolo (resultado)

Se o backend nao estiver disponivel, alinhe com Gabriel para ele providenciar.

---

## 7. Padroes de codigo

- Componentes: PascalCase
- Hooks: camelCase + `use`
- Services: camelCase + `Service`
- Types: PascalCase
- Constantes: UPPER_SNAKE_CASE

Regras de ouro:

1. Sem HTTP direto em componentes
2. Sem `any`
3. Sem duplicar permissoes
4. Sempre validar formularios
5. Sempre tratar erros da API
6. Sempre exibir loading
7. Campos calculados sao somente leitura
8. `n_lab` segue `AAAA/NNN`
9. **MUI Grid:** usar sempre `import { Grid } from "@mui/material"` com `<Grid container>` e `<Grid size={{ xs, md }}>` (Grid v2). Nunca usar `@mui/material/Grid2` ou `@mui/material/Unstable_Grid2` — modulos inexistentes neste projeto.

### Regra de Terminal e Comandos (Mãos no Teclado)

- **Sem Execução Autônoma:** Nunca tente executar comandos no terminal de forma autônoma.
- Sempre que for necessário rodar algo (instalar bibliotecas via `npm`, rodar migrações do Django, etc.), forneça os comandos em um bloco de código `bash` limpo e instrua: _"Rode o comando abaixo no seu terminal"_, para que eu mesmo faça a execução.

* **Backend usa Poetry:** O gerenciador de pacotes do backend (Django) é o **Poetry**. Sempre que fornecer comandos de terminal para o backend (instalação de dependências, migrações, testes), utilize estritamente a sintaxe do Poetry (ex: `poetry add <pacote>`, `poetry run python manage.py migrate`). Não sugira `pip install` ou chamadas de `python` soltas.

---

## 8. Testes automatizados

- Vitest, @testing-library/react, @testing-library/user-event, msw
- Testar schemas, hooks e paginas
- Testes em `src/__tests__/` espelhando a estrutura

---

## 9. Checklist unico de entrega

- [ ] Tipagem completa (sem `any`)
- [ ] Hook isolado para chamadas de API
- [ ] Componente sem acesso direto ao axios/fetch
- [ ] Formulario validado com zod + react-hook-form
- [ ] Erros da API exibidos via Snackbar
- [ ] Loading state durante operacoes assincronas
- [ ] Rotas protegidas corretamente
- [ ] Responsividade com Grid e breakpoints
- [ ] Tema MUI aplicado (sem cores hardcoded)
- [ ] Testes automatizados para a feature
- [ ] Branch atualizada com dev antes do PR
- [ ] Sem arquivos desnecessarios no commit (node_modules, dist, builds locais)

---

## 10. Fluxo de Branches e Boas Práticas (Git)

**A Regra de Ouro da Segurança:** NUNCA execute um comando de `merge` sem antes commitar o seu trabalho atual na sua branch. Commitar antes garante que o seu código fique salvo no histórico e não seja perdido caso dê algum conflito.

### Ao iniciar o dia ou retomar uma feature (Sincronização Diária)

1. **Salve o que você estava fazendo na sua branch atual:**

- `git add .`
- `git commit -m "chore: salvando progresso antes de sincronizar"`

2. **Atualize a branch base (`dev`):**

- `git checkout dev`
- `git pull origin dev`

3. **Volte para sua branch e traga as atualizações:**

- `git checkout feat/<sua-branch>`
- `git merge dev`
  > _Por que fazer isso? Isso garante que o seu código funcione perfeitamente com o que o resto da equipe fez ontem, além de resolver conflitos na sua máquina antes de abrir o PR._

### Ao iniciar uma nova feature

1. **Garanta que o `dev` está atualizado:**

- `git checkout dev`
- `git pull origin dev`

2. **Crie a sua nova branch a partir do `dev` limpo:**

- `git checkout -b feat/<nome-da-feature>`

3. **Durante o desenvolvimento:** Sincronize com o `dev` diariamente (repetindo os passos de "Ao iniciar o dia").

### Ao finalizar a feature

1. Garanta que sua branch está sincronizada com `dev` e que a aplicação roda sem erros localmente.
2. Faça o `git push` da sua branch.
3. Abra um Pull Request (PR) para a branch `dev` no GitHub (Review da equipe é obrigatória).

---

### 🚨 Regra Anti-Lixo: Prevenção de Arquivos Desnecessários

Sempre rode `git status` antes de fazer um `git add .` e `git commit`.

Se você notar que pastas pesadas ou sensíveis estão aparecendo em verde (prontas para subir), **PARE O QUE ESTÁ FAZENDO**. Nunca suba os seguintes arquivos/pastas para o GitHub:

- `node_modules/` (Bibliotecas do NPM)
- `dist/` ou `build/` (Código compilado)
- `.env` (Senhas e chaves secretas)
- `db.sqlite3` (Banco de dados local)

**Comandos rápidos de resgate (se você adicionou algo errado por engano):**

Se você rodou `git add .` e o `node_modules` entrou no rastreamento, tire-o do Git **sem apagar do seu computador** usando:

- `git rm -r --cached node_modules`

Em seguida, garanta que a palavra `node_modules/` está escrita dentro do seu arquivo `.gitignore`, e só então faça o seu commit final.

---

## 11. Sprints e Responsabilidades

### Gabriel — `feat/gabriel/foundation`

- ✅ Sprint 0: setup, tema, tipos, base de API e auth
- ✅ Sprint 1: login, register, layout, rotas, shared
- ✅ Sprint 2: calibracao completa
- ✅ Sprint 3: Operacao em Lote (rota /entrada-lote, UI profissional)
- ✅ Sprint 4: formulario de criacao de laudo + dashboard por perfil (staff/cliente)
  - `src/services/laudoService.ts` — CRUD + PDF (lidar, criar, buscar, atualizar, remover, baixarPdf, listarMeusLaudos, baixarPdfLaudo)
  - `src/hooks/useLaudoForm.ts` — hook de criacao com Zod + react-hook-form (incl. mapeamento de erros de API para campos do form)
  - `src/hooks/useLaudos.ts` — listagem + download de PDF para cliente
  - `src/schemas/laudoSchemas.ts` — schema Zod com input/output types
  - `src/pages/laudos/LaudoFormPage.tsx` — formulario de criacao (rota /laudos/novo, staff only)
  - `src/pages/dashboard/DashboardPlaceholder.tsx` — staff ve cards, cliente ve ClientDashboard
  - `src/pages/dashboard/components/ClientDashboard.tsx` — area do cliente com laudos recentes e PDF
  - `backend/serializers.py` — UniqueValidator em n_lab + create()/update() com resolucao de cliente_codigo
- ✅ Sprint 5: CRUD de clientes (staff only)
  - **Backend:** `ClienteCadastroSerializer` + `ClienteListCreateView` / `ClienteDetailView` + rotas `/clientes/` e `/clientes/<codigo>/`
  - `src/types/cliente.ts` + `src/services/clienteService.ts`
  - `src/schemas/clienteSchemas.ts` + `src/hooks/useClientes.ts` + `src/hooks/useClienteForm.ts`
  - `src/pages/clientes/ClientesPage.tsx` + `src/pages/clientes/ClienteFormPage.tsx`
- ✅ Sprint 6: Página de laudos — lista completa + editar + excluir (staff) — branch `feat/gabriel/laudos-page`
  - `src/hooks/useLaudos.ts` — refatorado: `Laudo[]`, `id: number`, `baixarPdf(id, codigoLaudo)`, `excluir(id)`, filtro por `codigo_laudo`/cliente
  - `src/pages/laudos/LaudosPage.tsx` — tabela MUI com colunas: Código, Cliente, Data Emissão; ações: ver detalhe, PDF, editar, excluir (staff); campo de busca; `ConfirmDialog`
  - `src/pages/laudos/LaudoFormPage.tsx` — formulário de criação cabeçalho only: Cliente (Autocomplete), `data_emissao`, `observacoes`
  - `src/pages/laudos/LaudoEditPage.tsx` — rota `/laudos/:id/editar` (staff); form do cabeçalho + DataGrid de análises (toggle ativo, remover); `useParams<{ id: string }>()`
- ✅ **Sprint 7 — Refatoração 1:N (Laudo → N Análises)** — branch `feat/gabriel/laudo-multi-analise`
  - **Bloco 0 — Backend:** migração Django — `AnaliseSolo` recebe ForeignKey `laudo` (NOT NULL, cascade); serializers aninhados; endpoints `/laudos/:id/analises/`; PDF WeasyPrint itera `laudo.analises.filter(ativo=True)`
  - **Bloco 1 — Tipos e Services:** `src/types/analise.ts` (`Laudo` + `AnaliseSolo` com `laudo_id`); `src/services/analiseService.ts` (listar, criar, atualizar, remover, toggleAtivo); `src/services/laudoService.ts` com `id: number`
  - **Bloco 2 — Hooks e Schemas:** `src/schemas/analiseSchemas.ts`; `src/hooks/useAnalises.ts` (por `laudoId`); `src/hooks/useLaudoForm.ts` e `useLaudoEditForm.ts` atualizados para `Laudo`
  - **Bloco 3 — UI:** `src/pages/laudos/LaudoDetalhePage.tsx` (rota `/laudos/:id`, read-only: cabeçalho + DataGrid + botão PDF); `src/App.tsx` (rotas com `:id`, lazy import `LaudoDetalhePage`)
- ✅ **Sprint 8 — Roteiro de Execução + Correção de Análises** — branch `feat/gabriel/laudo-multi-analise`
  - **`Laudo.data_saida`:** novo campo nullable `DateField` (migration `0019`); `data_emissao` relabelado para "Data de Entrada" na UI; `data_saida` ("Data de Saída") exposto em `LaudoEditPage`
  - **Fluxo de criação:** após `POST /laudos/`, frontend redireciona para `/laudos/:id/editar` (hook `useLaudoForm`)
  - **Sidebar:** item "Amostras" com `BiotechIcon` → `/entrada-lote`; botão "Ir para Amostras" no header de `LaudoEditPage`
  - **`useAnalises`:** adicionados `editando: number | null` e `editar(analiseId, payload)` → `PATCH /laudos/:id/analises/:id/`; `pagination_class = None` em `AnaliseSoloListCreateView` (fix spread error)
  - **Dialog Editar Ficha** (inline em `LaudoEditPage`): corrige `n_lab`, `referencia`, `data_entrada` via ícone `EditIcon`
  - **`DialogCorrecaoAnalise`** — `src/components/shared/DialogCorrecaoAnalise.tsx`:
    - Aba **Correção de Bancada**: lista leituras brutas por elemento; inputs de `leitura_bruta` + `fator_diluicao` (AA/FC/ES); PATCH em `/leituras/:id/` → signal re-dispara → recalcula SB/CTC/V%/m%; aviso informativo sobre recálculo automático
    - Aba **Granulometria**: inputs areia, argila, silte com validação soma ≤ 100%; PATCH direto em `AnaliseSolo`
    - Acionado pelo ícone `ScienceIcon` (cor `secondary`) na coluna de ações do DataGrid de amostras
  - **Backend — novos endpoints:**
    - `GET /api/analises/:id/leituras/` → `LeiturasPorAnaliseListView` (sem paginação)
    - `GET|PATCH /api/leituras/:id/` → `LeituraEquipamentoDetailView`
    - `LeituraEquipamentoDetalheSerializer`: expõe `elemento`, `elemento_display`, `equipamento`, `resultado_calculado`
  - **Novos arquivos frontend:** `src/types/analise.ts` (`LeituraDetalhe`, `LeituraCorrecaoPayload`); `src/services/correcaoService.ts`; `src/hooks/useCorrecaoAnalise.ts`; `src/services/analiseService.ts` + método `buscar(laudoId, analiseId)`

### Sabrina — `feat/sabrina/laudos`

- ~~Sprint 1: dashboard e lista de laudos~~ — assumido pelo Gabriel (Sprint 6)
- ~~Sprint 2: detalhe do laudo e PDF~~ — assumido pelo Gabriel (Sprint 6)

Zonas sem conflito:

- Gabriel: theme, types, api, auth, contexts, layout, shared, calibracao, operacao-lote, clientes
- Sabrina: laudos, dashboard, laudoService, hooks de laudo

---

## 12. Arquitetura 1:N (Laudo → Análises)

> **REGRA CORE — não violar.** Qualquer feature nova deve respeitar este contrato.

### Princípio Fundamental

**Laudo é o pai. AnaliseSolo é o filho. O PDF deve iterar sobre a coleção de análises.**

### Contratos de Entidade

| Entidade      | Papel                                             | Cardinalidade     |
| ------------- | ------------------------------------------------- | ----------------- |
| `Laudo`       | Cabeçalho do serviço — Cliente, Data, Observações | 1 (pai)           |
| `AnaliseSolo` | Amostra individual com N_Lab único                | N (filho, max 50) |

### Regras de Negócio

- **ForeignKey obrigatória:** `AnaliseSolo.laudo` é NOT NULL. Proibido criar `AnaliseSolo` sem `Laudo` pai.
- **Integridade referencial:** Ao deletar um `Laudo`, suas `AnaliseSolo` são removidas em cascata (`on_delete=CASCADE`).
- **N_Lab único por laudo:** `unique_together = ['laudo', 'n_lab']` — a unicidade de `n_lab` é validada no escopo do laudo pai, não globalmente.
- **codigo_laudo:** padrão `L-AAAA/N` (ex: `L-2026/1`), gerado automaticamente pelo backend via auto-increment por ano. O campo é read-only após criação.
- **Campo `ativo` em AnaliseSolo:** `ativo = BooleanField(default=True)`. Análises com `ativo=False` são excluídas do PDF e do DataGrid de detalhe do laudo. Somente staff pode alternar o flag.
- **PDF paginado:** O motor WeasyPrint itera `laudo.analises.filter(ativo=True)`. Limite de 50 análises ativas por laudo, com quebra de página a cada 5 (ou conforme layout do template).
- **Campos calculados (SB, CTC, V%, m%):** Somente leitura na UI — nunca expor input para esses campos.
- **Estratégia de migration:** Os registros legados de `AnaliseSolo` (sem laudo) recebem um `Laudo` stub gerado por cliente durante a migration — um laudo stub por cliente, agrupando todas as suas análises existentes.

### Contrato de API

```
GET    /laudos/                        # lista de laudos (cabeçalhos)
POST   /laudos/                        # cria laudo
GET    /laudos/:id/                    # detalhe do laudo
PUT    /laudos/:id/                    # edita laudo
DELETE /laudos/:id/                    # remove laudo + análises (cascade)
GET    /laudos/:id/analises/           # lista análises do laudo
POST   /laudos/:id/analises/           # adiciona análise ao laudo
GET    /laudos/:id/analises/:nLab/     # detalhe de uma análise
PUT    /laudos/:id/analises/:nLab/     # edita análise
DELETE /laudos/:id/analises/:nLab/     # remove análise
GET    /laudos/:id/pdf/                # PDF com todas as análises paginadas
```

### Regras de UI

- A tela de detalhe do laudo (`LaudoDetalhePage`) exibe o cabeçalho + DataGrid de análises.
- O DataGrid de análises **não possui campos de digitação de leitura bruta** — isso acontece na Operação em Lote (`/entrada-lote`).
- Botão "Gerar PDF" chama `/laudos/:id/pdf/` e faz download do documento único com todas as análises.

---

## 13. Diretrizes finais

- Entregas complexas devem ser divididas em blocos:
  1. Tipos e services
  2. Hooks e schemas
  3. Paginas e UI
- Qualquer mudanca de arquitetura deve ser validada com o tech lead

---

_Este arquivo e o guia vivo do frontend do LABAS. Consulte sempre antes de implementar. Duvidas ou mudancas, alinhe com o tech lead._
