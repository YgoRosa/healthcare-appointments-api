#!/bin/sh

# Failsafe: Para o script imediatamente se qualquer comando falhar
set -e

echo "Aguardando o banco de dados PostgreSQL..."

# Usando o próprio Python para tentar abrir uma conexão de rede com o banco na porta 5432
python << END
import socket
import time
import os

port = int(os.environ.get("DB_PORT", 5432))
host = os.environ.get("DB_HOST", "db")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error:
        time.sleep(1)
END

echo "PostgreSQL está pronto!"

# Executa as migrations automaticamente
echo "Aplicando migrações do banco de dados..."
python manage.py migrate

echo "Verificando/Criando superusuário de testes..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@email.com', 'admin123')"

# Executa o comando principal que foi passado no CMD do Dockerfile ou no Compose
exec "$@"