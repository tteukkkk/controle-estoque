from django import forms
from .models import Movimentacao, Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome",
            "descricao",
            "cor",
            "textura",
            "peso",
            "unidade_medida",
            "aplicacao",
            "data_validade",
            "estoque_minimo",
        ]
        widgets = {"data_validade": forms.DateInput(attrs={"type": "date"})}

    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if len(nome.strip()) < 3:
            raise forms.ValidationError(
                "O nome deve possuir pelo menos 3 caracteres."
            )
        return nome

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = [
            'produto',
            'tipo',
            'quantidade',
            'data_movimentacao',
        ]
        widgets = {
            'data_movimentacao': forms.DateInput(
                attrs={'type': 'date'}
            )
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade <= 0:
            raise forms.ValidationError(
                'A quantidade deve ser maior que zero.'
            )
        return quantidade



