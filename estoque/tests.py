from django.test import TestCase
from django.contrib.auth.models import User
from .models import Produto

class ProdutoTestCase(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='teste',
            password='123456'
        )
        self.produto = Produto.objects.create(
            nome='Cimento',
            unidade_medida='SC',
            estoque_atual=20,
            estoque_minimo=5
        )

    def test_produto_criado(self):
        self.assertEqual(
            self.produto.nome,
            'Cimento'
        )

    def test_estoque_inicial(self):
        self.assertEqual(
            self.produto.estoque_atual,
            20
        )

    def test_login(self):
        login = self.client.login(
            username='teste',
            password='123456'
        )
        self.assertTrue(login)