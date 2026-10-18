from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    UNIDADES = [
        ('UN', 'Unidade'),
        ('KG', 'Quilograma'),
        ('SC', 'Saco'),
        ('LT', 'Litro'),
        ('MT', 'Metro'),
        ('CX', 'Caixa'),
    ]
    
    nome = models.CharField(max_length=100)
    
    descricao = models.CharField(
        max_length=200,
        blank=True
    )
    cor = models.CharField(
        max_length=50,
        blank=True
    )
    textura = models.CharField(
        max_length=50,
        blank=True
    )
    peso = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    unidade_medida = models.CharField(
        max_length=2,
        choices=UNIDADES
    )
    aplicacao = models.CharField(
        max_length=100,
        blank=True
    )
    data_validade = models.DateField(
        null=True,
        blank=True
    )
    estoque_atual = models.PositiveIntegerField(
        default=0
    )
    estoque_minimo = models.PositiveIntegerField(
        default=5
    )
    def __str__(self):
        return self.nome
    

class Movimentacao(models.Model):
    TIPOS = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
)
    tipo = models.CharField(
        max_length=1,
        choices=TIPOS
    )
    quantidade = models.PositiveIntegerField()
    data_movimentacao = models.DateField()
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    criado_em = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return (
            f'{self.produto.nome} - '
            f'{self.get_tipo_display()}'
    )