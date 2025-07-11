from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nome = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    icone = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Ícone da categoria (ex: 'bi bi-heart', 'fas fa-leaf')"
    )
    descricao = models.TextField(
        blank=True, 
        null=True,
        help_text="Descrição da categoria"
    )
    categoria_pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategorias')
    
    # Configuração de campos visíveis para produtos desta categoria
    campos_visiveis = models.JSONField(
        default=dict,
        blank=True,
        help_text="Configuração de quais campos devem ser exibidos para produtos desta categoria. "
                  "Exemplo: {'composicao': True, 'contraindicacao': True, 'modo_uso': True}"
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.categoria_pai:
            return f"{self.categoria_pai.nome} > {self.nome}"
        return self.nome
    
    def is_categoria_principal(self):
        """Retorna True se é uma categoria principal (não tem pai)"""
        return self.categoria_pai is None
    
    def get_subcategorias(self):
        """Retorna as subcategorias desta categoria"""
        return self.subcategorias.all()
    
    def get_campos_visiveis(self):
        """Retorna a configuração de campos visíveis, com valores padrão se não configurado"""
        campos_padrao = {
            'composicao': True,
            'contraindicacao': True,
            'modo_uso': True,
        }
        
        if not self.campos_visiveis:
            return campos_padrao
        
        # Mescla configuração personalizada com padrões
        campos_finais = campos_padrao.copy()
        campos_finais.update(self.campos_visiveis)
        return campos_finais
    
    def deve_exibir_campo(self, nome_campo):
        """Verifica se um campo específico deve ser exibido para esta categoria"""
        campos_visiveis = self.get_campos_visiveis()
        return campos_visiveis.get(nome_campo, True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=200)
    link_compra = models.URLField(help_text="Link externo para compra do produto")
    imagem = models.URLField(max_length=300, blank=True, null=True)
    descricao = models.TextField()
    beneficios = models.TextField(help_text="Lista de benefícios separados por linha")
    composicao = models.TextField(help_text="Composição detalhada do produto")
    contraindicacao = models.TextField(help_text="Contraindicações e precauções")
    modo_uso = models.TextField(help_text="Instruções de uso do produto")
    destaque = models.BooleanField(default=False, help_text="Marcar para exibir na página inicial")
    lancamento = models.BooleanField(default=False, help_text="Marcar como produto lançamento")
    mais_vendido = models.BooleanField(default=False, help_text="Marcar como produto mais vendido")
    
    def __str__(self):
        return self.nome
    
    def get_beneficios_list(self):
        """Retorna os benefícios como uma lista"""
        return [beneficio.strip() for beneficio in self.beneficios.split('\n') if beneficio.strip()]
    
    def get_composicao_list(self):
        """Retorna a composição como uma lista"""
        return [item.strip() for item in self.composicao.split('\n') if item.strip()]
    
    def get_contraindicacao_list(self):
        """Retorna as contraindicações como uma lista"""
        return [item.strip() for item in self.contraindicacao.split('\n') if item.strip()]
    
    def get_modo_uso_list(self):
        """Retorna o modo de uso como uma lista"""
        return [item.strip() for item in self.modo_uso.split('\n') if item.strip()]
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"