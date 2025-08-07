from django.db import DatabaseError
from apps.produtos.models import Categoria

def categorias_globais(request):
    try:
        categorias_principais = Categoria.objects.filter(categoria_pai__isnull=True)
        return {
            'categorias_globais': categorias_principais
        }
    except DatabaseError:
        # Retorna lista vazia se houver erro de banco de dados
        return {
            'categorias_globais': []
        }
    except Exception:
        # Fallback para qualquer outro erro
        return {
            'categorias_globais': []
        }

