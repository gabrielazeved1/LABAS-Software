# 🚜 LABAS-Software - Guia de Retomada (Backend)

**Ambiente:** macOS | Python 3.11 | Poetry | Django 5.2

---

## 🛠 1. Preparação do Motor

Como você usa Poetry, não precisa ativar o venv manualmente se usar o `run`. Rode na pasta `backend/`:

```bash
# Instalar dependências (caso mude de máquina)
poetry install

# Sincronizar o Banco (SQLite)
# Você já resolveu as renomeações, mas é bom garantir:
poetry run python manage.py migrate
```

---

## 🚀 2. Subindo o Sistema

Para ver o Admin e testar os novos campos (`sb`, `t`, `T_maiusculo`, `p_m`...):

```bash
# Rodar o servidor de desenvolvimento
poetry run python manage.py runserver
```

**Acesso:** http://127.0.0.1:8000/admin/

---

## 📂 3. Mapa de Arquivos (Clean Architecture)

Sua estrutura atual que confirmamos no `find`:

| Caminho                                 | Função                                                         |
| --------------------------------------- | -------------------------------------------------------------- |
| `src/application/use_cases.py`          | **Calculadora**                                                |
| `src/application/constants.py`          | **Limites de Interpretação**                                   |
| `src/infrastructure/database/models.py` | Onde os campos foram **renomeados** para bater com as fórmulas |

---

## ⚠️ 4. Comandos de Emergência (Baseado no seu Log)

Se você alterar algum campo no `models.py` e der erro de `FieldError`:

```bash
# 1. Gerar migração
# O Django vai perguntar sobre 'rename' — responda 'y'
poetry run python manage.py makemigrations database

# 2. Aplicar
# Dê o valor default '0' se ele pedir para campos não-nulos
poetry run python manage.py migrate
```

---

## 📝 Resumo do que **Fechamos** hoje:

✅ **Refatoração de Banco**  
Você limpou o `models.py`. Saiu o "português extenso" e entraram as **siglas técnicas da sua planilha** (`sb`, `h_al`, `ca_mg`, `c_org`).

✅ **Cérebro Prático**  
O arquivo `use_cases.py` já reflete o **divisor 390 do Potássio** e o **1.72 do Carbono**.

✅ **Superuser**  
Já está criado. Você passou pela validação de senha e o **Admin está liberado**.

---
