from django.db import models

class Depoimento(models.Model):
    nome_cliente = models.CharField(max_length=100)
    video_youtube_id = models.CharField(max_length=20, help_text="Apenas o ID do vídeo do YouTube")
    citacao = models.TextField(help_text="Citação curta do cliente")
    texto_transformacao = models.TextField(help_text="Texto mais longo sobre a transformação")
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Depoimento de {self.nome_cliente}"
    
    def get_youtube_embed_url(self):
        """Retorna a URL de embed do YouTube"""
        return f"https://www.youtube.com/embed/{self.video_youtube_id}"
    
    class Meta:
        verbose_name = "Depoimento"
        verbose_name_plural = "Depoimentos"


class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    assunto = models.CharField(max_length=200)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Contato de {self.nome} - {self.assunto}"
    
    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ['-data_envio']
