# Revisão para portfólio

## Alterações comuns

- Removidos ambientes virtuais, arquivos compilados, bancos SQLite, uploads locais e estáticos coletados.
- Configuração de credenciais por variáveis de ambiente; arquivo `.env.example` sem senha real.
- SQLite como padrão para demonstração e MySQL opcional.
- Dependências e instruções de instalação documentadas.
- DEFAULT_AUTO_FIELD alinhado às migrações existentes.

## Alterações específicas

Leitura e validação de estoque realizadas dentro da transação, após bloqueio do produto; testes de entrada e saída insuficiente.

## Verificação executada

Python 3.12.14 / Django 5.2.18 / SQLite. 5 testes passaram; check, conferência de migrações e migrate concluíram com sucesso. Testes novos cobrem fluxos alterados e se somam aos testes originais. Não houve teste de MySQL, concorrência real, implantação ou inspeção visual em navegador da aplicação local.

## Limitações

É um sistema acadêmico com permissão ampla para usuários autenticados. Não inclui múltiplos depósitos, perfis detalhados por função ou auditoria de todas as edições. A proteção de saldo concorrente precisa ser validada no MySQL.

## Modelos principais

- `Produto`
- `Movimentacao`
