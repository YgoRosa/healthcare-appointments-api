# 1. Imagem base oficial do Python (versão estável e leve)
FROM python:3.11-slim

# 2. Define variáveis de ambiente para o Python rodar otimizado no container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define a pasta de trabalho dentro do container
WORKDIR /app

# 4. Instala as dependências do sistema necessárias para compilar o PostgreSQL (psycopg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Instala o Poetry
RUN pip install --no-cache-dir poetry

# 6. Copia apenas os arquivos de dependências primeiro (otimiza o cache do Docker)
COPY pyproject.toml poetry.lock /app/

# 7. Configura o Poetry para NÃO criar ambiente virtual dentro do container e instala as dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# 8. Copia o restante do código do projeto para dentro do container
COPY . /app/

# 9. Porta que o Django vai expor dentro do container
EXPOSE 8000

# 10. Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]