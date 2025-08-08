# New Life Website - Docker Setup

Este documento explica como configurar e executar o projeto New Life Website usando Docker Desktop.

## Pré-requisitos

- Docker Desktop instalado e rodando
- Git (para clonar o repositório)

## Configuração Inicial

### 1. Clone o repositório (se ainda não fez)
```bash
git clone <url-do-repositorio>
cd new_life_website
```

### 2. Configure o arquivo .env
O arquivo `.env` já está configurado com as variáveis necessárias para o projeto, incluindo a conexão com o banco PostgreSQL da Render.

## Executando o Projeto

### Opção 1: Usando o script de gerenciamento (Recomendado)

```bash
# Iniciar os containers
./docker-manage.sh start

# Verificar status
./docker-manage.sh status

# Ver logs do Django
./docker-manage.sh logs

# Parar os containers
./docker-manage.sh stop

# Reiniciar os containers
./docker-manage.sh restart
```

### Opção 2: Usando comandos Docker diretamente

```bash
# Construir e iniciar os containers
docker compose up -d

# Verificar status
docker ps

# Ver logs
docker logs newlife_django

# Parar os containers
docker compose down
```

## Acessando a Aplicação

Após iniciar os containers, a aplicação estará disponível em:

- **URL Principal**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin
  - Usuário: `admin`
  - Senha: `admin123`

## Estrutura dos Containers

### Container Django (`newlife_django`)
- **Porta**: 8000
- **Imagem**: Baseada em Python 3.11
- **Funções**:
  - Servidor web Django
  - Execução de migrações
  - Coleta de arquivos estáticos
  - Criação de superusuário (desenvolvimento)
- **Banco de Dados**: Conecta ao PostgreSQL da Render

## Comandos Úteis

### Gerenciamento de Containers
```bash
# Ver status dos containers
./docker-manage.sh status

# Ver logs em tempo real
./docker-manage.sh logs

# Acessar shell do container Django
./docker-manage.sh shell

# Executar migrações
./docker-manage.sh migrate

# Coletar arquivos estáticos
./docker-manage.sh collectstatic

# Criar superusuário
./docker-manage.sh createsuperuser
```

### Desenvolvimento
```bash
# Reconstruir containers após mudanças
./docker-manage.sh build

# Reiniciar containers
./docker-manage.sh restart
```

## Solução de Problemas

### Container não inicia
1. Verifique se o Docker Desktop está rodando
2. Verifique os logs: `./docker-manage.sh logs`
3. Reconstrua os containers: `./docker-manage.sh build`

### Erro de conexão com banco
1. Verifique se a DATABASE_URL no `.env` está correta
2. Verifique se o banco da Render está acessível
3. Verifique os logs: `./docker-manage.sh logs`

### Erro de permissão
1. Certifique-se de que o script tem permissão de execução:
   ```bash
   chmod +x docker-manage.sh
   ```

### Porta já em uso
1. Verifique se há outros serviços usando a porta 8000
2. Pare os containers: `./docker-manage.sh stop`
3. Modifique as portas no `docker-compose.yml` se necessário

## Variáveis de Ambiente

As principais variáveis de ambiente estão configuradas no arquivo `.env`:

- `DEBUG`: Modo de debug (True/False)
- `SECRET_KEY`: Chave secreta do Django
- `ALLOWED_HOSTS`: Hosts permitidos
- `DATABASE_URL`: URL de conexão com o banco da Render
- `CLOUDINARY_*`: Configurações do Cloudinary
- `EMAIL_*`: Configurações de email

## Volumes e Persistência

- **Static Files**: `static_volume` - Arquivos estáticos do Django
- **Banco de Dados**: PostgreSQL da Render (externo)

## Limpeza

Para limpar completamente os containers e volumes:

```bash
# Parar e remover containers
docker compose down

# Remover volumes (CUIDADO: isso apaga os dados)
docker compose down -v

# Remover imagens
docker rmi new_life_website-web
```

## Produção

Para configuração de produção, use o arquivo `docker-compose.prod.yml`:

```bash
docker compose -f docker-compose.prod.yml up -d
```

## Suporte

Se encontrar problemas:

1. Verifique os logs: `./docker-manage.sh logs`
2. Reconstrua os containers: `./docker-manage.sh build`
3. Verifique se o Docker Desktop está rodando
4. Consulte a documentação do Django e Docker
