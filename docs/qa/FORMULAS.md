# Fórmulas do LABAS — Validação por Aparelho

> Extraídas diretamente do código-fonte em 2026-08-05.  
> Arquivos de referência: `core_matematico.py`, `absorcao_atomica.py`, `espectrofotometro.py`,  
> `fotometro_chama.py`, `phmetro.py`, `titulacao.py`, `signals.py`, `use_cases.py`.

---

## 0 — Curva de Calibração (usada por AA, FC, ES)

> **Arquivo:** `core_matematico.py` — `CurvaRegressaoLinear`  
> Mínimo de **2 pontos** para calcular a curva. Com 1 ponto: curva nula.  
> X = concentrações dos padrões · Y = leituras (absorbância / emissão)

### Coeficiente angular `a` (inclinação)

```
a = (n·Σxy − Σx·Σy) / (n·Σx² − (Σx)²)
```

### Intercepto `b`

```
b = (Σy − a·Σx) / n
```

### Coeficiente de determinação R²

```
SS_res = Σ (y − (ax + b))²
SS_tot = Σ (y − ȳ)²

R² = 1 − SS_res / SS_tot
```

> Se SS_tot = 0 → R² = 1 (todos os pontos Y são idênticos).

### Equação da reta

```
y = ax + b
```

### Inversão para isolar a concentração

```
x = (y − b) / a
```

> Usado em AA, FC, ES (P-Mehlich, P-Resina, S) para obter concentração no extrato a partir da leitura do aparelho.

---

## 1 — Absorção Atômica (AA)

> **Arquivo:** `absorcao_atomica.py`  
> **Elementos:** Ca, Mg, Cu, Fe, Mn, Zn  
> **Unidades:** Ca e Mg → cmolc/dm³ · Cu, Fe, Mn, Zn → mg/dm³

### Passo 1 — Descontar o branco

```
Leitura corrigida = Leitura bruta − Leitura branco
```

### Passo 2 — Concentração no extrato

```
C_extrato = (Leitura corrigida − b) / a
```

### Passo 3 — Disponível no solo

```
Resultado = C_extrato × V_extrator × Fator_diluição / 1000 / PE / V_solo
```

### Pesos equivalentes (PE)

| Elemento | PE   | Unidade resultado |
|----------|------|-------------------|
| Ca       | 200  | cmolc/dm³         |
| Mg       | 120  | cmolc/dm³         |
| Cu       | 1    | mg/dm³            |
| Fe       | 1    | mg/dm³            |
| Mn       | 1    | mg/dm³            |
| Zn       | 1    | mg/dm³            |

### Exemplo de cálculo (Ca)

```
Parâmetros: a=0,45 · b=0,003 · branco=0,002 · V_extrator=50 mL · FD=5 · V_solo=5 cm³

Leit. corrigida = 0,213 − 0,002 = 0,211
C_extrato       = (0,211 − 0,003) / 0,45 = 0,4622...
Resultado (Ca)  = 0,4622 × 50 × 5 / 1000 / 200 / 5 = 0,000115... cmolc/dm³
```

> **Arredondamento:** 2 casas decimais (padrão de laboratório).

---

## 2 — Espectrofotômetro (ES)

> **Arquivo:** `espectrofotometro.py`  
> A leitura do aparelho é **Transmitância (T%)**.  
> Todos os elementos ES passam pela conversão óptica abaixo — **exceto MO** que usa fórmula fixa.

### Conversão óptica — Lei de Beer-Lambert

```
Absorbância = 2 − log₁₀(T%)
```

> T% deve ser > 0. Se T% ≤ 0, a curva é invalidada pelo backend.

---

### 2.1 — Matéria Orgânica (MO)

> **Fórmula fixa — não usa curva de calibração.**

```
Abs = 2 − log₁₀(T%)
MO  = (Abs + 0,0136) / 0,0729
```

**Unidade:** g/dm³ (ou %)

---

### 2.2 — Fósforo Mehlich (P-Mehlich)

```
Abs      = 2 − log₁₀(T%)
C_extrato = (Abs − b) / a
Resultado = C_extrato × V_extrator × Fator_diluição / 1000 / V_solo
```

**Unidade:** mg/dm³

---

### 2.3 — Fósforo Remanescente (P-rem)

> Não usa V_solo. Usa um **Fator Coluna E** que concentra volume extrator + diluição + outros.  
> Equivalência no Excel: `=(Abs − b) / a × E`

```
Abs         = 2 − log₁₀(T%)
C_extrato    = (Abs − b) / a
Resultado    = C_extrato × Fator_coluna_E
```

**Unidade:** mg/L

---

### 2.4 — Fósforo Resina (P-Resina)

> Mesma estrutura do P-Mehlich.

```
Abs      = 2 − log₁₀(T%)
C_extrato = (Abs − b) / a
Resultado = C_extrato × V_extrator × Fator_diluição / 1000 / V_solo
```

**Unidade:** mg/dm³

---

### 2.5 — Enxofre (S)

```
Abs      = 2 − log₁₀(T%)
C_extrato = (Abs − b) / a
Resultado = C_extrato × V_extrator × Fator_diluição / 1000 / V_solo
```

**Unidade:** mg/dm³

---

