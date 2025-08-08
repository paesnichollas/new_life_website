from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Depoimento, Contato
from .forms import ContatoForm


class DepoimentoModelTest(TestCase):
    def setUp(self):
        self.depoimento = Depoimento.objects.create(
            nome_cliente="João Silva",
            video_youtube_id="abc123def",
            citacao="Produto incrível!",
            texto_transformacao="Transformou minha vida completamente.",
            ativo=True
        )

    def test_depoimento_str(self):
        """Testa a representação string do depoimento"""
        self.assertEqual(str(self.depoimento), "Depoimento de João Silva")

    def test_get_youtube_embed_url(self):
        """Testa geração da URL de embed do YouTube"""
        expected_url = "https://www.youtube.com/embed/abc123def"
        self.assertEqual(self.depoimento.get_youtube_embed_url(), expected_url)


class ContatoModelTest(TestCase):
    def setUp(self):
        self.contato = Contato.objects.create(
            nome="Maria Santos",
            email="maria@exemplo.com",
            assunto="Dúvida sobre produto",
            mensagem="Gostaria de saber mais sobre o chá verde."
        )

    def test_contato_str(self):
        """Testa a representação string do contato"""
        expected = "Contato de Maria Santos - Dúvida sobre produto"
        self.assertEqual(str(self.contato), expected)

    def test_contato_ordering(self):
        """Testa ordenação dos contatos por data de envio"""
        contato2 = Contato.objects.create(
            nome="João Silva",
            email="joao@exemplo.com",
            assunto="Outro assunto",
            mensagem="Outra mensagem"
        )
        
        contatos = Contato.objects.all()
        # O mais recente deve vir primeiro
        self.assertEqual(contatos[0], contato2)
        self.assertEqual(contatos[1], self.contato)


class ContatoFormTest(TestCase):
    def test_contato_form_valid(self):
        """Testa formulário de contato válido"""
        form_data = {
            'nome': 'João Silva',
            'email': 'joao@exemplo.com',
            'assunto': 'Dúvida sobre produto',
            'mensagem': 'Gostaria de saber mais sobre o produto.'
        }
        form = ContatoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contato_form_invalid_email(self):
        """Testa formulário com email inválido"""
        form_data = {
            'nome': 'João Silva',
            'email': 'email-invalido',
            'assunto': 'Dúvida sobre produto',
            'mensagem': 'Gostaria de saber mais sobre o produto.'
        }
        form = ContatoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_contato_form_empty_fields(self):
        """Testa formulário com campos vazios"""
        form_data = {
            'nome': '',
            'email': '',
            'assunto': '',
            'mensagem': ''
        }
        form = ContatoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('assunto', form.errors)
        self.assertIn('mensagem', form.errors)


class UsuariosViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.depoimento = Depoimento.objects.create(
            nome_cliente="João Silva",
            video_youtube_id="abc123def",
            citacao="Produto incrível!",
            texto_transformacao="Transformou minha vida completamente.",
            ativo=True
        )

    def test_depoimentos_view(self):
        """Testa a view de depoimentos"""
        response = self.client.get(reverse('usuarios:depoimentos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/depoimentos.html')
        self.assertIn('depoimentos', response.context)

    def test_depoimentos_view_only_active(self):
        """Testa se apenas depoimentos ativos são exibidos"""
        # Criar depoimento inativo
        Depoimento.objects.create(
            nome_cliente="Maria Santos",
            video_youtube_id="xyz789",
            citacao="Produto ruim",
            texto_transformacao="Não funcionou.",
            ativo=False
        )
        
        response = self.client.get(reverse('usuarios:depoimentos'))
        depoimentos = response.context['depoimentos']
        self.assertEqual(depoimentos.count(), 1)
        self.assertEqual(depoimentos.first(), self.depoimento)

    def test_contato_view_get(self):
        """Testa a view de contato (GET)"""
        response = self.client.get(reverse('usuarios:contato'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/contato.html')
        self.assertIn('form', response.context)

    def test_contato_view_post_valid(self):
        """Testa a view de contato com dados válidos (POST)"""
        form_data = {
            'nome': 'João Silva',
            'email': 'joao@exemplo.com',
            'assunto': 'Dúvida sobre produto',
            'mensagem': 'Gostaria de saber mais sobre o produto.'
        }
        response = self.client.post(reverse('usuarios:contato'), form_data)
        
        # Deve redirecionar ou permanecer na mesma página com sucesso
        self.assertIn(response.status_code, [200, 302])
        
        # Verificar se o contato foi criado
        contato = Contato.objects.filter(email='joao@exemplo.com').first()
        self.assertIsNotNone(contato)
        self.assertEqual(contato.nome, 'João Silva')

    def test_contato_view_post_invalid(self):
        """Testa a view de contato com dados inválidos (POST)"""
        form_data = {
            'nome': '',
            'email': 'email-invalido',
            'assunto': '',
            'mensagem': ''
        }
        response = self.client.post(reverse('usuarios:contato'), form_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/contato.html')
        self.assertIn('form', response.context)
        
        # Verificar se não foi criado contato
        self.assertEqual(Contato.objects.count(), 0)
