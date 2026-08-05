# QA — Jornadas do Usuário (LABAS)

> **Fonte:** `GuidePage.tsx` — guia de uso embutido no sistema  
> **Objetivo:** testar o sistema do ponto de vista de quem opera — o técnico de laboratório.  
> Cada caso descreve o que o usuário vê, o que ele faz, e o que o sistema deve fazer em resposta.  
> Bugs encontrados são registrados em `ACHADOS.txt`.

---

## Fluxo correto resumido

```
Login → Cadastrar Cliente → Calibrar Equipamento (bateria ativa)
     → Criar Laudo → Inserir Amostras (bancada) → Revisar Análises
     → Gerar PDF → Comunicar ao cliente (WhatsApp / E-mail)
```

---

## J-UX-01 — Login

**Pré-condição:** servidor rodando, conta de técnico criada pelo admin.

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 01 | Abre o sistema sem sessão ativa | Redireciona para `/login` | Tela de login aparece imediatamente |
| 02 | Digita usuário e senha corretos → clica "Entrar" | Valida credenciais, armazena tokens, redireciona para `/` | Dashboard ou listagem de laudos aparece; sidebar visível |
| 03 | Digita senha errada → clica "Entrar" | Exibe snackbar de erro com mensagem do backend | Usuário permanece na tela de login; campos não são limpos |
| 04 | Clica "Entrar" com campos vazios | Validação client-side impede o submit | Mensagem de campo obrigatório embaixo do input |
| 05 | Clica no botão de logout (ícone no canto) | Limpa tokens, redireciona para `/login` | Não é mais possível navegar para páginas protegidas |
| 06 | Após logout, tenta acessar `/laudos` pelo browser | Redireciona para `/login` | Nenhum dado sensível exibido |
| 07 | Token expira enquanto o técnico está operando | Interceptor renova o token silenciosamente | Operação continua sem interrupção; nenhum snackbar de erro |

---

## J-UX-02 — Cadastro e Gestão de Clientes

**Pré-condição:** técnico logado com `is_staff=True`.

### Fluxo feliz — Cadastrar cliente novo

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 01 | Clica em "Clientes" na sidebar | Carrega lista de clientes paginada | Lista aparece; sem spinner infinito |
| 02 | Clica em "Novo Cliente" | Exibe formulário de cadastro | Campos: Código, Nome, Telefone, E-mail, Município, Área, Observações |
| 03 | Preenche somente Código e Nome → salva | Aceita o cadastro | `201`; campos opcionais ficam como `—` na listagem |
| 04 | Preenche todos os campos → salva | Aceita o cadastro | `201`; cliente aparece na listagem |
| 05 | Usa a busca para procurar o cliente cadastrado | Filtra resultados em tempo real | Cliente aparece; busca parcial funciona (ex: digitar "silva" encontra "João Silva") |

### Fluxo de erro — Validações

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 06 | Tenta cadastrar código já existente | Exibe erro com a chave `código` | Mensagem clara: "Este código já está em uso" |
| 07 | Tenta salvar sem preencher o Código | Validação client-side bloqueia | Campo Código marcado com erro |
| 08 | Busca por nome que não existe | Exibe lista vazia | Nenhuma mensagem de erro; estado vazio amigável |

### Edição e remoção

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 09 | Clica no ícone de editar de um cliente | Abre formulário preenchido com dados atuais | Todos os campos editáveis exceto o Código |
| 10 | Atualiza o telefone → salva | `200`; dados atualizados na listagem | Snackbar de sucesso |
| 11 | Clica no ícone de remover → confirma | `204`; cliente some da listagem | Dialog de confirmação antes de deletar |

> **Dica do guia:** o código do cliente não pode ser alterado após a criação. Teste que o campo Código esteja desabilitado no modo edição.

---

## J-UX-03 — Calibração de Equipamentos

**Pré-condição:** técnico logado com `is_staff=True`.

