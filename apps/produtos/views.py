from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from apps.produtos.models import Categoria, Produto
from apps.usuarios.models import Depoimento


def home(request):
    """Página inicial com categorias e produtos em destaque"""
    categorias_principais = Categoria.objects.filter(categoria_pai__isnull=True)
    produtos_destaque = Produto.objects.filter(destaque=True)[:6]
    depoimentos = Depoimento.objects.filter(ativo=True)[:3]
    
    context = {
        'categorias_principais': categorias_principais,
        'produtos_destaque': produtos_destaque,
        'depoimentos': depoimentos,
    }
    return render(request, 'home.html', context)


def produtos_por_categoria(request, categoria_slug):
    """Lista produtos de uma categoria específica"""
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    produtos = Produto.objects.filter(categoria=categoria)
    
    context = {
        'categoria': categoria,
        'produtos': produtos,
    }
    return render(request, 'produtos/produtos_categoria.html', context)

def categoria_subcategorias(request, categoria_slug):
    """Exibe as subcategorias de uma categoria principal"""
    categoria = get_object_or_404(Categoria, slug=categoria_slug, categoria_pai__isnull=True)
    subcategorias = categoria.get_subcategorias()
    
    context = {
        'categoria': categoria,
        'subcategorias': subcategorias,
    }
    return render(request, 'produtos/categoria_subcategorias.html', context)

def detalhe_produto(request, categoria_slug, produto_id):
    """Detalhe de um produto específico"""
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    produto = get_object_or_404(Produto, id=produto_id, categoria=categoria)
    produtos_relacionados = Produto.objects.filter(categoria=categoria).exclude(id=produto_id)[:3]
    
    context = {
        'produto': produto,
        'categoria': categoria,
        'produtos_relacionados': produtos_relacionados,
    }
    return render(request, 'produtos/detalhe_produto.html', context)

def buscar_produtos(request):
    """Busca produtos por nome em todas as categorias"""
    query_string = request.GET.get("q")
    print(f"Query String: {query_string}")
    if query_string:
        produtos = Produto.objects.filter(nome__icontains=query_string)
    else:
        produtos = Produto.objects.all()
    print(f"Produtos encontrados: {produtos.count()}")
    context = {
        "produtos": produtos,
        "query": query_string
    }

    return render(request, "produtos/produtos_busca.html", context)

def comprar_produto(request, produto_id):
    """
    View intermediária que redireciona primeiro para o link do consultor
    e depois para o link final do produto
    """
    produto = get_object_or_404(Produto, id=produto_id)
    
    # Link do consultor (configurável via settings)
    link_consultor = getattr(settings, 'CONSULTOR_LINK', 'https://loja.newlifeoficial.com/nichollaspaes')
    
    # Link final do produto (cadastrado no modelo)
    link_produto_final = produto.link_compra
    
    # Criar HTML com JavaScript para redirecionamento automático
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Redirecionando para {produto.nome}...</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #1f628e 0%, #2980b9 50%, #3498db 100%);
                color: white;
                margin: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                max-width: 500px;
                width: 100%;
            }}
            .logo {{
                width: 120px;
                height: 120px;
                margin: 0 auto 30px;
                display: block;
            }}
            .loader {{
                border: 4px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top: 4px solid white;
                width: 60px;
                height: 60px;
                animation: spin 1s linear infinite;
                margin: 0 auto 30px;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            .message {{
                margin-bottom: 20px;
                font-size: 20px;
                font-weight: 500;
            }}
            .product-name {{
                font-size: 16px;
                opacity: 0.9;
                margin-bottom: 30px;
            }}
            .progress {{
                width: 100%;
                max-width: 400px;
                height: 8px;
                background: rgba(255,255,255,0.3);
                border-radius: 4px;
                overflow: hidden;
                margin: 20px auto;
            }}
            .progress-bar {{
                height: 100%;
                background: white;
                width: 0%;
                transition: width 0.3s ease;
                border-radius: 4px;
            }}
            .status {{
                font-size: 14px;
                opacity: 0.8;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="/static/img/banner/LOGOMARCA.png" alt="New Life" class="logo">
            <div class="loader"></div>
            <div class="message">Redirecionando para a loja...</div>
            <div class="product-name">Produto: {produto.nome}</div>
            <div class="progress">
                <div class="progress-bar" id="progressBar"></div>
            </div>
            <div class="status" id="status">Iniciando redirecionamento...</div>
        </div>
        
        <script>
            // Função para atualizar a barra de progresso
            function updateProgress(percent) {{
                document.getElementById('progressBar').style.width = percent + '%';
            }}
            
            // Função para atualizar o status
            function updateStatus(message) {{
                document.getElementById('status').textContent = message;
            }}
            
            // Função para redirecionar
            function redirectToStore() {{
                updateStatus('Redirecionando para a loja do consultor...');
                
                // Primeiro redireciona para o link do consultor
                window.location.href = '{link_consultor}';
                
                // Após 3 segundos, redireciona para o produto final
                setTimeout(function() {{
                    updateStatus('Redirecionando para o produto...');
                    window.location.href = '{link_produto_final}';
                }}, 3000);
            }}
            
            // Iniciar o processo
            let progress = 0;
            const interval = setInterval(function() {{
                progress += 1;
                updateProgress(progress);
                
                if (progress >= 100) {{
                    clearInterval(interval);
                    redirectToStore();
                }}
            }}, 30); // 3 segundos total (100 * 30ms)
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)