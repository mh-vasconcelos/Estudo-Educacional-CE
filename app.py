import streamlit as st
import pandas as pd
import plotly.express as px
from img import img_list
from func import grafico_comparativo, gerar_histograma

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Educação Digital CE: 2019 vs 2024", layout="wide", page_icon="📊")

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    df19 = pd.read_csv('indicadores19.csv')
    df24 = pd.read_csv('indicadores24.csv')
    

    df19 = df19.rename(columns={
        'NO_MUNICIPIO_PROVA': 'Municipio', 
        'Computador': 'Total_Computador', 
        'Internet': 'Total_Internet'
    })
    df24 = df24.rename(columns={
        'NO_MUNICIPIO_PROVA': 'Municipio', 
        'Computador': 'Total_Computador', 
        'Internet': 'Total_Internet'
    })
    
    return df19, df24

try:
    df19, df24 = load_data()
except FileNotFoundError:
    st.error("⚠️ Arquivos 'indicadores19.csv' ou 'indicadores24.csv' não encontrados na pasta.")
    st.stop()

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("⚙️ Configurações")
st.sidebar.info("Selecione a métrica que deseja comparar entre o período Pré e Pós Pandemia.")

metricas_disponiveis = {
    'Taxa_Inclusao_Digital': '🌐 Taxa de Suporte Digital ao Estudo (PC + Net)',
    'Taxa_Computador': '💻 Posse de Computador',
    'Taxa_Internet': '📡 Acesso à Internet'
    # 'Nota_Media_Geral': '📝 Nota Média do ENEM'
}

metrica_selecionada = st.sidebar.radio(
    "Métrica de Análise:", 
    list(metricas_disponiveis.keys()), 
    format_func=lambda x: metricas_disponiveis[x]
)

nome_metrica = metricas_disponiveis[metrica_selecionada]

# --- CÁLCULOS GERAIS ---
media_19 = df19[metrica_selecionada].mean()
media_24 = df24[metrica_selecionada].mean()
delta_absoluto = media_24 - media_19
delta_percentual = delta_absoluto * 100

if delta_absoluto > 0:
    cor_delta = "normal" 
    cor_texto = "green"
    icone = "📈"
    tendencia = "CRESCIMENTO"
else:
    cor_delta = "normal" 
    cor_texto = "red"
    icone = "📉"
    tendencia = "RETROCESSO"

# --- INTERFACE PRINCIPAL ---
st.title("📊 Panorama da Educação Digital no Ceará")
# --- Seção Explicativa ---
st.markdown('### 💡 Métrica de Interesse: Taxa de Suporte Digital ao Estudo')
st.markdown(
    'O indicador mede a **proporção de estudantes que possuem acesso a um computador** '
    '***E*** **acesso à internet** em casa, essencial para uma participação digital completa **no contexto educativo, visando o aprendizado e desempenho nas provas**. '
    'É calculado a partir das seguintes variáveis, dividindo pelo **Total de Alunos**:'
)

# Fórmula em latex
with st.container(border=True):
    st.latex(
        r'''
        \text{Taxa de Suporte Digital ao Estudo} = \frac{\text{Alunos com Computador } \cap \text{ Alunos com Internet}}{\text{Total de Alunos}}
        '''
    )

    st.markdown('---')

    st.markdown('#### Detalhes das Variáveis')
    st.markdown(
        '* **Alunos com Computador $\cap$ Alunos com Internet:** '
        'O número de alunos que responderam **sim** para **AMBOS** os requisitos. '
        'Representa a **Inclusão Plena**.'
    )
    st.markdown(
        '* **Total de Alunos:** O número total de estudantes por município (ou total, caso agreguemos para o estado)'
    )

