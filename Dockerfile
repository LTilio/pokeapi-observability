# Usa uma imagem base do Python
FROM python:3.13-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock* ./

# Instala o Poetry e configura para não usar ambiente virtual
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Instala todas as dependências, incluindo as de desenvolvimento
RUN poetry install --with dev --no-root

# Instala as dependências do OpenTelemetry
RUN opentelemetry-bootstrap -a install

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta usada pela aplicação
EXPOSE 8001

# Comando para rodar a aplicação instrumentada com OpenTelemetry
CMD ["opentelemetry-instrument", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8001"]