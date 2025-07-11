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