### 2.6 — Boro (B)

> **Atenção:** Boro **não desconta o intercepto `b`** — divide a absorbância diretamente por `a`.

```
Abs      = 2 − log₁₀(T%)
C_extrato = Abs / a          ← sem subtrair b
Resultado = C_extrato × V_extrator × Fator_diluição / 1000 / V_solo
```

**Unidade:** mg/dm³

---

## 3 — Fotômetro de Chama (FC)

> **Arquivo:** `fotometro_chama.py`  
> **Elementos:** K (Potássio), Na (Sódio)  
> Leitura de **emissão direta** — sem conversão óptica logarítmica.

```
C_extrato = (Leitura_emissão − b) / a
Resultado = C_extrato × V_extrator × Fator_diluição / 1000 / V_solo
```

**Unidade:** mg/dm³ (K e Na)

---

## 4 — pHmetro (PH)

> **Arquivo:** `phmetro.py`  
> **Elementos:** ph_agua, ph_cacl2, ph_kcl  
> Leitura **direta** — o valor do visor vai direto para o laudo.

```
Resultado = Leitura bruta    (sem cálculo)
```

### Validação de faixa

```
0 ≤ pH ≤ 14     (escala química completa)
Solos normais: 3 a 9
```

> Valores fora de 0–14 são rejeitados com erro de digitação.

---

## 5 — Titulação (TI)

> **Arquivo:** `titulacao.py`  
> **Elementos:** Al³⁺ (Alumínio Trocável), H+Al (Acidez Potencial)

```
Resultado = Leitura_amostra − Leitura_branco
```

### Trava agronômica

```
Se Resultado < 0 → Resultado = 0
(Não existe alumínio ou acidez potencial negativa no solo)
```

**Unidade:** cmolc/dm³

---

## 6 — Relações Agronômicas (calculadas automaticamente)

> **Arquivo:** `use_cases.py` — `CalculadoraAnaliseSolo`  
> Executadas via signal `pre_save` de `AnaliseSolo` sempre que Ca, Mg ou K são atualizados.  
> **Campos nulos são tratados como 0** no cálculo.

### 6.1 — Conversão de K

```
K (cmolc/dm³) = K (mg/dm³) / 390
```

### 6.2 — Soma de Bases (SB)

```
SB = K_cmolc + Ca + Mg
```

**Unidade:** cmolc/dm³ · Precisão: 2 casas decimais

### 6.3 — CTC Efetiva (t)

```
t = SB + Al
```

**Unidade:** cmolc/dm³ · Precisão: 2 casas decimais

### 6.4 — CTC a pH 7 (T)

```
T = SB + H+Al
```

**Unidade:** cmolc/dm³ · Precisão: 2 casas decimais

### 6.5 — Saturação por Bases (V%)

```
V% = (SB / T) × 100    [se T > 0]
V% = 0                  [se T = 0]
```

**Precisão:** 1 casa decimal

### 6.6 — Saturação por Alumínio (m%)

```
m% = (Al / t) × 100    [se t > 0]
m% = 0                  [se t = 0]
```

**Precisão:** 1 casa decimal

### 6.7 — Relações catônicas

```
Ca/Mg = Ca / Mg         [se Mg > 0, senão 0]
Ca/K  = Ca / K_cmolc    [se K > 0, senão 0]
Mg/K  = Mg / K_cmolc    [se K > 0, senão 0]
```

**Precisão:** 2 casas decimais

### 6.8 — Carbono Orgânico (C.org)

```
C.org = MO / 1,72
```

**Precisão:** 2 casas decimais

---

## Resumo — O que cada aparelho fornece ao laudo

| Aparelho | Elemento | Campo no laudo | Unidade |
|---|---|---|---|
| AA | Ca | `ca` | cmolc/dm³ |
| AA | Mg | `mg` | cmolc/dm³ |
| AA | Cu | `cu` | mg/dm³ |
| AA | Fe | `fe` | mg/dm³ |
| AA | Mn | `mn` | mg/dm³ |
| AA | Zn | `zn` | mg/dm³ |
| ES | MO | `mo` | g/dm³ |
| ES | P-Mehlich | `p_m` | mg/dm³ |
| ES | P-rem | `p_rem` | mg/L |
| ES | P-Resina | `p_r` | mg/dm³ |
| ES | S | `s` | mg/dm³ |
| ES | B | `b` | mg/dm³ |
| FC | K | `k` | mg/dm³ |
| FC | Na | `na` | mg/dm³ |
| PH | ph_agua | `ph_agua` | — |
| PH | ph_cacl2 | `ph_cacl2` | — |
| PH | ph_kcl | `ph_kcl` | — |
| TI | Al | `al` | cmolc/dm³ |
| TI | H+Al | `h_al` | cmolc/dm³ |
| — | SB (calculado) | `sb` | cmolc/dm³ |
| — | t / CTC efetiva | `t` | cmolc/dm³ |
| — | T / CTC pH7 | `T_maiusculo` | cmolc/dm³ |
| — | V% | `V` | % |
| — | m% | `m` | % |
| — | Ca/Mg | `ca_mg` | — |
| — | Ca/K | `ca_k` | — |
| — | Mg/K | `mg_k` | — |
| — | C.org | `c_org` | % |
