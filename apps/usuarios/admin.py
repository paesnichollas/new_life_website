from django.contrib import admin

from .models import Depoimento, Contato

@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    list_display = ['nome_cliente', 'video_youtube_id', 'ativo']
    list_filter = ['ativo']
    list_editable = ['ativo']


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'assunto', 'data_envio']
    list_filter = ['data_envio']
    readonly_fields = ['data_envio']
    search_fields = ['nome', 'email', 'assunto']