### Criar nova bateria e calcular curva

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 01 | Acessa "Calibração" na sidebar | Lista de baterias existentes | Colunas: Equipamento, Elemento, R², Status (Ativa/Inativa) |
| 02 | Clica em "Nova Calibração" | Abre formulário com campos condicionais por equipamento | AA: exige Volume Solo, Volume Extrator, Leitura Branco |
| 03 | Seleciona AA / Ca, preenche volumes e branco → salva | `201`; curva ainda nula (sem pontos) | Bateria aparece na lista com R² = `—` |
| 04 | Adiciona 1 ponto (concentração + absorvância) | `201`; R² ainda `—` (mínimo 2 pontos) | Ponto aparece na tabela da bateria |
| 05 | Adiciona 2º ponto | `201`; sistema calcula curva automaticamente | R², coeficientes e equação aparecem preenchidos |
| 06 | Ativa a bateria | Desativa qualquer outra bateria ativa do mesmo elemento | `200`; chip "Ativa" visível; outra bateria passa a "Inativa" |
| 07 | Tenta ativar a bateria que já está ativa | Operação é idempotente | `200`; nenhum efeito colateral |

### Casos específicos por equipamento

| # | O que o usuário faz | O que o sistema deve fazer |
|---|---|---|
| 08 | Cria bateria PH / ph_agua (sem volumes) | Aceita sem exigir Volume Solo / Extrator |
| 09 | Cria bateria ES / MO (sem volumes) | Aceita — MO usa fórmula fixa |
| 10 | Cria bateria AA sem informar Leitura Branco | Rejeita com erro no campo `leitura_branco` |
| 11 | Cria bateria ES (não-MO) sem Volume Solo | Rejeita com erro no campo `volume_solo` |

### Modo edição

| # | O que o usuário faz | O que o sistema deve fazer |
|---|---|---|
| 12 | Clica em editar uma bateria existente | Abre formulário com dados atuais + lista de pontos existentes |
| 13 | Remove um ponto → restam menos de 2 | Curva é resetada (R² vira `—`) |
| 14 | Edita Volume Solo de uma bateria com curva | Parâmetros salvos; curva permanece (depende de pontos, não de volume) |

> **Dica do guia:** o branco deve ser inserido como ponto com concentração 0. Testar que um ponto com `concentracao=0` é aceito e contribui para o cálculo da curva.

---

## J-UX-04 — Criar Laudo

**Pré-condição:** pelo menos 1 cliente cadastrado.

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 01 | Acessa "Meus Laudos" na sidebar | Lista de laudos existentes | Colunas: Código, Cliente, Data de Entrada, Data de Saída |
| 02 | Clica em "Novo Laudo" | Abre formulário: busca de cliente + data de entrada | Campo de busca de cliente com autocomplete |
| 03 | Digita parte do nome/código do cliente | Lista filtrada em tempo real | Sem lag perceptível; debounce de ~300ms |
| 04 | Seleciona o cliente → preenche data → cria | `201`; redireciona para tela de edição do laudo | Código gerado automaticamente: formato `L-AAAA/N` |
| 05 | Cria 2º laudo para o mesmo ano | Sequencial incrementa | `L-2026/1` → `L-2026/2` |
| 06 | Tenta criar sem selecionar cliente | Validação bloqueia | Mensagem de campo obrigatório |
| 07 | Informa cliente que não existe | `400`; mensagem com chave `cliente_codigo` | Snackbar de erro com detalhe do backend |

---

## J-UX-05 — Entrada de Amostras (Bancada em Lote)

**Pré-condição:** laudo criado; bateria ativa para o elemento desejado; amostras com N. Lab associadas ao laudo.

> Esta é a jornada mais crítica: qualquer falha aqui gera resultados errados no laudo do cliente.

### Fluxo feliz

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 01 | Acessa "Amostras" na sidebar | Tela com filtros Equipamento e Elemento | Sem dados ainda; nenhum spinner desnecessário |
| 02 | Seleciona Equipamento (ex: Absorção Atômica) | Lista de elementos disponíveis para o equipamento | Apenas elementos válidos para AA aparecem |
| 03 | Seleciona Elemento (ex: Mg) → clica "Carregar" | Busca bateria ativa + amostras pendentes | Painel da curva ativa aparece (equação, R², branco, volumes) |
| 04 | Edita a célula "Leitura Bruta" de uma linha → pressiona Enter | API salva a leitura; calcula resultado via signal do backend | Coluna "Resultado Calculado" preenche com o valor; status vira "Salvo" |
| 05 | Edita célula "Fator de Diluição" antes da leitura | Preserva o valor digitado sem chamar a API ainda | Nenhum spinner; nenhuma chamada à API prematura |
| 06 | Depois de digitar o Fator, edita a Leitura Bruta → Enter | Agora chama a API com ambos os valores | Resultado calculado correto aparece |
| 07 | Todas as amostras processadas | Estado vazio amigável | "Todas as amostras para Mg já foram processadas nesta bateria." |

