#!/usr/bin/env python3
"""
Utilitários para o projeto New Life Website
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

def check_environment():
    """Verifica se o ambiente está configurado corretamente"""
    print("🔍 Verificando ambiente...")
    
    # Verificar variáveis de ambiente críticas
    critical_vars = ['SECRET_KEY', 'DEBUG']
    missing_vars = []
    
    for var in critical_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis de ambiente faltando: {', '.join(missing_vars)}")
        return False
    
    # Verificar se o banco está acessível
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Banco de dados acessível")
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False
    
    # Verificar arquivos estáticos
    static_root = settings.STATIC_ROOT
    if not os.path.exists(static_root):
        print(f"⚠️  Diretório de arquivos estáticos não existe: {static_root}")
    else:
        print("✅ Arquivos estáticos configurados")
    
    print("✅ Ambiente verificado com sucesso!")
    return True

def backup_database():
    """Cria backup do banco de dados"""
    print("💾 Criando backup do banco...")
    
    # Criar diretório de backup
    backup_dir = Path("backup")
    backup_dir.mkdir(exist_ok=True)
    
    # Nome do arquivo de backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"newlife_{timestamp}.json"
    
    try:
        # Exportar dados como JSON
        from django.core.management import call_command
        from io import StringIO
        
        output = StringIO()
        call_command('dumpdata', stdout=output, indent=2)
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(output.getvalue())
        
        print(f"✅ Backup criado: {backup_file}")
        return str(backup_file)
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return None

def restore_database(backup_file):
    """Restaura backup do banco de dados"""
    print(f"🔄 Restaurando backup: {backup_file}")
    
    if not os.path.exists(backup_file):
        print(f"❌ Arquivo de backup não encontrado: {backup_file}")
        return False
    
    try:
        from django.core.management import call_command
        
        # Limpar dados existentes
        call_command('flush', '--noinput')
        
        # Restaurar dados
        call_command('loaddata', backup_file)
        
        print("✅ Backup restaurado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao restaurar backup: {e}")
        return False

def check_security():
    """Verifica configurações de segurança"""
    print("🔒 Verificando configurações de segurança...")
    
    issues = []
    
    # Verificar DEBUG em produção
    if not settings.DEBUG and os.getenv('ENVIRONMENT') == 'production':
        print("✅ DEBUG desabilitado em produção")
    elif settings.DEBUG and os.getenv('ENVIRONMENT') == 'production':
        issues.append("DEBUG habilitado em produção")
    
    # Verificar SECRET_KEY
    if len(settings.SECRET_KEY) < 50:
        issues.append("SECRET_KEY muito curta")
    else:
        print("✅ SECRET_KEY adequada")
    
    # Verificar configurações SSL
    if hasattr(settings, 'SECURE_SSL_REDIRECT') and settings.SECURE_SSL_REDIRECT:
        print("✅ SSL redirecionamento habilitado")
    else:
        issues.append("SSL redirecionamento desabilitado")
    
    if issues:
        print(f"⚠️  Problemas de segurança encontrados: {', '.join(issues)}")
        return False
    else:
        print("✅ Configurações de segurança adequadas")
        return True

def optimize_static_files():
    """Otimiza arquivos estáticos"""
    print("📦 Otimizando arquivos estáticos...")
    
    try:
        from django.core.management import call_command
        
        # Coletar arquivos estáticos
        call_command('collectstatic', '--noinput', '--clear')
        
        # Comprimir arquivos CSS/JS (se django-compressor estiver instalado)
        try:
            call_command('compress', '--force')
            print("✅ Arquivos estáticos comprimidos")
        except:
            print("ℹ️  django-compressor não instalado, pulando compressão")
        
        print("✅ Arquivos estáticos otimizados!")
        return True
    except Exception as e:
        print(f"❌ Erro ao otimizar arquivos estáticos: {e}")
        return False

def generate_sitemap():
    """Gera sitemap do site"""
    print("🗺️  Gerando sitemap...")
    
    try:
        from django.core.management import call_command
        call_command('generate_sitemap')
        print("✅ Sitemap gerado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar sitemap: {e}")
        return False

def check_permissions():
    """Verifica permissões de arquivos"""
    print("🔐 Verificando permissões...")
    
    critical_files = [
        'manage.py',
        'setup/settings.py',
        '.env'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            mode = oct(os.stat(file_path).st_mode)[-3:]
            if mode != '644' and file_path != '.env':
                print(f"⚠️  Permissão inadequada para {file_path}: {mode}")
            else:
                print(f"✅ {file_path}: {mode}")
    
    # Verificar .env (deve ser 600)
    if os.path.exists('.env'):
        mode = oct(os.stat('.env').st_mode)[-3:]
        if mode != '600':
            print(f"⚠️  .env deve ter permissão 600, atual: {mode}")
        else:
            print("✅ .env: 600")

def run_tests():
    """Executa testes do projeto"""
    print("🧪 Executando testes...")
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'test', '--verbosity=2'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Todos os testes passaram!")
            return True
        else:
            print(f"❌ Testes falharam:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python scripts/utils.py [comando]")
        print("Comandos disponíveis:")
        print("  check-env     - Verifica ambiente")
        print("  backup        - Cria backup do banco")
        print("  restore [file]- Restaura backup")
        print("  security      - Verifica segurança")
        print("  optimize      - Otimiza arquivos estáticos")
        print("  sitemap       - Gera sitemap")
        print("  permissions   - Verifica permissões")
        print("  test          - Executa testes")
        return
    
    command = sys.argv[1]
    
    if command == 'check-env':
        check_environment()
    elif command == 'backup':
        backup_database()
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("❌ Arquivo de backup não especificado")
            return
        restore_database(sys.argv[2])
    elif command == 'security':
        check_security()
    elif command == 'optimize':
        optimize_static_files()
    elif command == 'sitemap':
        generate_sitemap()
    elif command == 'permissions':
        check_permissions()
    elif command == 'test':
        run_tests()
    else:
        print(f"❌ Comando desconhecido: {command}")

if __name__ == '__main__':
    main()
