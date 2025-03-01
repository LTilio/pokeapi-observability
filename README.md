# PokeAPI Observability

Este projeto é uma API FastAPI que busca dados de Pokémon na PokéAPI e os armazena em um banco de dados PostgreSQL.

## 🎯 Observabilidade
Este projeto já está instrumentado com OpenTelemetry. Os traces, logs e métricas serão enviados para os serviços configurados. Você pode visualizar os dados no Grafana ou outra ferramenta conectada ao OpenTelemetry.


## 📌 Pré-requisitos
Antes de iniciar, certifique-se de ter os seguintes softwares instalados:
- Docker 
- Git 

## 🏗️ Passo a passo para rodar o projeto

### 1️⃣ Clonar o repositório
```sh
 git clone https://github.com/LTilio/pokeapi-observability.git
```
```sh
cd pokeapi-observability
```
### 2️⃣ Criar o arquivo .env
Antes de rodar o projeto, crie um arquivo .env na raiz do projeto usando o .env.EXAMPLE como base

### 3️⃣ Criar a rede Docker (se ainda não existir)
```sh
docker network create sentinel
```

### 4️⃣ Construir e subir os containers
```sh
docker compose up --build -d
```
Isso irá:
- Criar o container do banco de dados PostgreSQL
- Criar o container da aplicação FastAPI
- Configurar a instrumentação com OpenTelemetry

### 5️⃣ Acessar a API
A API estará rodando em `http://localhost:8001`

### 6️⃣ Documentação Interativa (Swagger UI)
A documentação interativa do FastAPI pode ser acessada em:
```sh
http://localhost:8001/docs
```

### 7️⃣ Para visualizar os logs
Caso precise visualizar os logs da aplicação, utilize:
```sh
docker logs -f PokeApi_observability
```

### 8️⃣ Para parar os containers
Se precisar parar a aplicação, execute:
```sh
docker compose down
```

## 🔥 Endpoints Disponíveis

### ✅ Testar conexão com a API
```http
GET /ping
```
Retorna:
```json
{"ping": "pong"}
```

### 🔍 Buscar um Pokémon na PokéAPI
```http
GET /pokemon/{id}
```
Exemplo:
```sh
GET http://localhost:8001/pokemon/1
```

### 💾 Salvar um Pokémon no banco de dados
```http
POST /pokemon/{id}
```
Exemplo:
```sh
POST http://localhost:8001/pokemon/1
```

## 📝 Observações
- O banco de dados roda na porta `5433`.
- A API roda na porta `8001`.
- Os dados do PostgreSQL não são persistidos após `docker compose down`.
- OpenTelemetry já está configurado para capturar logs, métricas e traces.