### Casos de erro e alertas

| # | O que o usuário faz / situação | O que o sistema deve mostrar |
|---|---|---|
| 08 | Seleciona elemento sem bateria ativa | Alerta vermelho: "Nenhuma bateria ativa para [Elemento]..." |
| 09 | Bateria ativa existe mas sem curva (< 2 pontos) | Alerta laranja: "Bateria ativa encontrada, mas a curva ainda não está calculada. Adicione pelo menos 2 pontos." |
| 10 | AA sem Fator de Diluição → tenta salvar | API bloqueia com `400`; snackbar de erro; linha volta ao status anterior |
| 11 | Troca de Equipamento após carregar | Reset completo: bateria e amostras anteriores somem; novo filtro necessário |
| 12 | Troca de Elemento após carregar | Mesmo comportamento de reset |

> **Dica do guia:** nunca insira amostras sem confirmar que a bateria está ativa para o elemento correspondente. O sistema deve deixar isso visualmente claro antes de permitir digitação.

---

## J-UX-06 — Revisar Análises no Laudo

**Pré-condição:** laudo com amostras que passaram pela bancada.

### Gerenciar amostras

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 01 | Acessa a tela de edição de um laudo | Tabela de amostras com colunas: N. Lab, Referência, Entrada, Ativo, SB, CTC, V% | Dados corretos; colunas calculadas preenchidas quando há leituras |
| 02 | Clica no toggle "Ativo" de uma amostra → desativa | `200`; chip muda para "Não" | Snackbar: "Análise desativada." |
| 03 | Reativa a amostra | `200`; chip volta para "Sim" | Snackbar: "Análise ativada." |
| 04 | Clica no ícone de editar (lápis) de uma amostra | Dialog abre com N. Lab, Referência e Data de Entrada preenchidos | Campos editáveis; N. Lab validado com formato `AAAA/NNN` |
| 05 | Salva edição com N. Lab inválido (ex: `abc`) | Validação client-side bloqueia | Mensagem: "Formato inválido. Use AAAA/NNN (ex: 2026/001)" |
| 06 | Tenta criar amostra com N. Lab já existente | `400`; dialog permanece aberto | Snackbar com detalhe do backend: "n_lab já cadastrado" |
| 07 | Clica no ícone de excluir (lixeira) de uma amostra | Dialog de confirmação | Ao confirmar: amostra some da tabela; snackbar de sucesso |

### Corrigir leitura individual

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 08 | Clica no ícone de correção (tubo de ensaio) de uma amostra | Dialog abre com duas abas: Bancada e Granulometria | Aba Bancada lista todas as leituras da amostra com valores atuais |
| 09 | Edita a Leitura Bruta de um elemento → salva | `200`; backend recalcula via signal; dialog atualiza | Índices recalculados (SB, CTC, V%) refletidos nos campos |
| 10 | Edita Fator de Diluição junto com a leitura | Ambos enviados no PATCH | Resultado recalculado corretamente |
| 11 | Vai para aba Granulometria → preenche Areia, Argila, Silte → salva | `200`; valores gravados | Snackbar: "Granulometria salva." |

---

## J-UX-07 — Gerar PDF e Comunicar ao Cliente

**Pré-condição:** laudo com pelo menos 1 análise ativa.

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 01 | Na tela de detalhe do laudo, clica em "Gerar PDF" | Chama `GET /laudos/{id}/pdf/`; faz download | Arquivo `laudo_L-AAAA-N.pdf` é baixado automaticamente |
| 02 | PDF contém apenas análises ativas | Análises com `ativo=False` não aparecem no documento | Verificar visualmente que amostras inativadas não constam |
| 03 | Clica em "WhatsApp" | Abre nova aba com link `wa.me/55{telefone}?text=...` | Link com mensagem padrão e número do cliente sem caracteres especiais |
| 04 | Cliente sem telefone cadastrado → clica "WhatsApp" | Snackbar de aviso | "O cliente não possui um telefone registado." |
| 05 | Clica em "E-mail" → aguarda | Botão desabilitado durante envio; spinner no ícone | Snackbar: "E-mail enviado com sucesso para o cliente!" |
| 06 | Backend falha ao enviar e-mail | Snackbar com detalhe do erro do backend | Botão volta ao estado normal após falha |
| 07 | Laudo inexistente (URL digitada manualmente) | `404` tratado; tela de erro amigável ou redirecionamento | Sem tela branca ou erro JavaScript |

