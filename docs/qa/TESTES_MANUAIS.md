# Testes Manuais — LABAS

> Execute do início ao fim na ordem abaixo.  
> Marque cada caso como ✅ Passou · ❌ Falhou · ⚠️ Comportamento inesperado.  
> Registre qualquer achado em `ACHADOS.txt`.

---

## Pré-requisito — Dados mínimos para os testes

Antes de começar, certifique-se de ter:
- Backend rodando em `http://localhost:8000`
- Frontend rodando em `http://localhost:5173`
- Conta de técnico criada via `python manage.py createsuperuser`

---

## M-01 — Login e Segurança

### Bons casos

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Abra o sistema sem sessão → acesse `http://localhost:5173/laudos` | Redireciona para `/login` antes de exibir qualquer dado | |
| 02 | Preencha usuário e senha corretos → clique "Entrar" | Dashboard/laudos visível; sidebar com todos os módulos | |
| 03 | Permaneça logado por alguns minutos e faça uma ação qualquer | Sistema continua funcionando sem pedir login novamente (token renovado silenciosamente) | |
| 04 | Clique no ícone de logout | Redireciona para `/login`; pressionar Voltar no navegador não mostra dados | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 05 | Deixe usuário e senha em branco → clique "Entrar" | Mensagens de campo obrigatório embaixo dos inputs; nenhuma requisição enviada | |
| 06 | Digite senha com 7 caracteres → clique "Entrar" | Mensagem "Mínimo de 8 caracteres" aparece; nenhuma requisição enviada | |
| 07 | Digite senha correta de outro usuário para seu usuário | Mensagem de erro do backend; permanece na tela de login | |
| 08 | Com sessão ativa, edite manualmente o token no `localStorage` e recarregue | Sistema detecta token inválido e redireciona para `/login` | |

---

## M-02 — Cadastro de Clientes

### Bons casos

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Clique em "Clientes" → "Novo Cliente" → preencha só Código `CLI-T01` e Nome `Fazenda Teste` → salve | Cliente aparece na listagem com campos opcionais em "—" | |
| 02 | Clique em "Novo Cliente" → preencha todos os campos incluindo telefone `(34) 99999-0001` e e-mail → salve | Cliente aparece na listagem com todos os dados | |
| 03 | Na listagem, clique em editar do cliente criado | Formulário abre com dados preenchidos; campo **Código está desabilitado** | |
| 04 | Altere o telefone → salve | Telefone atualizado; snackbar de sucesso | |
| 05 | Clique em excluir de um cliente → confirme no dialog | Dialog de confirmação aparece (não `window.confirm` nativo); cliente some da lista após confirmar | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 06 | Tente criar novo cliente com o mesmo Código `CLI-T01` | Erro: "Este código já está em uso" (ou similar); cliente não criado | |
| 07 | Tente salvar cliente sem informar o Código | Campo Código marcado com erro; botão não envia | |
| 08 | Tente salvar cliente sem informar o Nome | Campo Nome marcado com erro | |
| 09 | No dialog de exclusão, clique em "Cancelar" | Dialog fecha; cliente permanece na lista | |

---

## M-03 — Calibração de Equipamentos

### Bons casos — criar e ativar bateria

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Clique em "Calibração" → "Nova Calibração" → selecione AA / Ca → preencha Volume Solo=`5`, Volume Extrator=`50`, Leitura Branco=`0.002` → salve | Bateria criada; R² aparece como "—" (sem pontos ainda) | |
| 02 | Clique na bateria criada → adicione 1 ponto: Concentração=`0` (branco), Absorvância=`0.002` | 1 ponto salvo; curva ainda "—" | |
| 03 | Adicione 2º ponto: Concentração=`2`, Absorvância=`0.090` | Curva calculada automaticamente; R², `a` e `b` aparecem preenchidos | |
| 04 | Adicione mais pontos → verifique que R² melhora | R² se aproxima de 1 conforme os pontos ficam mais lineares | |
| 05 | Clique em "Ativar" nessa bateria | Chip "Ativa" aparece; qualquer outra bateria AA/Ca existente passa para "Inativa" | |
| 06 | Crie bateria PH / ph_agua → salve sem informar volumes | Aceito sem erro (PH não exige volumes) | |
| 07 | Crie bateria ES / MO → salve sem informar volumes | Aceito sem erro (MO usa fórmula fixa) | |

