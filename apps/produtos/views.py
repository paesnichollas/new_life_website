from django.shortcuts import render, get_object_or_404
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

def redirecionar_compra(request, categoria_slug, produto_id):
    """Redireciona para a loja do consultor e depois para a página do produto"""
    produto = get_object_or_404(Produto, id=produto_id)
    
    # URL da loja do consultor
    loja_consultor = "https://loja.newlifeoficial.com/nichollaspaes"
    
    # URL final do produto (extraída do link_compra do produto)
    url_produto_final = produto.link_compra
    
    context = {
        'produto': produto,
        'loja_consultor': loja_consultor,
        'url_produto_final': url_produto_final,
        'categoria_slug': categoria_slug,
        'produto_id': produto_id,
    }
    
    return render(request, 'produtos/redirecionar_compra.html', context)