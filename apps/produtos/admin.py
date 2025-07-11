from django.contrib import admin
from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone', 'categoria_pai', 'slug']
    list_filter = ['categoria_pai']
    search_fields = ['nome', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}
    fields = ['nome', 'slug', 'icone', 'descricao', 'categoria_pai', 'campos_visiveis']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Adiciona help text mais detalhado para o campo campos_visiveis
        if 'campos_visiveis' in form.base_fields:
            form.base_fields['campos_visiveis'].help_text = (
                "Configure quais campos devem ser exibidos para produtos desta categoria. "
                "Exemplo para categoria Beleza (ocultar composição e contraindicações): "
                '{"composicao": false, "contraindicacao": false, "modo_uso": false}'
            )
        return form


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'destaque', 'lancamento', 'mais_vendido']
    list_filter = ['categoria', 'destaque', 'lancamento', 'mais_vendido']
    search_fields = ['nome', 'descricao']
    list_editable = ['destaque', 'lancamento', 'mais_vendido']