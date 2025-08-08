# New Life Website

Um website moderno e responsivo desenvolvido em Django para produtos naturais e bem-estar. O projeto inclui funcionalidades completas de e-commerce, sistema de contato, depoimentos e administração.

## 🚀 Características Principais

- **Sistema de Produtos**: Categorias hierárquicas com produtos detalhados
- **Sistema de Busca**: Busca inteligente por nome de produtos
- **Formulário de Contato**: Envio de mensagens com notificação por email
- **Depoimentos**: Sistema de depoimentos com vídeos do YouTube
- **Design Responsivo**: Interface moderna com Bootstrap 5
- **Modo Escuro**: Toggle de tema claro/escuro
- **Administração**: Interface Django Admin completa
- **Deploy Automatizado**: Configuração Docker para desenvolvimento e produção

## 📁 Estrutura do Projeto

```
new_life_website/
├── 📁 apps/                    # Aplicações Django
│   ├── 📁 produtos/           # Gerenciamento de produtos
│   │   ├── models.py          # Categoria, Produto
│   │   ├── views.py           # Views de produtos
│   │   ├── urls.py            # URLs do app
│   │   ├── admin.py           # Interface administrativa
│   │   └── tests.py           # Testes automatizados
│   └── 📁 usuarios/           # Funcionalidades de usuário
│       ├── models.py          # Depoimento, Contato
│       ├── views.py           # Views de contato/depoimentos
│       ├── forms.py           # Formulários
│       ├── admin.py           # Interface administrativa
│       └── tests.py           # Testes automatizados
├── 📁 setup/                  # Configuração principal
│   ├── settings.py            # Configurações Django
│   ├── urls.py               # URLs principais
│   ├── wsgi.py               # Configuração WSGI
│   └── asgi.py               # Configuração ASGI
├── 📁 static/                 # Arquivos estáticos
│   ├── 📁 css/               # Estilos CSS
│   │   ├── style.css         # Estilos principais
│   │   ├── components.css    # Componentes reutilizáveis
│   │   └── navbar-fixes.css  # Correções da navbar
│   ├── 📁 js/                # JavaScript
│   │   ├── main.js           # Scripts principais
│   │   ├── search.js         # Funcionalidade de busca
│   │   └── navbar-dropdown.js # Dropdown da navbar
│   └── 📁 img/               # Imagens
│       ├── 📁 banner/        # Imagens de banner
│       └── 📁 produtos/      # Imagens de produtos
├── 📁 templates/              # Templates HTML
│   ├── base.html             # Template base
│   ├── home.html             # Página inicial
│   ├── 📁 produtos/          # Templates de produtos
│   └── 📁 usuarios/          # Templates de usuários
├── 📁 scripts/                # Scripts utilitários
│   ├── deploy.sh             # Script de deploy
│   └── utils.py              # Utilitários Python
├── 📁 docs/                   # Documentação
│   └── README.md             # Documentação detalhada
├── 📁 backup/                 # Backups do banco
├── 📄 requirements.txt        # Dependências Python
├── 📄 docker-compose.yml      # Configuração Docker dev
├── 📄 docker-compose.prod.yml # Configuração Docker prod
├── 📄 Dockerfile              # Imagem Docker
├── 📄 Makefile                # Comandos úteis
├── 📄 env.example             # Exemplo de variáveis
└── 📄 README.md               # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.3** - Framework web principal
- **PostgreSQL** - Banco de dados (produção)
- **SQLite** - Banco de dados (desenvolvimento)
- **Python 3.11+** - Linguagem de programação

### Frontend
- **Bootstrap 5** - Framework CSS responsivo
- **Font Awesome** - Biblioteca de ícones
- **JavaScript ES6+** - Funcionalidades interativas
- **CSS3** - Estilos customizados

### Infraestrutura
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Nginx** - Servidor web (produção)
- **Gunicorn** - Servidor WSGI (produção)
- **Cloudinary** - Armazenamento de mídia
- **Whitenoise** - Servir arquivos estáticos

### Ferramentas de Desenvolvimento
- **Git** - Controle de versão
- **Make** - Automação de tarefas
- **Pytest** - Testes automatizados
- **Python Decouple** - Gerenciamento de configurações

## 📋 Funcionalidades

### 🛍️ Sistema de Produtos
- **Categorias Hierárquicas**: Categorias principais e subcategorias
- **Produtos Detalhados**: Informações completas com benefícios, composição, contraindicações
- **Sistema de Busca**: Busca inteligente por nome de produtos
- **Produtos em Destaque**: Marcação para produtos especiais (destaque, lançamento, mais vendido)
- **Redirecionamento de Compra**: Links externos para compra

### 👥 Sistema de Usuários
- **Formulário de Contato**: Envio de mensagens com notificação por email
- **Depoimentos**: Sistema de depoimentos com vídeos do YouTube
- **Administração**: Interface Django Admin completa para gerenciamento

### 🎨 Interface
- **Design Responsivo**: Adaptação para todos os dispositivos
- **Modo Escuro**: Toggle de tema claro/escuro
- **Navegação Intuitiva**: Menu dropdown para categorias
- **Busca em Tempo Real**: Funcionalidade de busca avançada
- **Componentes Reutilizáveis**: CSS modular e organizado

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Git
- Docker (opcional, para containerização)
- PostgreSQL (para produção)

### 🔧 Desenvolvimento Local

#### 1. Clone o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd new_life_website
```

