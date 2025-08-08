-- Script de inicialização do PostgreSQL
-- Este arquivo é executado automaticamente quando o container do PostgreSQL é criado pela primeira vez

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Configurar timezone
SET timezone = 'America/Sao_Paulo';

-- Criar índices de performance (se necessário)
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_produtos_nome ON produtos_produto USING gin(to_tsvector('portuguese', nome));
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_produtos_categoria ON produtos_produto(categoria_id);

-- Comentários sobre o banco
COMMENT ON DATABASE newlife_db IS 'Banco de dados do projeto New Life - Produtos Naturais';
