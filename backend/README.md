# LABAS-Software - Guia de Retomada (Backend)

**Ambiente:** macOS | Python 3.11 | Poetry | Django 5.2

---

## 1. Preparação do Motor

Como você usa Poetry, não precisa ativar o venv manualmente se usar o `run`. Rode na pasta `backend/`:

```bash
# Instalar dependências (caso mude de máquina)
poetry install

# Sincronizar o Banco (SQLite)
# Você já resolveu as renomeações, mas é bom garantir:
poetry run python manage.py migrate
```

---

## 2. Subindo o Sistema

```bash
# Rodar o servidor de desenvolvimento
poetry run python manage.py runserver
```

**Acesso:** http://127.0.0.1:8000/admin/

---
