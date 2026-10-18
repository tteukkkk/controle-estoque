from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Produto,Movimentacao

class MovimentacaoTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('operador',password='teste-local-123');self.client.force_login(self.user)
        self.produto=Produto.objects.create(nome='Cimento',unidade_medida='SC',estoque_atual=5)

    def test_saida_insuficiente_nao_cria_movimento(self):
        self.client.post(reverse('movimentar'),{'produto':self.produto.pk,'tipo':'S','quantidade':6,'data_movimentacao':'2026-01-01'})
        self.produto.refresh_from_db();self.assertEqual(self.produto.estoque_atual,5);self.assertFalse(Movimentacao.objects.exists())

    def test_entrada_atualiza_saldo_e_historico(self):
        self.client.post(reverse('movimentar'),{'produto':self.produto.pk,'tipo':'E','quantidade':2,'data_movimentacao':'2026-01-01'})
        self.produto.refresh_from_db();self.assertEqual(self.produto.estoque_atual,7);self.assertEqual(Movimentacao.objects.get().usuario,self.user)
