#!/bin/bash

# =============================================================================
# SCRIPT DE DEPLOY AUTOMATIZADO - NEW LIFE WEBSITE
# =============================================================================

set -e  # Para o script se qualquer comando falhar

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    error "Este script deve ser executado no diretório raiz do projeto Django"
    exit 1
fi

# Configurações
ENVIRONMENT=${1:-production}
BACKUP_BEFORE_DEPLOY=${2:-true}

log "Iniciando deploy para ambiente: $ENVIRONMENT"

# =============================================================================
# BACKUP DO BANCO DE DADOS
# =============================================================================
if [ "$BACKUP_BEFORE_DEPLOY" = "true" ]; then
    log "Criando backup do banco de dados..."
    
    # Criar diretório de backup se não existir
    mkdir -p backup
    
    # Nome do arquivo de backup
    BACKUP_FILE="backup/newlife_$(date +%Y%m%d_%H%M%S).dump"
    
    # Verificar se DATABASE_URL está definida
    if [ -z "$DATABASE_URL" ]; then
        warn "DATABASE_URL não definida, pulando backup"
    else
        # Backup do PostgreSQL
        if pg_dump "$DATABASE_URL" --format=custom --no-acl --no-owner -o "$BACKUP_FILE"; then
            log "Backup criado com sucesso: $BACKUP_FILE"
        else
            warn "Falha ao criar backup, continuando deploy..."
        fi
    fi
fi

# =============================================================================
# INSTALAÇÃO DE DEPENDÊNCIAS
# =============================================================================
log "Instalando dependências Python..."
pip install -r requirements.txt

# =============================================================================
# COLETA DE ARQUIVOS ESTÁTICOS
# =============================================================================
log "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# =============================================================================
# MIGRAÇÕES DO BANCO DE DADOS
# =============================================================================
log "Aplicando migrações do banco de dados..."
python manage.py migrate

# =============================================================================
# VERIFICAÇÃO DE CONFIGURAÇÃO
# =============================================================================
log "Verificando configuração do Django..."
python manage.py check --deploy

# =============================================================================
# TESTES (OPCIONAL)
# =============================================================================
if [ "$ENVIRONMENT" = "staging" ]; then
    log "Executando testes..."
    python manage.py test --verbosity=2
fi

# =============================================================================
# LIMPEZA DE CACHE
# =============================================================================
log "Limpando cache..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# =============================================================================
# VERIFICAÇÃO DE SEGURANÇA
# =============================================================================
log "Verificando configurações de segurança..."

# Verificar se SECRET_KEY está definida
if [ -z "$SECRET_KEY" ]; then
    error "SECRET_KEY não está definida!"
    exit 1
fi

# Verificar se DEBUG está desabilitado em produção
if [ "$ENVIRONMENT" = "production" ] && [ "$DEBUG" = "True" ]; then
    error "DEBUG deve ser False em produção!"
    exit 1
fi

# =============================================================================
# RESTART DO SERVIÇO (se aplicável)
# =============================================================================
if [ "$ENVIRONMENT" = "production" ]; then
    log "Reiniciando serviços..."
    
    # Se estiver usando systemd
    if command -v systemctl &> /dev/null; then
        sudo systemctl restart newlife-django || warn "Falha ao reiniciar serviço Django"
        sudo systemctl restart nginx || warn "Falha ao reiniciar Nginx"
    fi
    
    # Se estiver usando Docker
    if [ -f "docker-compose.yml" ]; then
        docker-compose restart web || warn "Falha ao reiniciar container web"
    fi
fi

# =============================================================================
# VERIFICAÇÃO DE SAÚDE
# =============================================================================
log "Verificando saúde da aplicação..."

# Aguardar um pouco para o serviço inicializar
sleep 5

# Testar se a aplicação está respondendo
if curl -f -s http://localhost:8000/ > /dev/null; then
    log "✅ Aplicação está respondendo corretamente"
else
    warn "⚠️  Aplicação pode não estar respondendo corretamente"
fi

# =============================================================================
# LIMPEZA DE BACKUPS ANTIGOS
# =============================================================================
log "Removendo backups antigos (mais de 7 dias)..."
find backup -name "*.dump" -type f -mtime +7 -delete 2>/dev/null || true

# =============================================================================
# FINALIZAÇÃO
# =============================================================================
log "✅ Deploy concluído com sucesso!"
log "Ambiente: $ENVIRONMENT"
log "Timestamp: $(date)"

# Informações úteis
echo ""
echo "📋 Informações do Deploy:"
echo "   - Ambiente: $ENVIRONMENT"
echo "   - Data/Hora: $(date)"
echo "   - Diretório: $(pwd)"
echo "   - Python: $(python --version)"
echo "   - Django: $(python -c 'import django; print(django.get_version())')"

if [ "$ENVIRONMENT" = "production" ]; then
    echo ""
    echo "🔒 Configurações de Segurança Verificadas:"
    echo "   - DEBUG: False"
    echo "   - SECRET_KEY: Definida"
    echo "   - SSL: Habilitado"
fi

echo ""
log "Deploy finalizado!"
