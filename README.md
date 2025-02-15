# read_api_network

Processo seletivo da Stract!

1- Esta página é a raiz de uma API de dados de contas de anúncios de clientes imaginários. A API possui os seguintes endpoints:
   - /api/platforms
   - /api/accounts?platform={{platform}}
   - /api/fields?platform={{platform}}
   - /api/insights?platform={{platform}}&account={{account}}&token={{token}}&fields={{field1,field2,etc}}

Para acessa-los, continue a utilizar o token de autorização que você recebeu. Se os resultados vierem paginados, as paginas podem ser navegadas através do parâmetro "page".

No dia a dia da Stract precisamos fazer o tratamento de dados como esses e apresenta-los no navegador como relatórios em forma de tabela.
 Primeiramente obtemos uma relação das plataformas disponíveis, em seguida extraímos as contas e campos de cada plataforma.
  Por fim, extraímos os insights relativos aos anúncios de cada conta.

2- Seu objetivo será escrever um servidor local que consuma os dados desta API e entregue os relatórios especificados abaixo.
 Os relatórios devem ser gerados em tempo real e apresentados em formato CSV com seus devidos cabeçalhos. 
 Os relatórios deve ser acessíveis a partir dos seguintes endpoints:
   - /
   - /{{plataforma}}
   - /{{plataforma}}/resumo
   - /geral
   - /geral/resumo

A raiz da sua API deve retornar seu nome, email e o link para o seu LinkedIn (se tiver).

O endpoint "/{{plataforma}}" deve retornar uma tabela em que cada linha represente um anúncio veiculado na plataforma indicada. As colunas devem trazer todos os campos de insights daquele anúncio, bem como o nome da conta que o está veiculando. Em nenhuma das tabelas precisam ser retornados IDs, mas é importante observar que o nome não é um identificador único. Exemplo:

Platform,Ad Name,Clicks,...
Facebook,Some Ad,10,...
Facebook,Other Ad,20,...
YouTube,One More Ad,5,...

O endpoint "/{{plataforma}}/resumo" deve trazer uma tabela similar, mas colapsando em uma única linha todas as linhas que forem da mesma conta, ficando apenas uma linha para cada conta. Os dados devem ser somados nas colunas numéricas e, nas colunas que tem texto, os dados podem ficar vazios (exceto o nome da conta, que é o mesmo para todas as linhas agregadas da conta em questão). Exemplo:

Platform,Ad Name,Clicks,...
Facebook,,30,...
YouTube,,5,...

O endpoint "/geral" deve trazer todos os anúncios de todas as plataformas. Nesse relatório devem ser adicionadas colunas para identificar por nome a plataforma na qual o anúncio está sendo veiculado, além do nome conta que esta veiculando o anúncio. 
Devem haver colunas para todos os campos existentes na API. Campos de diferentes plataformas que possuam o mesmo nome podem ser apresentados na mesma coluna, isto é, uma mesma coluna pode (mas não necessariamente deve) ser aproveitada pelas mesmas plataformas. O campo pode ficar vazio nas linhas das plataformas nas quais ele não exista. Uma exceção é o campo "Cost per Click", que não está disponível para esta API no Google Analytics, porém pode ser calculado dividindo-se o valor de "spend" pelo valor de "clicks".

O endpoint "/geral/resumo" deve trazer uma tabela similar, mas colapsando em uma única linha todas as linhas que forem da mesma plataforma. Caso as colunas seja numéricas, os dados devem ser somados. Caso sejam texto, a coluna pode ficar vazia na linha em questão (exceto nome da plataforma, que é o mesmo para todas as linhas agregadas da plataforma em questão).

O programa deve ser implementado em Python+Flask, com o mínimo de dependências possíveis. Os endpoints devem ter como raiz o localhost na porta padrão e serem publicamente acessíveis através de um GET. Seu código, bem como o README de instalação, deve ser colocado em um repositório público (sugerimos o GitHub), cujo link deve ser submetido no form do processo seletivo. É parte do seu trabalho explorar e entender a API, inclusive suas peculiaridades, contando apenas com a documentação mínima apresentada acima.

Boa sorte!


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