### Bons casos — modo edição

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 08 | Clique em editar de uma bateria com pontos | Formulário abre com os parâmetros atuais **e a lista de pontos existentes** | |
| 09 | Remova um ponto → restam menos de 2 | R² e coeficientes voltam para "—" | |
| 10 | Clique em "Ativar" numa bateria que já está ativa | Nenhum efeito colateral; estado permanece "Ativa" | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 11 | Crie bateria AA sem informar Leitura Branco | Erro no campo `leitura_branco`; bateria não criada | |
| 12 | Crie bateria ES (elemento P-Mehlich) sem Volume Solo | Erro no campo `volume_solo` | |
| 13 | Tente inserir 2 pontos com concentrações idênticas (ex: ambos `2.0`) | Backend invalida a curva (inclinação = 0 — "Leituras idênticas") | |
| 14 | Tente inserir transmitância `0` em ponto de bateria ES | Curva invalidada (T% ≤ 0 não tem log₁₀) | |

---

## M-04 — Criar Laudo

### Bons casos

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Clique em "Meus Laudos" → "Novo Laudo" | Formulário com autocomplete de cliente e campo de data | |
| 02 | Digite `Faz` no campo Cliente | Após ~300ms, lista filtra clientes com "Faz" no nome (debounce; não deve disparar por keystroke) | |
| 03 | Selecione `CLI-T01 — Fazenda Teste` → informe data de hoje → clique "Criar laudo" | Redirecionado para tela de edição do laudo; código `L-{ano}/N` gerado automaticamente | |
| 04 | Crie um 2º laudo para o mesmo cliente | Código sequencial: `L-{ano}/2` | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 05 | Tente criar laudo sem selecionar cliente | Mensagem "Cliente é obrigatório"; formulário não enviado | |
| 06 | Tente criar laudo sem data de entrada | Mensagem de campo obrigatório | |
| 07 | Digite código de cliente inexistente diretamente (sem usar o autocomplete) | Backend retorna erro; snackbar com detalhe | |

---

## M-05 — Adicionar Amostras ao Laudo

> Execute na tela de edição do laudo criado em M-04.

### Bons casos

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Clique em "Nova Amostra" | Dialog abre com campos N. Lab, Referência e Data de Entrada | |
| 02 | Preencha N. Lab=`{ano}/001`, Referência=`Amostra A`, Data=hoje → salve | Amostra aparece na tabela com Ativo=**Sim** | |
| 03 | Crie 2ª amostra: N. Lab=`{ano}/002`, Referência=`Amostra B` | 2ª amostra na tabela | |
| 04 | Clique em editar da amostra → altere a Referência → salve | Referência atualizada; dialog fecha | |
| 05 | Clique no toggle "Ativo" de uma amostra → desative | Toggle muda para "Não"; snackbar "Análise desativada." | |
| 06 | Reative a mesma amostra | Toggle volta para "Sim"; snackbar "Análise ativada." | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 07 | Tente criar amostra com N. Lab `2026/abc` (formato inválido) | Mensagem "Formato inválido. Use AAAA/NNN (ex: 2026/001)"; botão Salvar bloqueado | |
| 08 | Tente criar 2ª amostra com mesmo N. Lab `{ano}/001` | Backend rejeita; dialog permanece aberto; snackbar com detalhe | |
| 09 | Tente criar amostra sem N. Lab | Validação client-side bloqueia | |
| 10 | Clique em excluir de uma amostra → cancele no dialog | Amostra permanece; nenhuma requisição enviada | |
| 11 | Clique em excluir → confirme | Amostra removida da tabela; snackbar de sucesso | |

---

## M-06 — Entrada de Amostras (Bancada)

> Pré-condição: bateria AA/Ca ativa com curva calculada (M-03); amostras `{ano}/001` e `{ano}/002` criadas (M-05).

