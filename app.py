import streamlit as st
import pandas as pd
import plotly.express as px

# Leitura dos dados
dados = pd.read_excel('Vendas_Base_de_Dados.xlsx')

# Cálculo do faturamento
dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']

# Filtros na barra lateral
st.sidebar.header('Filtros')
lojas = sorted(dados['Loja'].unique())
produtos = ['Todos'] + sorted(dados['Produto'].unique())

loja_escolhida = st.sidebar.selectbox('Escolha a loja:', lojas)
produto_escolhido = st.sidebar.selectbox('Escolha o produto:', produtos)

# Aplicação dos filtros
dados_filtrados = dados[dados['Loja'] == loja_escolhida]
if produto_escolhido != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['Produto'] == produto_escolhido]

# Faturamento total após o filtro
faturamento_total = dados_filtrados['Faturamento'].sum()

# Título e tabela
st.title('Dashboard de Vendas')
st.write('Tabela de vendas do mês (após filtro):')
st.dataframe(dados_filtrados)

# Exibir o faturamento total
st.subheader(f'Faturamento total: R$ {faturamento_total:,.2f}')

# Gráfico de barras: faturamento por loja (usando todos os dados, não filtrado)
dados_lojas = (
    dados.groupby('Loja')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Faturamento', ascending=False)
)

grafico_barras = px.bar(dados_lojas, x='Loja', y='Faturamento', title='Faturamento por Loja')
st.plotly_chart(grafico_barras)

# Gráfico de pizza: participação dos produtos na loja selecionada
dados_loja = dados[dados['Loja'] == loja_escolhida]
dados_produtos_loja = (
    dados_loja.groupby('Produto')['Faturamento']
    .sum()
    .reset_index()
)

grafico_pizza = px.pie(
    dados_produtos_loja,
    names='Produto',
    values='Faturamento',
    title=f'Participação dos produtos no faturamento da loja {loja_escolhida}'
)
st.plotly_chart(grafico_pizza)

# Texto resumo
if produto_escolhido == 'Todos':
    st.info(f'Na loja {loja_escolhida}, o faturamento total considerando todos os produtos foi de R$ {faturamento_total:,.2f}.')
else:
    st.info(f'Na loja {loja_escolhida}, o produto {produto_escolhido} teve um faturamento total de R$ {faturamento_total:,.2f}.')
