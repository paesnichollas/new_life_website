# New Life Website - Documentação

## Visão Geral

O New Life Website é uma plataforma Django para exibição e gerenciamento de produtos naturais e de bem-estar. O projeto inclui funcionalidades completas de e-commerce, sistema de contato, depoimentos e administração.

## Arquitetura do Projeto

### Estrutura de Apps

```
apps/
├── produtos/          # Gerenciamento de produtos e categorias
│   ├── models.py      # Categoria, Produto
│   ├── views.py       # Views para listagem e detalhes
│   ├── urls.py        # URLs específicas do app
│   └── admin.py       # Interface administrativa
└── usuarios/          # Funcionalidades de usuário
    ├── models.py      # Depoimento, Contato
    ├── views.py       # Views de contato e depoimentos
    ├── forms.py       # Formulários
    └── admin.py       # Interface administrativa
```

### Configuração Principal

```
setup/
├── settings.py        # Configurações Django
├── urls.py           # URLs principais
├── wsgi.py           # Configuração WSGI
└── asgi.py           # Configuração ASGI
```

### Arquivos Estáticos

```
static/
├── css/              # Estilos CSS
├── js/               # JavaScript
└── img/              # Imagens
    ├── banner/       # Imagens de banner
    └── produtos/     # Imagens de produtos
```

## Funcionalidades Principais

### 1. Sistema de Produtos
- **Categorias Hierárquicas**: Categorias principais e subcategorias
- **Produtos Detalhados**: Informações completas com benefícios, composição, etc.
- **Sistema de Busca**: Busca por nome de produtos
- **Produtos em Destaque**: Marcação para produtos especiais

### 2. Sistema de Usuários
- **Formulário de Contato**: Envio de mensagens com notificação por email
- **Depoimentos**: Sistema de depoimentos com vídeos do YouTube
- **Administração**: Interface Django Admin completa

### 3. Frontend
- **Design Responsivo**: Bootstrap 5
- **Modo Escuro**: Toggle de tema
- **Navegação Intuitiva**: Menu dropdown para categorias
- **Busca em Tempo Real**: Funcionalidade de busca

## Tecnologias Utilizadas

### Backend
- **Django 5.2.3**: Framework web principal
- **PostgreSQL**: Banco de dados (produção)
- **SQLite**: Banco de dados (desenvolvimento)

### Frontend
- **Bootstrap 5**: Framework CSS
- **Font Awesome**: Ícones
- **JavaScript**: Funcionalidades interativas

### Infraestrutura
- **Docker**: Containerização
- **Nginx**: Servidor web (produção)
- **Cloudinary**: Armazenamento de mídia
- **Gunicorn**: Servidor WSGI (produção)

## Configuração de Ambiente

### Desenvolvimento Local
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd new_life_website

# Configure o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp env.example .env
# Edite o arquivo .env com suas configurações

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Execute o servidor
python manage.py runserver
```

### Docker (Desenvolvimento)
```bash
# Execute com Docker Compose
docker-compose up --build

# Acesse em http://localhost:8000
```

### Produção
```bash
# Execute com configuração de produção
docker-compose -f docker-compose.prod.yml up --build
```

## Estrutura de Banco de Dados

### Modelos Principais

#### Categoria
- `nome`: Nome da categoria
- `slug`: URL amigável
- `icone`: Ícone da categoria
- `descricao`: Descrição da categoria
- `categoria_pai`: Relacionamento hierárquico
- `campos_visiveis`: Configuração de campos visíveis

#### Produto
- `categoria`: Categoria do produto
- `nome`: Nome do produto
- `link_compra`: Link externo para compra
- `imagem`: URL da imagem
- `descricao`: Descrição do produto
- `beneficios`: Lista de benefícios
- `composicao`: Composição do produto
- `contraindicacao`: Contraindicações
- `modo_uso`: Instruções de uso
- `destaque`: Produto em destaque
- `lancamento`: Produto lançamento
- `mais_vendido`: Produto mais vendido

#### Depoimento
- `nome_cliente`: Nome do cliente
- `video_youtube_id`: ID do vídeo do YouTube
- `citacao`: Citação curta
- `texto_transformacao`: Texto longo sobre transformação
- `ativo`: Status ativo/inativo

#### Contato
- `nome`: Nome do contato
- `email`: Email do contato
- `assunto`: Assunto da mensagem
- `mensagem`: Conteúdo da mensagem
- `data_envio`: Data de envio

## Configurações de Email

O projeto utiliza SMTP do Gmail para envio de emails de contato. Configure as seguintes variáveis:

```env
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
CONTACT_EMAIL=contato@newlife.com
```

## Configurações do Cloudinary

Para armazenamento de imagens, configure:

```env
CLOUDINARY_CLOUD_NAME=seu-cloud-name
CLOUDINARY_API_KEY=sua-api-key
CLOUDINARY_API_SECRET=sua-api-secret
```

## Comandos Úteis

### Desenvolvimento
```bash
# Executar servidor
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Shell Django
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic
```

### Docker
```bash
# Executar com Docker
make run

# Backup do banco
make backup-db-render

# Limpar cache
make clean
```

## Deploy

### Render
O projeto está configurado para deploy no Render com:
- Build automático
- PostgreSQL como banco de dados
- Nginx como proxy reverso
- SSL automático

### Heroku
Configuração disponível com:
- Procfile para gunicorn
- Configurações de produção
- Variáveis de ambiente

## Manutenção

### Backup
O projeto inclui script automatizado de backup:
```bash
./backup.sh
```

### Logs
Os logs são configurados para produção com rotação automática.

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.
