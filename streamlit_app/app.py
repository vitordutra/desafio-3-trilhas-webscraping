import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image

image = Image.open('../imgs/ecommerce.png')

st.write("""
## Web Scraping & Análise de preços
""")

st.image(image)

st.write("""
**Loja representante**: Americanas.

**Web Scraping das lojas**: Amazon, Americanas, Casas Bahia, Magazine Luiza e Submarino.
""")

st.sidebar.header('Filtros')

dados_gerais = pd.read_csv('../output_geral/dataset_geral.csv',sep=';')
dados_marcas = pd.read_csv('../output_geral/dataset_geral_marcas.csv',sep=';')

max_preco = 10000.0
min_preco = 0.0

# Sidebar - Slider Preço
preco_sidebar = st.sidebar.slider('Preço',min_preco, max_preco, max_preco)

# Sidebar - Seleção de Lojas
lojas = sorted(dados_gerais['Loja'].unique())
lojas_selecionadas = st.sidebar.multiselect('Seleção de lojas',lojas,lojas)

# Sidebar - Seleção de Categorias
categorias = sorted(dados_gerais['Categoria'].unique())
categorias_selecionadas = st.sidebar.multiselect('Seleção de categorias',categorias, categorias)

# Sidebar - Seleção de Marcas
marcas = sorted(dados_marcas['Marca'].unique())
marcas_selecionadas = st.sidebar.multiselect('Seleção de marcas', marcas, marcas)

selecao_preco = dados_gerais['Preço'] <= preco_sidebar

# Sidebar - Select Avaliação
# agree = st.sidebar.checkbox('Classificar por avaliação')
# if agree:
#     produto = st.sidebar.selectbox('Avaliação', ('1 Estrela', '2 Estrelas', '3 Estrelas', '4 Estrelas', '5 Estrelas'))

# DataFrame filtrados
df_filtros_geral = dados_gerais[
    (dados_gerais['Loja'].isin(lojas_selecionadas)) & (dados_gerais['Categoria'].isin(categorias_selecionadas) & selecao_preco)
]

df_filtros_marcas = dados_marcas[
    (dados_marcas['Loja'].isin(lojas_selecionadas)) & (dados_marcas['Categoria'].isin(categorias_selecionadas) & selecao_preco)
    & (dados_marcas['Marca'].isin(marcas_selecionadas))
]

st.subheader("Dados")
# Seção DataFrame de dados gerais
if st.button('Exibir dataframe de dados gerais'):
    st.markdown("**Dados Gerais**")
    st.write(f'Dimensão dos dados:  {str(df_filtros_geral.shape[0])} Linhas e {str(df_filtros_geral.shape[1])} Colunas.') 
    st.dataframe(df_filtros_geral)

# Seção DataFrame de dados por marcas
if st.button('Exibir dataframe de dados por marcas'):
    st.markdown("**Dados com marcas**")
    st.write(f'Dimensão dos dados:  {str(df_filtros_marcas.shape[0])} Linhas e {str(df_filtros_marcas.shape[1])} Colunas.') 
    st.dataframe(df_filtros_marcas)

# Agrupando dados e fazendo contagem
contagem_dados = df_filtros_geral[['Loja','Descrição']].groupby('Loja').count()
contagem_dados.reset_index(inplace=True)
contagem_dados.rename(columns={'Descrição':'Quantidade'},inplace=True)

# Gráficos
st.subheader("Gráficos")

# Plot gráfico 1
st.write("**Gráfico I - Quantidade de dados por loja**")
fig = px.bar(contagem_dados, x='Loja',y='Quantidade', text="Quantidade")
st.plotly_chart(fig)

# Criando Select Box
st.write("**A escolha de produto asseguir, influência nos dois proximos gráficos.**")
produto = st.selectbox('Escolha um produto', ('Notebook', 'Smartphone', 'TV', 'Geladeira'))
dados_selecionados = df_filtros_marcas[df_filtros_marcas["Categoria"] == produto]
    

st.write("**Gráfico II - Contagem de produtos de cada marca por loja**")

# Agrupando dados
groupby_loja_marca= dados_selecionados[['Loja','Marca','Descrição']].groupby(['Loja','Marca']).count()
groupby_loja_marca.reset_index(inplace=True)
groupby_loja_marca.rename(columns={'Descrição':'Quantidade'}, inplace=True)

# Plot de grafico 2
fig1 = px.bar(groupby_loja_marca, x='Loja',y='Quantidade',  color="Marca", title=f"Contagem de {produto}s de cada marca por loja", text="Quantidade")
st.plotly_chart(fig1)

st.write("**Gráfico III - Preço médio de produto por marca em cada loja**")

dados_selecionados = df_filtros_marcas[df_filtros_marcas["Categoria"] == produto]

# Agrupando dados
groupby_loja_marca_preco = dados_selecionados[['Loja','Marca','Preço']].groupby(['Loja','Marca']).mean()
groupby_loja_marca_preco.reset_index(inplace=True)
groupby_loja_marca_preco.rename(columns={'Preço':'Preço médio'}, inplace=True)

# Plot de gráfico 3
fig2 = px.bar(groupby_loja_marca_preco, x='Loja' ,y='Preço médio',  color="Marca", barmode="group", title=f"Preço médio de {produto} por marcas em cada loja",text="Preço médio")
fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
st.plotly_chart(fig2)

if (produto == 'Notebook'):
    ntb_processador = pd.read_csv('../output_geral/ntb_processador.csv',sep=';')
    fig_ntb = px.bar(ntb_processador, x='Loja' ,y='Preço médio',  color="Processador", barmode="group", title="Preço médio de notebooks por processador (i3, i5 ou i7) em cada loja",text="Preço médio",height=600)
    fig_ntb.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_ntb.update_layout()
    st.plotly_chart(fig_ntb)

# Plot gráfico 4
st.write("#### Gráficos de variação de preços")

ntb_diario = pd.read_csv("../output_geral/ntb_date_group.csv")
phn_diario = pd.read_csv("../output_geral/phn_date_group.csv")

st.write("**Variação diaria de preço de Notebooks**")
fig3 = go.Figure()
for col in ['Preço Americanas', 'Preço Amazon']:
    fig3.add_trace(go.Scatter(x = ntb_diario['Data'], y = ntb_diario[col], name=col))
    fig3.update_yaxes(rangemode="tozero")
    fig3.update_layout(
        yaxis_title='Preço (R$)',
        xaxis_title='Data'
    )
st.plotly_chart(fig3)

st.write("**Variação diaria de preço de Smartphones**")

fig4 = go.Figure()
for col in ['Preço Americanas', 'Preço Amazon']:
    fig4.add_trace(go.Scatter(x = phn_diario['Data'], y = phn_diario[col], name=col))
    fig4.update_yaxes(rangemode="tozero")
    fig4.update_layout(
        yaxis_title='Preço (R$)',
        xaxis_title='Data'
    )
st.plotly_chart(fig4)



