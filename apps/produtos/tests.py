from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Produto


class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria_principal = Categoria.objects.create(
            nome="Produtos Naturais",
            slug="produtos-naturais",
            icone="bi bi-leaf",
            descricao="Produtos naturais para saúde e bem-estar"
        )
        
        self.subcategoria = Categoria.objects.create(
            nome="Chás",
            slug="chas",
            icone="bi bi-cup-hot",
            categoria_pai=self.categoria_principal
        )

    def test_categoria_str(self):
        """Testa a representação string da categoria"""
        self.assertEqual(str(self.categoria_principal), "Produtos Naturais")
        self.assertEqual(str(self.subcategoria), "Produtos Naturais > Chás")

    def test_is_categoria_principal(self):
        """Testa se a categoria é principal"""
        self.assertTrue(self.categoria_principal.is_categoria_principal())
        self.assertFalse(self.subcategoria.is_categoria_principal())

    def test_get_subcategorias(self):
        """Testa obtenção de subcategorias"""
        subcategorias = self.categoria_principal.get_subcategorias()
        self.assertEqual(subcategorias.count(), 1)
        self.assertEqual(subcategorias.first(), self.subcategoria)

    def test_get_campos_visiveis(self):
        """Testa configuração de campos visíveis"""
        campos = self.categoria_principal.get_campos_visiveis()
        self.assertIn('composicao', campos)
        self.assertIn('contraindicacao', campos)
        self.assertIn('modo_uso', campos)

    def test_deve_exibir_campo(self):
        """Testa verificação de campo visível"""
        self.assertTrue(self.categoria_principal.deve_exibir_campo('composicao'))
        self.assertTrue(self.categoria_principal.deve_exibir_campo('contraindicacao'))


class ProdutoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome="Chás",
            slug="chas"
        )
        
        self.produto = Produto.objects.create(
            categoria=self.categoria,
            nome="Chá Verde",
            link_compra="https://exemplo.com/cha-verde",
            descricao="Chá verde natural",
            beneficios="Antioxidante\nEnergia\nSaúde",
            composicao="Folhas de chá verde\nVitamina C",
            contraindicacao="Não recomendado para gestantes",
            modo_uso="1 xícara por dia"
        )

    def test_produto_str(self):
        """Testa a representação string do produto"""
        self.assertEqual(str(self.produto), "Chá Verde")

    def test_get_beneficios_list(self):
        """Testa obtenção de benefícios como lista"""
        beneficios = self.produto.get_beneficios_list()
        self.assertEqual(len(beneficios), 3)
        self.assertIn("Antioxidante", beneficios)
        self.assertIn("Energia", beneficios)
        self.assertIn("Saúde", beneficios)

    def test_get_composicao_list(self):
        """Testa obtenção de composição como lista"""
        composicao = self.produto.get_composicao_list()
        self.assertEqual(len(composicao), 2)
        self.assertIn("Folhas de chá verde", composicao)
        self.assertIn("Vitamina C", composicao)


class ProdutoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(
            nome="Chás",
            slug="chas"
        )
        
        self.produto = Produto.objects.create(
            categoria=self.categoria,
            nome="Chá Verde",
            link_compra="https://exemplo.com/cha-verde",
            descricao="Chá verde natural",
            beneficios="Antioxidante\nEnergia",
            composicao="Folhas de chá verde",
            contraindicacao="Não recomendado para gestantes",
            modo_uso="1 xícara por dia"
        )

    def test_home_view(self):
        """Testa a view da página inicial"""
        response = self.client.get(reverse('produtos:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_produtos_por_categoria_view(self):
        """Testa a view de produtos por categoria"""
        response = self.client.get(reverse('produtos:produtos_categoria', args=['chas']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produtos/produtos_categoria.html')
        self.assertIn('produtos', response.context)

    def test_detalhe_produto_view(self):
        """Testa a view de detalhe do produto"""
        response = self.client.get(reverse('produtos:detalhe_produto', args=['chas', self.produto.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produtos/detalhe_produto.html')
        self.assertIn('produto', response.context)

    def test_buscar_produtos_view(self):
        """Testa a view de busca de produtos"""
        response = self.client.get(reverse('produtos:buscar_produtos'), {'q': 'verde'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produtos/produtos_busca.html')
        self.assertIn('produtos', response.context)

    def test_buscar_produtos_sem_query(self):
        """Testa busca sem query string"""
        response = self.client.get(reverse('produtos:buscar_produtos'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('produtos', response.context)

    def test_redirecionar_compra_view(self):
        """Testa a view de redirecionamento para compra"""
        response = self.client.get(reverse('produtos:redirecionar_compra', args=['chas', self.produto.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produtos/redirecionar_compra.html')
        self.assertIn('produto', response.context)


class CategoriaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria_principal = Categoria.objects.create(
            nome="Produtos Naturais",
            slug="produtos-naturais"
        )
        
        self.subcategoria = Categoria.objects.create(
            nome="Chás",
            slug="chas",
            categoria_pai=self.categoria_principal
        )

    def test_categoria_subcategorias_view(self):
        """Testa a view de subcategorias"""
        response = self.client.get(reverse('produtos:categoria_subcategorias', args=['produtos-naturais']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produtos/categoria_subcategorias.html')
        self.assertIn('subcategorias', response.context)

    def test_categoria_404(self):
        """Testa 404 para categoria inexistente"""
        response = self.client.get(reverse('produtos:produtos_categoria', args=['categoria-inexistente']))
        self.assertEqual(response.status_code, 404)
