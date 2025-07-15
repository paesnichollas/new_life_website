from apps.produtos.models import Categoria

def categorias_globais(request):
    categorias_principais = Categoria.objects.filter(categoria_pai__isnull=True)
    return {
        'categorias_globais': categorias_principais
    }

