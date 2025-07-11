# Projeto New Life Website

Este é um projeto de website desenvolvido em Django, focado em produtos naturais e bem-estar. O site inclui funcionalidades para exibição de produtos, categorias, subcategorias, detalhes de produtos, além de seções para contato e depoimentos.

## Estrutura do Projeto

```
new_life_website1/
├── manage.py
├── README.md
├── apps/
│   ├── produtos/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   └── usuarios/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations/
│       ├── models.py
│       ├── tests.py
│       └── views.py
├── setup/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── img/
│   │   ├── banner/
│   │   └── produtos/
│   └── js/
│       └── main.js
├── staticfiles/ (gerado pelo Django)
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── produtos/
│   │   ├── categoria_subcategorias.html
│   │   ├── detalhe_produto.html
│   │   └── produtos_categoria.html
│   └── usuarios/
│       ├── contato.html
│       └── depoimentos.html
└── db.sqlite3 (banco de dados padrão do Django)
```

## Funcionalidades

- **Página Inicial:** Exibição de produtos em destaque e informações gerais.
- **Produtos:** Listagem de produtos por categoria e subcategoria, com páginas de detalhes para cada produto.
- **Contato:** Formulário de contato para que os usuários possam enviar mensagens.
- **Depoimentos:** Seção para exibir depoimentos de clientes.
- **Administração:** Painel de administração Django para gerenciamento de conteúdo (produtos, usuários, etc.).

## Tecnologias Utilizadas

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Banco de Dados:** SQLite3 (padrão, pode ser configurado para outros)

## Instalação e Configuração

Siga os passos abaixo para configurar e rodar o projeto localmente:

1.  **Clone o repositório:**

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd new_life_website1
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```
    *Nota: O arquivo `requirements.txt` não foi fornecido no ZIP, mas é uma prática recomendada. Você pode precisar criar um com as dependências do Django e outras bibliotecas usadas.* 

4.  **Execute as migrações do banco de dados:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Crie um superusuário (para acessar o painel de administração):**

    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções no terminal para criar o usuário.

6.  **Colete arquivos estáticos:**

    ```bash
    python manage.py collectstatic
    ```

7.  **Inicie o servidor de desenvolvimento:**

    ```bash
    python manage.py runserver
    ```

    O site estará disponível em `http://127.0.0.1:8000/` e o painel de administração em `http://127.0.0.1:8000/admin/`.

## Uso

Após a instalação, você pode navegar pelo site, adicionar produtos e categorias através do painel de administração, e testar as funcionalidades de contato e depoimentos.

## Contribuição

Se você deseja contribuir com este projeto, por favor, siga as diretrizes de contribuição (se houver) ou entre em contato com o mantenedor do projeto.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. (Assumindo licença MIT, caso contrário, ajuste conforme necessário).


