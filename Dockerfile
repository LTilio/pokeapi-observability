# Usa uma imagem base do Python
FROM python:3.13-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock* ./

# Instala o Poetry
RUN pip install poetry

# Instala todas as dependências, incluindo as de desenvolvimento
RUN poetry install --no-root 

# Instala a instrumentação do OpenTelemetry
RUN poetry run poe otel-install

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta usada pela aplicação
EXPOSE 8001

# Define o ambiente carregando variáveis do `.env`
ENV $(cat .env | xargs)

# Comando para rodar a API com OpenTelemetry
CMD ["poetry", "run", "poe", "serve"]
