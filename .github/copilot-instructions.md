# LABAS Frontend — Guia de Arquitetura

> **Tech Lead:** Gabriel Azevedo | **Dev:** Sabrina  
> **Stack:** React 19 + TypeScript + MUI v7 + React Hook Form + Zod + Axios  
> **API:** Django REST Framework + JWT (SimpleJWT) — `http://localhost:8000/api/`  
> **Última atualização:** 03/04/2026

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
10. Sprints e responsabilidades
11. Diretrizes finais

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
- /laudos/:nLab (privada)
- /laudos/:nLab/editar (staff)
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

## 10. Fluxo de branches e Boas Práticas (Git)

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

## 11. Sprints e responsabilidades

### Gabriel — `feat/gabriel/foundation`

- Sprint 0: setup, tema, tipos, base de API e auth
- Sprint 1: login, register, layout, rotas, shared
- Sprint 2: calibracao completa
- Sprint 3: Operacao em Lote (rota /entrada-lote, UI profissional)
- Sprint 4: formulario de criacao de laudo

### Sabrina — `feat/sabrina/laudos`

- Sprint 1: dashboard e lista de laudos
- Sprint 2: detalhe do laudo e PDF

Zonas sem conflito:

- Gabriel: theme, types, api, auth, contexts, layout, shared, calibracao, operacao-lote
- Sabrina: laudos, dashboard, laudoService, hooks de laudo

---

## 12. Diretrizes finais

- Entregas complexas devem ser divididas em blocos:
  1. Tipos e services
  2. Hooks e schemas
  3. Paginas e UI
- Qualquer mudanca de arquitetura deve ser validada com o tech lead

---

_Este arquivo e o guia vivo do frontend do LABAS. Consulte sempre antes de implementar. Duvidas ou mudancas, alinhe com o tech lead._