# st.markdown("---")
# --- Comparativo ---
with st.container(border=True):
    st.markdown(f"### Comparativo: **{nome_metrica}**")
    # st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2019 (Pré-Pandemia)")
        st.metric(label="Média Estadual", value=f"{media_19:.2f}", delta_color="off")    

    # --- COLUNA 2: 2024 ---
    with col2:
        st.subheader("2024 (Pós-Pandemia)")
        st.metric(label="Média Estadual", value=f"{media_24:.2f}", delta=f"{delta_percentual:.1f} p.p.", delta_color=cor_delta)
    graf1, graf2 = st.columns(2)
    with graf1:
        fig1 = gerar_histograma(
        df=df19,
        coluna=metrica_selecionada,
        cor='#8e44ad', # roxo
        titulo="Distribuição dos Municípios (2019)",
        x_label=nome_metrica,
        is_nota=False
    )
        st.plotly_chart(fig1, use_container_width=True)
    
    with graf2:
        fig2 = gerar_histograma(
            df=df24,
            coluna=metrica_selecionada,
            cor='#ff9f43', # laranja
            titulo="Distribuição dos Municípios (2024)",
            x_label=nome_metrica,
            is_nota=False
        )
        st.plotly_chart(fig2, use_container_width=True)


    # --- Storytelling ---
    st.subheader("💡 Análise do Cenário")

    insight = ""
    if metrica_selecionada == 'Taxa_Computador':
        insight = "Isso evidencia o **'Paradoxo da Conectividade'**. Embora haja mais alunos, o estoque de equipamentos de produtividade (computadores) diminuiu, sugerindo uma migração massiva para o celular."
    elif metrica_selecionada == 'Taxa_Internet':
        insight = "O acesso à rede foi **universalizado**. A pandemia acelerou a infraestrutura de telecomunicações, rompendo a barreira do sinal para a maioria dos municípios. A Internet virou uma espécie de commodity e sua rápida proliferação foi suficiente para aumentar os índices do ENEM para a maioria"
    elif metrica_selecionada == 'Taxa_Inclusao_Digital':
        insight = "A Inclusão Plena (ter as duas coisas) caiu. Estamos criando uma geração **'Mobile-Only'**, o que pode limitar o desenvolvimento de habilidades técnicas avançadas."

    texto_explicativo = f"""
    Entre 2019 e 2024, o Ceará observou um(a) :{cor_texto}[**{tendencia}**] de **{abs(delta_percentual):.1f} pontos percentuais** neste indicador.
    {insight}
    """

    st.markdown(f"#### {icone} O que isso significa?")
    st.write(texto_explicativo)
    # --- EXTRAS: TABELA DE DADOS ---
    with st.expander("🔍 Ver Dados Detalhados por Município"):
        df_merge = pd.merge(df19[['Municipio', metrica_selecionada, 'Total_Alunos']], df24[['Municipio', metrica_selecionada, 'Total_Alunos']], on='Municipio', suffixes=('_19', '_24'))
        df_merge[f'{metrica_selecionada}_19'] = round((df_merge[f'{metrica_selecionada}_19']) * 1, 4)
        df_merge[f'{metrica_selecionada}_24'] = round((df_merge[f'{metrica_selecionada}_24']) * 1, 4)
        df_merge['Variação (p.p)'] = round((df_merge[f'{metrica_selecionada}_24'] - df_merge[f'{metrica_selecionada}_19']), 4) * 100.000
        # df_merge[f'{metrica_selecionada}_19'] = ((df_merge[f'{metrica_selecionada}_19'])).map('{:.2f}%'.format)
        # df_merge[f'{metrica_selecionada}_24'] = ((df_merge[f'{metrica_selecionada}_24'])).map('{:.2f}%'.format)
        st.dataframe(df_merge.sort_values('Variação (p.p)', ascending=False))


## COMPARATIVO ENEM 2019 X 2024
with st.container(border=True):
    nota_media19 = df19['Nota_Media_Geral'].mean()
    nota_media24 = df24['Nota_Media_Geral'].mean()
    delta_enem = ((nota_media24- nota_media19) / nota_media19) * 100
    if delta_enem > 0:
        cor_delta_enem = "normal" 
        cor_texto_enem = "green"
        icone_enem = "📈"
        tendencia_enem = "CRESCIMENTO"
    else:
        cor_delta_enem = "inverse" 
        cor_texto_enem = "red"
        icone_enem = "📉"
        tendencia_enem = "RETROCESSO"
    insight_enem = "Surpreendentemente, **o desempenho subiu** mesmo com a queda dos computadores. Hipótese provável: o uso de **IA Generativa e Celulares** compensou a falta de hardware físico."
    texto_explicativo_nota= f"""
    Entre 2019 e 2024, o Ceará observou um(a) :{cor_texto_enem}[**{tendencia_enem}**] de **{abs(delta_enem):.1f} %** neste indicador.
    {insight_enem}
    """


    st.subheader("📝 Nota Média do ENEM")
# Definição de Cores e Ícones baseados na tendência
    col12, col22 = st.columns(2)
    with col12:
        st.subheader("2019 (Pré-Pandemia)")
        st.metric(label="Média Estadual da Nota do ENEM", value=f"{nota_media19:.2f}")


    with col22:
        st.subheader("2024 (Pós-Pandemia)")
        st.metric(label="Média Estadual da Nota do ENEM", value=f"{nota_media24:.2f}", delta=f"{delta_enem:.1f}%", delta_color=cor_delta_enem)
    
    graf_enem1, graf_enem2 = st.columns(2)
    with graf_enem1:
        fig1_enem = gerar_histograma(
            df=df19,
            coluna='Nota_Media_Geral',
            cor='#8e44ad', # roxo
            titulo="Distribuição dos Municípios (2019)",
            x_label='📝 Nota Média do ENEM',
            is_nota=True
        )
        st.plotly_chart(fig1_enem, use_container_width=True)
    
    with graf_enem2:
        fig2_enem = gerar_histograma(
            df=df24,
            coluna='Nota_Media_Geral' ,
            cor='#ff9f43', # laranja
            titulo="Distribuição dos Municípios (2019)",
            x_label='📝 Nota Média do ENEM',
            is_nota=True
        )
        st.plotly_chart(fig2_enem, use_container_width=True)

        
    st.subheader("💡 Análise do Cenário")
    st.write(texto_explicativo_nota)




st.markdown("---")
with st.container(border=True):
  st.markdown(f"## {icone} Hipótese da IA Generativa")
  st.write("Tentamos considerar o efeito revolucionário das Inteligências Artificiais Generativas, que poderiam ter influenciado a subida da nota, especialmente em redação, apesar da baixa adesão à dispositivos adequados.")
  col1, col2 = st.columns(2)
  with col1:
    st.image(img_list[0], use_container_width=True) # use_container_width ajusta ao tamanho da coluna
  with col2:
    st.image(img_list[1], use_container_width=True)
  grafico_comparativo(df_indicadores_mun=df19, df_indicadores_mun24=df24, notas=True)

