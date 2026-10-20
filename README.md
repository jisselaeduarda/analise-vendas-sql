# Análise de Vendas com SQL

Projeto de portfólio para praticar SQL, análise de dados e exportação de relatórios em CSV. Usa uma base fictícia de vendas e SQLite, sem precisar instalar um servidor de banco de dados.

## Requisitos
- Python 3.10 ou superior

## Executar
```bash
python analise.py
```
O script cria a base `vendas.db`, mostra o faturamento por produto e por mês e gera `vendas.csv`.

## Consultas SQL praticadas
- `SUM()` para somar quantidades e faturamento
- `GROUP BY` para agrupar produtos e meses
- `ORDER BY` para ordenar os resultados
- `substr()` para extrair o mês da data
- cálculo de receita: quantidade × preço unitário

## Dados
Os dados são fictícios e servem apenas para aprendizado.

## Próximas melhorias para estudar
Adicionar margem de lucro, ticket médio, filtros por período, gráficos e testes.