### Bons casos

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Clique em "Amostras" → selecione Equipamento=`Absorção Atômica`, Elemento=`Ca` → clique "Carregar" | Painel da curva ativa aparece (equação, R², branco, volumes); amostras `{ano}/001` e `{ano}/002` listadas | |
| 02 | Clique na célula "Fator Diluição" da linha `{ano}/001` → digite `5` → pressione Tab | Valor preservado sem chamar API ainda | |
| 03 | Clique em "Leitura Bruta" → digite `0.213` → pressione Enter | Resultado Calculado preenche automaticamente; status vira "Salvo" | |
| 04 | Repita para `{ano}/002`: Fator=`5`, Leitura=`0.189` → Enter | 2ª linha processada; status "Salvo" | |
| 05 | Troque Elemento para `Mg` → clique "Carregar" | Lista e painel de curva resetam; amostras para Mg aparecem | |
| 06 | Processe todas as amostras de Mg | Estado vazio: "Todas as amostras para Mg já foram processadas nesta bateria." | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 07 | Selecione um elemento **sem bateria ativa** → clique "Carregar" | Alerta **vermelho**: "Nenhuma bateria ativa para [elemento]..." | |
| 08 | Selecione um elemento com bateria ativa mas sem curva (< 2 pontos) → "Carregar" | Alerta **laranja**: "Bateria ativa encontrada, mas a curva ainda não está calculada. Adicione pelo menos 2 pontos." | |
| 09 | Com AA carregado, não preencha Fator Diluição → tente salvar só a Leitura | API **não é chamada**; linha preserva o valor digitado sem status "Salvo" | |
| 10 | Após carregar, troque o Equipamento | Lista e painel resetam completamente; novo filtro necessário | |
| 11 | Digite leitura negativa ou zero → Enter | Resultado Calculado pode ser negativo — backend aplica trava (resultado ≥ 0) | |

---

## M-07 — Corrigir Leitura (Dialog Correção)

> Pré-condição: amostra com leituras processadas na bancada (M-06).

### Bons casos

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Na tela de edição do laudo, clique no ícone de correção (tubo de ensaio) de uma amostra | Dialog abre com abas "Bancada" e "Granulometria"; aba Bancada lista os elementos lidos com valores atuais | |
| 02 | Altere a Leitura Bruta do Ca → salve | `200`; índices SB, CTC, V% recalculados no dialog imediatamente | |
| 03 | Altere o Fator de Diluição junto com a leitura → salve | Ambos enviados; resultado recalculado | |
| 04 | Vá para aba "Granulometria" → preencha Areia, Argila, Silte → salve | Snackbar "Granulometria salva."; dialog permanece aberto | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 05 | Salve a correção com campo obrigatório vazio | Validação bloqueia ou backend retorna erro | |
| 06 | Feche o dialog → verifique a tabela do laudo | Colunas SB/CTC/V% refletem os valores recalculados | |

---

## M-08 — Gerar PDF e Comunicar ao Cliente

> Pré-condição: laudo com pelo menos 1 análise ativa.

### Bons casos

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Na tela de detalhe do laudo, clique em "Gerar PDF" | Arquivo `laudo_L-{ano}-N.pdf` é baixado; sem erro | |
| 02 | Abra o PDF | Somente amostras com Ativo=Sim aparecem no documento | |
| 03 | Com cliente com telefone cadastrado, clique "WhatsApp" | Nova aba abre com `wa.me/55{número}?text=...`; número sem caracteres especiais | |
| 04 | Clique "E-mail" (com backend de e-mail configurado) | Botão desabilitado + spinner durante o envio; snackbar "E-mail enviado com sucesso para o cliente!" | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 05 | Inative **todas** as amostras do laudo → gere o PDF | PDF gerado (ou backend retorna arquivo vazio); não deve dar erro 500 | |
| 06 | Com cliente **sem telefone**, clique "WhatsApp" | Snackbar de **aviso** (não erro): "O cliente não possui um telefone registado." | |
| 07 | Com backend de e-mail desconfigurado, clique "E-mail" | Snackbar com detalhe do erro do backend; botão volta ao estado normal | |
| 08 | Acesse `http://localhost:5173/laudos/99999` diretamente | Tela de erro amigável ou redirecionamento; sem tela branca | |

