from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<slug:categoria_slug>/', views.categoria_subcategorias, name='categoria_subcategorias'),
    path('produtos/<slug:categoria_slug>/', views.produtos_por_categoria, name='produtos_categoria'),
    path('produtos/<slug:categoria_slug>/<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
]