#### 2. Configure o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

#### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

#### 4. Configure as variáveis de ambiente
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

#### 5. Execute as migrações
```bash
python manage.py migrate
```

#### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

#### 7. Colete arquivos estáticos
```bash
python manage.py collectstatic
```

#### 8. Execute o servidor
```bash
python manage.py runserver
```

Acesse em `http://127.0.0.1:8000/` e o admin em `http://127.0.0.1:8000/admin/`

### 🐳 Docker (Recomendado)

#### Desenvolvimento
```bash
# Execute com Docker Compose
docker-compose up --build

# Acesse em http://localhost:8000
```

#### Produção
```bash
# Execute com configuração de produção
docker-compose -f docker-compose.prod.yml up --build
```

### 📦 Usando Make (Automação)

```bash
# Instalar dependências
make install

# Executar servidor
make run

# Aplicar migrações
make migrate

# Criar migrações
make makem

# Executar testes
make test

# Limpar cache
make clean
```

### 🔍 Verificação do Ambiente

```bash
# Verificar configuração
python scripts/utils.py check-env

# Executar testes
python scripts/utils.py test

# Verificar segurança
python scripts/utils.py security
```

## 📖 Uso

### 🛍️ Gerenciamento de Produtos
1. Acesse o painel administrativo em `/admin/`
2. Crie categorias principais e subcategorias
3. Adicione produtos com informações detalhadas
4. Configure campos visíveis por categoria
5. Marque produtos como destaque, lançamento ou mais vendido

### 📧 Sistema de Contato
- Formulário de contato em `/contato/`
- Notificação automática por email
- Armazenamento no banco de dados
- Interface administrativa para visualização

### 🎥 Sistema de Depoimentos
- Adicione depoimentos com vídeos do YouTube
- Controle de status ativo/inativo
- Exibição na página inicial e página dedicada

### 🔍 Funcionalidades de Busca
- Busca por nome de produtos
- Resultados em tempo real
- Interface responsiva

## 🛠️ Manutenção

### 🔄 Deploy Automatizado
```bash
# Deploy em produção
./scripts/deploy.sh production

# Deploy em staging
./scripts/deploy.sh staging

# Deploy sem backup
./scripts/deploy.sh production false
```

### 💾 Backup e Restauração
```bash
# Backup do banco
python scripts/utils.py backup

# Restaurar backup
python scripts/utils.py restore backup/newlife_20240101_120000.json

# Backup automático (usando Make)
make backup-db-render
```

### 🔍 Monitoramento
```bash
# Verificar saúde da aplicação
python scripts/utils.py check-env

# Verificar configurações de segurança
python scripts/utils.py security

# Verificar permissões de arquivos
python scripts/utils.py permissions
```

### 🧹 Limpeza
```bash
# Limpar cache Python
make clean

# Otimizar arquivos estáticos
python scripts/utils.py optimize

# Remover backups antigos (automático no deploy)
```

## 🚀 Deploy

### Render (Recomendado)
- Build automático
- PostgreSQL como banco de dados
- Nginx como proxy reverso
- SSL automático

### Heroku
- Procfile configurado
- Configurações de produção
- Variáveis de ambiente

### VPS/Dedicado
```bash
# Usando Docker
docker-compose -f docker-compose.prod.yml up -d

# Usando systemd
sudo systemctl start newlife-django
sudo systemctl start nginx
```

## 🧪 Testes

### Executar Testes
```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test apps.produtos.tests
python manage.py test apps.usuarios.tests

# Com utilitário
python scripts/utils.py test
```

### Cobertura de Testes
- Testes de modelos (Categoria, Produto, Depoimento, Contato)
- Testes de views (produtos, usuários)
- Testes de formulários
- Testes de segurança

## 📚 Documentação

Documentação detalhada disponível em `docs/README.md`:
- Arquitetura do projeto
- Configurações detalhadas
- Guias de desenvolvimento
- Troubleshooting

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Padrões de Código
- Siga o estilo PEP 8 para Python
- Use docstrings para funções e classes
- Escreva testes para novas funcionalidades
- Mantenha commits atômicos e descritivos

### Relatando Bugs
- Use o template de issue
- Inclua passos para reproduzir
- Especifique ambiente e versões
- Adicione logs de erro se aplicável

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

- **Email**: contato@newlife.com
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/new-life-website/issues)
- **Documentação**: [docs/README.md](docs/README.md)

---

**Desenvolvido com ❤️ pela equipe New Life**