---

## M-09 — Gestão de Técnicos

### Bons casos

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Clique em "Usuários" → "Novo Técnico" | Formulário: Nome, Username, E-mail, Senha, Confirmar Senha | |
| 02 | Preencha dados válidos com senha de 8+ caracteres → cadastre | `201`; técnico aparece na listagem; snackbar de sucesso | |
| 03 | Tente logar com as credenciais do novo técnico | Login bem-sucedido | |
| 04 | Com o técnico original logado, clique em excluir o técnico novo → confirme | Dialog de confirmação (componente, não `window.confirm`); técnico removido | |

### Casos ruins

| # | Ação | Esperado | ✅/❌ |
|---|---|---|---|
| 05 | Senha com 7 caracteres | Mensagem "Mínimo de 8 caracteres" — Zod bloqueia | |
| 06 | Senhas diferentes nos campos Senha e Confirmar | Mensagem de confirmação — Zod bloqueia | |
| 07 | Username já existente no sistema | Backend retorna `400`; snackbar com detalhe | |
| 08 | E-mail já existente no sistema | Backend retorna `400`; snackbar com detalhe | |
| 09 | Clique em excluir a **própria conta** | Backend retorna `400`; snackbar "Você não pode remover sua própria conta" | |
| 10 | Faça logout do técnico staff → tente acessar `/usuarios` com conta de cliente | Redirecionado — tela de usuários não acessível para não-staff | |

---

## M-10 — Jornada End-to-End Completa

> Execute este bloco depois de validar todos os módulos acima.  
> Simula um ciclo real de análise de solo do laboratório.

| # | Passo | Esperado | ✅/❌ |
|---|---|---|---|
| 01 | Login com técnico válido | Dashboard visível |  |
| 02 | Cadastrar cliente: Código=`E2E-001`, Nome=`Fazenda End to End`, Telefone=`(34) 98888-0001` | Cliente na listagem |  |
| 03 | Criar bateria AA/Ca: V_solo=5, V_extrator=50, Branco=0.002 | Bateria sem curva |  |
| 04 | Adicionar pontos: (0, 0.002), (2, 0.093), (4, 0.181), (6, 0.271) | Curva calculada; R² ≥ 0.999 |  |
| 05 | Ativar a bateria | Chip "Ativa" |  |
| 06 | Criar laudo: cliente `E2E-001`, data de hoje | Código `L-{ano}/N`; redirecionado para edição |  |
| 07 | Criar amostra `{ano}/101`, Ref=`Solo A` | Na tabela, Ativo=Sim |  |
| 08 | Criar amostra `{ano}/102`, Ref=`Solo B` | Na tabela, Ativo=Sim |  |
| 09 | Acessar Amostras → AA / Ca → Carregar | Painel de curva ativa; 2 amostras listadas |  |
| 10 | Preencher `{ano}/101`: FD=5, Leitura=0.213 → Enter | Status "Salvo"; resultado calculado visível |  |
| 11 | Preencher `{ano}/102`: FD=5, Leitura=0.189 → Enter | Status "Salvo" |  |
| 12 | Voltar ao laudo → desativar `{ano}/102` | Toggle "Não"; snackbar "Análise desativada." |  |
| 13 | Abrir detalhe do laudo | "Análises (1 ativa)" com `{ano}/101` listada |  |
| 14 | Clicar "Gerar PDF" | Download com apenas `{ano}/101` no documento |  |
| 15 | Clicar "WhatsApp" | Abre `wa.me/5534988880001?text=...` com mensagem padrão |  |

**Resultado da jornada E2E:** ✅ Completa / ❌ Falhou no passo ___

---

## Como registrar achados

```
[M-XX-NN] Título curto
Módulo   : M-XX — Nome do módulo
Caso     : #NN — descrição do que foi feito
Esperado : comportamento documentado
Obtido   : o que aconteceu de fato
Impacto  : Alto / Médio / Baixo
Situação : Aberto
```

Adicione em `docs/qa/ACHADOS.txt`.
