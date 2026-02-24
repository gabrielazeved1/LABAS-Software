# LABAS-Software - Backend

## Sobre o Projeto

O LABAS é um sistema desenvolvido como Projeto de Extensão em parceria com o curso de Agronomia da Universidade Federal de Uberlândia (UFU).

O objetivo principal da aplicacao e modernizar, otimizar e automatizar as operacoes laboratoriais voltadas para o agronegocio, especificamente no controle e analise de nutrientes do solo e de sementes. O software foi projetado para substituir o uso de planilhas manuais, oferecendo uma infraestrutura robusta para o cadastro de amostras, modelagem de dados relacionais e a geracao automatizada de laudos tecnicos.

## Tecnologias e Arquitetura

Este repositorio contem o codigo-fonte do Back-End da aplicacao, desenvolvido com foco em escalabilidade e boas praticas de engenharia de software (POO).

- **Linguagem:** Python 3.11
- **Framework:** Django 5.2
- **Banco de Dados:** PostgreSQL (Producao) / SQLite (Ambiente de Desenvolvimento)
- **Gerenciamento de Dependencias:** Poetry
- **Sistema Operacional Base de Desenvolvimento:** macOS

## Guia de Execucao Local

Este guia descreve os passos necessarios para configurar e rodar o ambiente de desenvolvimento em sua maquina local.

### 1. Preparacao do Ambiente

Como o projeto utiliza o gerenciador de pacotes Poetry, a ativacao do ambiente virtual (venv) ocorre de forma automatizada. No terminal, navegue ate o diretorio `backend/` e execute:

```bash
# Instalar todas as dependencias do projeto
poetry install

# Sincronizar e aplicar as migracoes no Banco de Dados
poetry run python manage.py migrate

```

### 2. Inicializacao do Sistema

Apos a instalacao e configuracao do banco de dados, inicie o servidor de desenvolvimento:

```bash
# Rodar o servidor local
poetry run python manage.py runserver

```

**Acesso Administrativo:** O painel pode ser acessado em `http://127.0.0.1:8000/admin/`
