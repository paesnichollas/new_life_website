#!/bin/bash

# Script para gerenciar containers Docker do projeto New Life

DOCKER_CMD='"/c/Program Files/Docker/Docker/resources/bin/docker.exe"'

case "$1" in
    "start")
        echo "Iniciando containers..."
        eval $DOCKER_CMD compose up -d
        echo "Containers iniciados!"
        ;;
    "stop")
        echo "Parando containers..."
        eval $DOCKER_CMD compose down
        echo "Containers parados!"
        ;;
    "restart")
        echo "Reiniciando containers..."
        eval $DOCKER_CMD compose down
        eval $DOCKER_CMD compose up -d
        echo "Containers reiniciados!"
        ;;
    "logs")
        echo "Mostrando logs do Django..."
        eval $DOCKER_CMD logs -f newlife_django
        ;;
    "build")
        echo "Construindo containers..."
        eval $DOCKER_CMD compose build
        echo "Containers construídos!"
        ;;
    "status")
        echo "Status dos containers:"
        eval $DOCKER_CMD ps
        ;;
    "shell")
        echo "Abrindo shell no container Django..."
        eval $DOCKER_CMD exec -it newlife_django /bin/bash
        ;;
    "migrate")
        echo "Executando migrações..."
        eval $DOCKER_CMD exec newlife_django python manage.py migrate
        ;;
    "collectstatic")
        echo "Coletando arquivos estáticos..."
        eval $DOCKER_CMD exec newlife_django python manage.py collectstatic --noinput
        ;;
    "createsuperuser")
        echo "Criando superusuário..."
        eval $DOCKER_CMD exec -it newlife_django python manage.py createsuperuser
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|logs|build|status|shell|migrate|collectstatic|createsuperuser}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  start           - Inicia os containers"
        echo "  stop            - Para os containers"
        echo "  restart         - Reinicia os containers"
        echo "  logs            - Mostra logs do Django"
        echo "  build           - Reconstrói os containers"
        echo "  status          - Mostra status dos containers"
        echo "  shell           - Abre shell no container Django"
        echo "  migrate         - Executa migrações"
        echo "  collectstatic   - Coleta arquivos estáticos"
        echo "  createsuperuser - Cria superusuário"
        exit 1
        ;;
esac
