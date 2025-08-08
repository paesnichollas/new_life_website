#!/bin/bash

# Função para executar migrações
run_migrations() {
    echo "Executando migrações..."
    python manage.py migrate
}

# Função para coletar arquivos estáticos
collect_static() {
    echo "Coletando arquivos estáticos..."
    python manage.py collectstatic --noinput
}

# Função para criar superusuário se não existir
create_superuser() {
    echo "Verificando superusuário..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuário criado: admin/admin123')
else:
    print('Superusuário já existe')
"
}

# Executar migrações
run_migrations

# Coletar arquivos estáticos
collect_static

# Criar superusuário (apenas em desenvolvimento)
if [ "$DEBUG" = "True" ]; then
    create_superuser
fi

# Iniciar servidor
echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
