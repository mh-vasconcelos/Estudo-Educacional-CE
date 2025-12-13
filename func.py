from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px


# Carregador de Dados
@st.cache_data
def load_data():
    df19 = pd.read_csv('indicadores19.csv')
    df24 = pd.read_csv('indicadores24.csv')
    

    df19 = df19.rename(columns={
        'NO_MUNICIPIO_RESIDENCIA': 'MUNICIPIO', 
        'Computador': 'Total_Computador', 
        'Internet': 'Total_Internet'
    })
    df24 = df24.rename(columns={
        'NO_MUNICIPIO_PROVA': 'MUNICIPIO', 
        'Computador': 'Total_Computador', 
        'Internet': 'Total_Internet'
    })
    
    return df19, df24

def grafico_comparativo(df_indicadores_mun, df_indicadores_mun24, notas = False):
  df_final = pd.merge(
    df_indicadores_mun[['MUNICIPIO', 'Taxa_Inclusao_Digital', 'Taxa_Computador', 'Taxa_Internet', 'Nota_Media_Geral', 'Nota_Redacao','Nota_CH', 'Nota_Mat', 'Nota_CN', 'Nota_LC', 'Total_Alunos']],
    df_indicadores_mun24[['MUNICIPIO', 'Taxa_Inclusao_Digital', 'Taxa_Computador', 'Taxa_Internet', 'Nota_Media_Geral', 'Nota_Redacao','Nota_CH', 'Nota_Mat', 'Nota_CN', 'Nota_LC','Total_Alunos']],
    on='MUNICIPIO',
    suffixes=('_2019', '_2024'))
  
  # condicionar flag notas
  if notas:
    metricas = {
    'Nota_Media_Geral': 'Nota Média',
    'Nota_Redacao': 'Nota Redação',
    'Nota_CH': 'Nota CH',
    'Nota_LC': 'Nota LC',
    'Nota_CN': 'Nota CN',
    'Nota_Mat': 'Nota Mat',

    }
    
  else:
    metricas = {
    'Taxa_Inclusao_Digital': 'Taxa Inclusão Digital',
    'Taxa_Computador': 'Taxa Computador',
    'Taxa_Internet': 'Taxa Internet',
    'Total_Alunos': 'Total de Alunos (Média Mun.)'}


  dados_resumo = []
  # criar tabela de resumo
  for metrica_db, metrica_nome in metricas.items():
      valor_19 = df_final[f'{metrica_db}_2019'].mean()
      valor_24 = df_final[f'{metrica_db}_2024'].mean()
      
      if metrica_db == 'Total_Alunos':
          valor_19 = df_final[f'{metrica_db}_2019'].sum()
          valor_24 = df_final[f'{metrica_db}_2024'].sum()
          metrica_nome = 'Total de Alunos (Soma Estado)'
      
      delta = valor_24 - valor_19
      var_pct = (delta / valor_19) * 100
      
      dados_resumo.append({
          'Indicador': metrica_nome,
          '2019': valor_19,
          '2024': valor_24,
          'Diferença': delta,
          'Variação (%)': var_pct
      })

  df_resumo_executivo = pd.DataFrame(dados_resumo)

  # gerar gráfico
  st.write("### Tabela Resumo")
  st.dataframe(df_resumo_executivo.sort_values(by=['Variação (%)'], ascending=False)) 

  df_plot = df_resumo_executivo[df_resumo_executivo['Indicador'] != 'Total de Alunos (Soma Estado)'].melt(
      id_vars='Indicador', 
      value_vars=['2019', '2024'], 
      var_name='Ano', 
      value_name='Valor'
  )

  fig, ax = plt.subplots(figsize=(14, 9))
  
  grafico = sns.barplot(data=df_plot, x='Indicador', y='Valor', hue='Ano', palette=['gray', 'blue'], ax=ax)

  ax.set_title('Comparativo de Indicadores: 2019 vs 2024', fontsize=14)
  ax.set_ylabel('Taxa Média / Nota')
  plt.xticks(rotation=15) 
  ax.legend(title='Ano')

  for container in grafico.containers:
      grafico.bar_label(container, fmt='%.2f', padding=3)

  plt.tight_layout()
  
  st.pyplot(fig)




def gerar_histograma(df, coluna, cor, titulo, x_label, is_nota=False):
    """
    Gera um objeto de figura Plotly (histograma) padronizado.
    """
    fig = px.histogram(
        df, 
        x=coluna, 
        nbins=20, 
        color_discrete_sequence=[cor], 
        title=titulo
    )
    
    fig.update_layout(
        xaxis_title=x_label, 
        yaxis_title="Qtd. Municípios", 
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    if not is_nota:
        fig.update_xaxes(range=[0, 1])
        
    return fig