---

## J-UX-08 — Gestão de Técnicos (staff only)

**Pré-condição:** usuário logado com `is_staff=True`.

| # | O que o usuário faz | O que o sistema deve fazer | Critério de sucesso |
|---|---|---|---|
| 01 | Acessa "Usuários" na sidebar | Lista de técnicos cadastrados | Colunas: Nome, Username, E-mail |
| 02 | Clica em "Novo Técnico" | Formulário: Nome, Username, E-mail, Senha, Confirmar Senha | Validação client-side com Zod |
| 03 | Preenche todos os campos corretamente → cadastra | `201`; técnico aparece na lista | Snackbar de sucesso; formulário fecha/limpa |
| 04 | Senha com menos de 8 caracteres | Validação Zod bloqueia | Mensagem: "Senha deve ter pelo menos 8 caracteres" |
| 05 | Senhas não coincidem | Validação Zod bloqueia | Mensagem de confirmação de senha |
| 06 | Username já existente | `400` do backend | Snackbar com detalhe do backend: "username já cadastrado" |
| 07 | E-mail já existente | `400` do backend | Snackbar com detalhe do backend |
| 08 | Clica no ícone de remover outro técnico → confirma | `204`; técnico some da lista | Dialog de confirmação (`ConfirmDialog`) antes de deletar |
| 09 | Tenta remover a própria conta | `400` do backend | Snackbar: "Você não pode remover sua própria conta" |
| 10 | Usuário sem `is_staff` tenta acessar `/usuarios` | Redirecionado por `StaffRoute` | Não vê a página de gestão de técnicos |

---

## J-UX-09 — Jornada Completa End-to-End (Fluxo do Guia)

> Cobre o ciclo completo de uma requisição real de análise de solo.

| # | Ação | Verificação |
|---|---|---|
| 01 | Login com técnico válido | Dashboard visível |
| 02 | Cadastrar cliente "Fazenda Modelo" (código: FM-001) | Aparece na listagem |
| 03 | Criar bateria AA / Ca (volumes + branco) | Bateria criada sem curva |
| 04 | Adicionar 2+ pontos à bateria | Curva calculada; R² visível |
| 05 | Ativar a bateria | Chip "Ativa"; outras AA/Ca desativadas |
| 06 | Criar laudo para FM-001 com data de hoje | Código `L-{ano}/N` gerado; redirecionado para edição |
| 07 | Criar 2 amostras no laudo (N. Lab: `{ano}/001` e `{ano}/002`) | Aparecem na tabela com `Ativo=Sim` |
| 08 | Acessar Amostras → AA / Ca → Carregar | Painel de curva ativa exibido; as 2 amostras aparecem |
| 09 | Preencher Fator e Leitura Bruta para cada amostra → Enter | Status "Salvo"; Resultado Calculado preenchido |
| 10 | Voltar ao laudo → desativar a amostra `{ano}/002` | Toggle "Não"; snackbar confirma |
| 11 | Abrir detalhe do laudo | "Análises (1 ativa)" listadas |
| 12 | Clicar "Gerar PDF" | Download do arquivo; apenas a amostra ativa consta no PDF |
| 13 | Clicar "WhatsApp" | Abre link `wa.me/55...` com mensagem padrão |

---

## Achados a registrar durante os testes

Ao encontrar qualquer comportamento divergente dos critérios acima, registrar em `ACHADOS.txt` seguindo o formato:

```
[J-UX-XX-NN] Título curto
----------------------------------------------------------------------
Jornada  : J-UX-XX — Nome da Jornada
Caso     : #NN — O que o usuário faz
Esperado : (descrição do comportamento esperado)
Obtido   : (descrição do que realmente aconteceu)
Impacto  : Alto / Médio / Baixo
Situação : Aberto / Corrigido em AAAA-MM-DD
```

---

## Achados já conhecidos (do backend) com impacto no frontend

| ID | Jornada | Descrição | Impacto no frontend |
|---|---|---|---|
| J5-02 | J-UX-05 / #09 | Bateria sem curva retorna `resultado_calculado=0.0` em vez de `null` | Frontend exibe `0.0000` em vez de `—` se o usuário salvar uma leitura com bateria sem curva |
| J2-01 | — | `validate_codigo` é código morto no backend | Nenhum impacto no frontend |
