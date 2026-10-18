from django.contrib import admin
from .models import Produto, Movimentacao

# Register your models here.

admin.site.register(Produto)
admin.site.register(Movimentacao)