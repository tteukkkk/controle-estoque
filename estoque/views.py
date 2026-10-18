from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Produto, Movimentacao
from .forms import MovimentacaoForm, ProdutoForm
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.db import transaction

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        
        if usuario is not None:
            login(request, usuario)
            return redirect('principal')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')
            
    return render(request, 'estoque/login.html')


def logout_usuario(request):
    logout(request)
    return redirect('login')


@login_required
def principal(request):
    return render(
        request,
        'estoque/principal.html'
)
    
@login_required
def produtos(request):
    busca = request.GET.get('busca')
    produtos = Produto.objects.all()
    if busca:
        produtos = produtos.filter(
            nome__icontains=busca
)
    return render(
        request,
        'estoque/produtos.html',
        {
            'produtos': produtos,
            'busca': busca
        }
    )
    
    

@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Produto cadastrado com sucesso.'
            )
            return redirect('produtos')
    else:
        form = ProdutoForm()
    return render(
        request,
        'estoque/form_produto.html',
        {'form': form}
    )
    
    

@login_required
def editar_produto(request, id):
    produto = get_object_or_404(
        Produto,
        id=id
    )
    if request.method == 'POST':
        form = ProdutoForm(
        request.POST,
            instance=produto
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Produto alterado com sucesso.'
            )
            return redirect('produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(
        request,
        'estoque/form_produto.html',
        {'form': form}
    )
    
@login_required
def excluir_produto(request, id):
    produto = get_object_or_404(
        Produto,
        id=id
    )
    if request.method == 'POST':
        try:
            produto.delete()
            messages.success(
            request,
                'Produto excluído.'
        )
        except ProtectedError:
            messages.error(
                request,
                'O produto possui movimentações '
                'e não pode ser excluído.'
            )
        return redirect('produtos')
    return render(
        request,
        'estoque/excluir_produto.html',
        {'produto': produto}
    )

@login_required
def movimentar(request):
    produtos = Produto.objects.all().order_by('nome')
    produtos_ordenados = produtos
    
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            produto = movimentacao.produto
            quantidade = movimentacao.quantidade
            
            with transaction.atomic():
                produto = Produto.objects.select_for_update().get(pk=produto.pk)
                if movimentacao.tipo == 'S' and quantidade > produto.estoque_atual:
                    messages.error(request, 'Estoque insuficiente.')
                    return redirect('movimentar')
                if movimentacao.tipo == 'E':
                    produto.estoque_atual += quantidade
                else:
                    produto.estoque_atual -= quantidade
                produto.save()
                
                movimentacao.usuario = request.user
                movimentacao.save()
                
                if produto.estoque_atual < produto.estoque_minimo:
                    messages.warning(
                        request, 
                        f'ATENÇÃO: {produto.nome} está abaixo do estoque mínimo.'
                    )
                else:
                    messages.success(request, 'Movimentação realizada com sucesso.')
                    
            return redirect('movimentar')
    else:
        form = MovimentacaoForm()
        
    return render(
        request, 
        'estoque/movimentar.html', 
        {'form': form, 'produtos': produtos_ordenados}
    )

@login_required
def historico(request):
    movimentacoes = (
        Movimentacao.objects
        .select_related(
            'produto',
            'usuario'
        )
        .order_by(
            '-data_movimentacao',
            '-id'
        )
    )
    return render(
        request,
        'estoque/historico.html',
    {
        'movimentacoes':
            movimentacoes
    }
)
