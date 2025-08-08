#!/bin/bash

# Script de backup automático para o projeto New Life
# Uso: ./backup.sh [nome_do_backup]

# Configurações
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME=${1:-"backup_$DATE"}

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Função para fazer backup
do_backup() {
    echo "Iniciando backup do banco de dados..."
    
    # Verificar se os containers estão rodando
    if ! docker-compose ps | grep -q "newlife_postgres.*Up"; then
        echo "Erro: Container do PostgreSQL não está rodando!"
        exit 1
    fi
    
    # Fazer backup
    docker-compose exec -T db pg_dump -U newlife_user newlife_db > "$BACKUP_DIR/$BACKUP_NAME.sql"
    
    if [ $? -eq 0 ]; then
        echo "✅ Backup criado com sucesso: $BACKUP_DIR/$BACKUP_NAME.sql"
        
        # Comprimir backup
        gzip "$BACKUP_DIR/$BACKUP_NAME.sql"
        echo "✅ Backup comprimido: $BACKUP_DIR/$BACKUP_NAME.sql.gz"
        
        # Mostrar tamanho do arquivo
        echo "📊 Tamanho do backup: $(du -h "$BACKUP_DIR/$BACKUP_NAME.sql.gz" | cut -f1)"
        
        # Limpar backups antigos (manter apenas os últimos 7 dias)
        find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
        echo "🧹 Backups antigos removidos (mais de 7 dias)"
        
    else
        echo "❌ Erro ao criar backup!"
        exit 1
    fi
}

# Função para restaurar backup
restore_backup() {
    local backup_file=$1
    
    if [ -z "$backup_file" ]; then
        echo "Uso: $0 restore <arquivo_backup>"
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        echo "❌ Arquivo de backup não encontrado: $backup_file"
        exit 1
    fi
    
    echo "⚠️  ATENÇÃO: Isso irá sobrescrever o banco de dados atual!"
    read -p "Tem certeza que deseja continuar? (y/N): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo "Restaurando backup: $backup_file"
        
        # Se o arquivo estiver comprimido, descomprimir
        if [[ $backup_file == *.gz ]]; then
            gunzip -c "$backup_file" | docker-compose exec -T db psql -U newlife_user -d newlife_db
        else
            docker-compose exec -T db psql -U newlife_user -d newlife_db < "$backup_file"
        fi
        
        if [ $? -eq 0 ]; then
            echo "✅ Backup restaurado com sucesso!"
        else
            echo "❌ Erro ao restaurar backup!"
            exit 1
        fi
    else
        echo "Operação cancelada."
    fi
}

# Função para listar backups
list_backups() {
    echo "📋 Backups disponíveis:"
    if [ -d "$BACKUP_DIR" ] && [ "$(ls -A $BACKUP_DIR)" ]; then
        ls -lh $BACKUP_DIR/*.sql.gz 2>/dev/null | while read line; do
            echo "  $line"
        done
    else
        echo "  Nenhum backup encontrado."
    fi
}

# Menu principal
case "${1:-backup}" in
    "backup")
        do_backup
        ;;
    "restore")
        restore_backup "$2"
        ;;
    "list")
        list_backups
        ;;
    "help"|"-h"|"--help")
        echo "Uso: $0 [comando] [opções]"
        echo ""
        echo "Comandos:"
        echo "  backup [nome]     - Criar backup (padrão)"
        echo "  restore <arquivo>  - Restaurar backup"
        echo "  list              - Listar backups disponíveis"
        echo "  help              - Mostrar esta ajuda"
        echo ""
        echo "Exemplos:"
        echo "  $0                    # Criar backup com nome automático"
        echo "  $0 backup meu_backup  # Criar backup com nome específico"
        echo "  $0 restore backup.sql # Restaurar backup"
        echo "  $0 list              # Listar backups"
        ;;
    *)
        echo "Comando inválido. Use '$0 help' para ver as opções."
        exit 1
        ;;
esac
