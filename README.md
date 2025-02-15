# read_api_network

## Processo seletivo da Stract!

# Resolução

# API de Insights Publicitários

Esta API fornece relatórios sobre anúncios publicitários veiculados em diferentes plataformas, consolidando dados de performance e permitindo a extração de relatórios em formato CSV.

## 🚀 Tecnologias Utilizadas
- **Python** 3.9+
- **Flask** - Framework para APIs
- **Pandas** - Manipulação e agregação de dados
- **Poetry** - Gerenciamento de dependências
- **Requests** - Consumo de APIs externas

## 📂 Estrutura do Projeto
```
├── api/
│   ├── candidate.py              # Rota para dados do candidato
│   ├── plataforma.py             # Rotas para os dados das plataformas
│   ├── process_data_request.py   # Funções para prepara as requisições para api externa
│   ├── __init__.py               # Inicialização do Flask
├── core/
|   ├── plataforms_api.py # Faz as requisições para api externa
├── repo/  
|   ├── parser.py         # Parse/formatação/Lógica de agregação dos dados
├── pyproject.toml        # Gerenciamento de dependências (Poetry)
├── README.md             # Documentação
```

## 🔧 Instalação e Configuração
### 1️⃣ Clonar o Repositório
```bash
https://github.com/MieleSantos/read_api_network.git
cd read_api_network
```

### 2️⃣ Instalar Dependências
Usando **Poetry**:
```bash
poetry install
```
#### Crie um arquivo .env na raiz do projeto com os campos:
```bash
TOKEN=token de acesso
URL_BASE=https://sidebar.stract.to/api
```
### 3️⃣ Rodar a API

#### Habilite o ambiente virtual

```bash
poetry shell
```
#### Execute
```bash
flask --app api run
```
A API estará disponível em **http://127.0.0.1:5000/**

## 📌 Endpoints

### Obter dados do candidato
```http
GET http://127.0.0.1:5000/
```
### Obter dados da plataforma, pode ser ga4, tiktok_insights, meta_ads

```http
GET http://127.0.0.1:5000/meta_ads
```
### Obter resumo dos dados da plataforma, pode ser ga4, tiktok_insights, meta_ads
```http
GET http://127.0.0.1:5000/meta_ads/resumo
```
### Obter dados gerais das plataformas

```http
GET http://127.0.0.1:5000/geral
```
### Obter dados gerais das plataformas de forma resumida
```http
GET http://127.0.0.1:5000/geral/resumo
```

As requisições vão retorna dados em formato dataframe/tabula