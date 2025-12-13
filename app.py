import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from img import img_list, img_box, img_ideb, img_ideb_ce, mapa_taxa
from func import grafico_comparativo, gerar_histograma

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Educação Digital CE: 2019 vs 2023", layout="wide", page_icon="📊")

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    df19 = pd.read_csv('indicadores19.csv')
    df24 = pd.read_csv('indicadores24.csv')
    df23 = pd.read_csv('indicadores23.csv')    

    df19 = df19.rename(columns={
        'NO_MUNICIPIO_PROVA': 'MUNICIPIO', 
        'Computador': 'Total_Computador', 
        'Internet': 'Total_Internet'
    })
    df23 = df23.rename(columns={
        'NO_MUNICIPIO_PROVA': 'MUNICIPIO', 
        'Computador': 'Total_Computador', 
        'Internet': 'Total_Internet'
    })
    
    return df19, df23, df24

try:
    df19, df23, df24 = load_data()
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
media_23 = df23[metrica_selecionada].mean()
delta_absoluto = media_23 - media_19
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

with st.container(border=True):
    st.markdown(f'### Mapa de calor da Taxa de Suporte Digital ao Estudo no Ceará (2023)')
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(mapa_taxa, use_container_width=True)

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
        st.subheader("2023 (Pós-Pandemia)")
        st.metric(label="Média Estadual", value=f"{media_23:.2f}", delta=f"{delta_percentual:.1f} p.p.", delta_color=cor_delta)
    graf1, graf2 = st.columns(2)
    with graf1:
        fig1 = gerar_histograma(
        df=df19,
        coluna=metrica_selecionada,
        cor='#8e44ad', # roxo
        titulo="Distribuição dos Municípios (2023)",
        x_label=nome_metrica,
        is_nota=False
    )
        st.plotly_chart(fig1, use_container_width=True)
    
    with graf2:
        fig2 = gerar_histograma(
            df=df23,
            coluna=metrica_selecionada,
            cor='#ff9f43', # laranja
            titulo="Distribuição dos Municípios (2023)",
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
    Entre 2019 e 2023, o Ceará observou um(a) :{cor_texto}[**{tendencia}**] de **{abs(delta_percentual):.1f} pontos percentuais** neste indicador.
    {insight}
    """

    # st.markdown(f"#### {icone} O que isso significa?")
    st.write(texto_explicativo)
    # --- EXTRAS: TABELA DE DADOS ---
    with st.expander("🔍 Ver Mais"):
        with st.expander("Ver Dados Detalhados por Município"):
            df_merge = pd.merge(df19[['MUNICIPIO', metrica_selecionada, 'Total_Alunos']], df23[['MUNICIPIO', metrica_selecionada, 'Total_Alunos']], on='MUNICIPIO', suffixes=('_19', '_23'))
            df_merge[f'{metrica_selecionada}_19'] = round((df_merge[f'{metrica_selecionada}_19']) * 1, 4)
            df_merge[f'{metrica_selecionada}_23'] = round((df_merge[f'{metrica_selecionada}_23']) * 1, 4)
            df_merge['Variação (p.p)'] = round((df_merge[f'{metrica_selecionada}_23'] - df_merge[f'{metrica_selecionada}_19']), 4) * 100.000
            # df_merge[f'{metrica_selecionada}_19'] = ((df_merge[f'{metrica_selecionada}_19'])).map('{:.2f}%'.format)
            # df_merge[f'{metrica_selecionada}_23'] = ((df_merge[f'{metrica_selecionada}_23'])).map('{:.2f}%'.format)
            st.dataframe(df_merge.sort_values('Variação (p.p)', ascending=False))
        with st.expander("Municípios abaixo do percentil 25 em 2023"):
            p25 = np.percentile(df23[metrica_selecionada], 25)
            df_baixo = df23[df23[metrica_selecionada] <= p25]
            df_baixo = df_baixo[['MUNICIPIO', metrica_selecionada, 'Total_Alunos']]
            df_baixo[metrica_selecionada] = round((df_baixo[metrica_selecionada]) * 1, 4)
            st.dataframe(df_baixo.sort_values(metrica_selecionada))
        with st.expander("Municípios acima do percentil 75 em 2023"):
            p75 = np.percentile(df23[metrica_selecionada], 75)
            df_alto = df23[df23[metrica_selecionada] >= p75]
            df_alto = df_alto[['MUNICIPIO', metrica_selecionada, 'Total_Alunos']]
            df_alto[metrica_selecionada] = round((df_alto[metrica_selecionada]) * 1, 4)
            st.dataframe(df_alto.sort_values(metrica_selecionada, ascending=False))

        


## COMPARATIVO ENEM 2019 X 2023
alunos19 = pd.read_csv('alunos19.csv')
alunos23 = pd.read_csv('alunos23.csv')  

with st.container(border=True):
    # nota_media19 = alunos19['media'].mean()
    # nota_media24 = alunos23['media'].mean()
    nota_media19 = df19['Nota_Media_Geral'].dropna().mean()
    nota_media24 = df23['Nota_Media_Geral'].dropna().mean()
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
    insight_enem = "Surpreendentemente, **o desempenho subiu** mesmo com a queda dos computadores. Hipótese provável: o uso de **IA Generativa e Celulares** compensou a falta de hardware físico. \n\nA universalização da internet atuou como uma rede de segurança, garantindo um aumento na nota média através da inclusão massiva. No entanto, trocamos um crescimento potencial de alta eficiência (via computadores) por um crescimento de volume (via mobile), o que sugere que estamos operando abaixo do nosso potencial máximo"
    texto_explicativo_nota= f"""
    Entre 2019 e 2023, o Ceará observou um(a) :{cor_texto_enem}[**{tendencia_enem}**] de **{abs(delta_enem):.1f} %** neste indicador.
    {insight_enem}
    """


    st.subheader("📝 Nota Média do ENEM")
# Definição de Cores e Ícones baseados na tendência
    col12, col22 = st.columns(2)
    with col12:
        st.subheader("2019 (Pré-Pandemia)")
        st.metric(label="Média Estadual da Nota do ENEM", value=f"{nota_media19:.2f}")


    with col22:
        st.subheader("2023 (Pós-Pandemia)")
        st.metric(label="Média Estadual da Nota do ENEM", value=f"{nota_media24:.2f}", delta=f"{delta_enem:.1f}%", delta_color=cor_delta_enem)
    
    graf_enem1, graf_enem2 = st.columns(2)
    with graf_enem1:
        fig1_enem = gerar_histograma(
            df=df19,
            coluna='Nota_Media_Geral',
            cor='#8e44ad', # roxo
            titulo="Distribuição dos Municípios (2023)",
            x_label='📝 Nota Média do ENEM',
            is_nota=True
        )
        st.plotly_chart(fig1_enem, use_container_width=True)
    
    with graf_enem2:
        fig2_enem = gerar_histograma(
            df=df23,
            coluna='Nota_Media_Geral' ,
            cor='#ff9f43', # laranja
            titulo="Distribuição dos Municípios (2019)",
            x_label='📝 Nota Média do ENEM',
            is_nota=True
        )
        st.plotly_chart(fig2_enem, use_container_width=True)

        
    st.subheader("💡 Análise do Cenário")
    st.write(texto_explicativo_nota)
    with st.expander("🔍 Ver Mais"):
        with st.expander("Ver Dados Detalhados por Município"):
            df_merge_enem = pd.merge(df19[['MUNICIPIO', 'Nota_Media_Geral', 'Total_Alunos']], df23[['MUNICIPIO', 'Nota_Media_Geral', 'Total_Alunos']], on='MUNICIPIO', suffixes=('_19', '_23'))
            df_merge_enem['Nota_Media_Geral_19'] = round(df_merge_enem['Nota_Media_Geral_19'], 2)
            df_merge_enem['Nota_Media_Geral_23'] = round(df_merge_enem['Nota_Media_Geral_23'], 2)
            df_merge_enem['Variação (p.p)'] = round((df_merge_enem['Nota_Media_Geral_23'] - df_merge_enem['Nota_Media_Geral_19']) / df_merge_enem['Nota_Media_Geral_19'] * 100, 2)
            # df_merge_enem['Nota_Media_Geral_19'] = df_merge_enem['Nota_Media_Geral_19'].map('{:.2f}'.format)
            # df_merge_enem['Nota_Media_Geral_23'] = df_merge_enem['Nota_Media_Geral_23'].map('{:.2f}'.format)
            st.dataframe(df_merge_enem.sort_values('Variação (p.p)', ascending=False))
        with st.expander("Municípios abaixo do percentil 25 em 2023"):
            p25_enem = np.percentile(df23['Nota_Media_Geral'], 25)
            df_baixo_enem = df23[df23['Nota_Media_Geral'] <= p25_enem]
            df_baixo_enem = df_baixo_enem[['MUNICIPIO', 'Nota_Media_Geral', 'Total_Alunos']]
            df_baixo_enem['Nota_Media_Geral'] = round(df_baixo_enem['Nota_Media_Geral'], 2)
            st.dataframe(df_baixo_enem.sort_values('Nota_Media_Geral'))
        with st.expander("Municípios acima do percentil 75 em 2023"):
            p75_enem = np.percentile(df23['Nota_Media_Geral'], 75)
            df_alto_enem = df23[df23['Nota_Media_Geral'] >= p75_enem]
            df_alto_enem = df_alto_enem[['MUNICIPIO', 'Nota_Media_Geral', 'Total_Alunos']]
            df_alto_enem['Nota_Media_Geral'] = round(df_alto_enem['Nota_Media_Geral'], 2)
            st.dataframe(df_alto_enem.sort_values('Nota_Media_Geral', ascending=False))




# Preparar dados (remover NA)
df19_corr = df19[["Nota_Media_Geral", metrica_selecionada]].dropna()
df23_corr = df23[["Nota_Media_Geral", metrica_selecionada]].dropna()
# Calcular correlação de Pearson
corr19 = round(df19_corr["Nota_Media_Geral"].corr(df19_corr[metrica_selecionada]), 2) if not df19_corr.empty else None
corr24 = round(df23_corr["Nota_Media_Geral"].corr(df23_corr[metrica_selecionada]),2) if not df23_corr.empty else None
delta_absoluto_corr = corr24 - corr19
delta_percentual = delta_absoluto_corr * 100

if delta_absoluto_corr > 0:
    cor_delta = "normal" 
    cor_texto = "green"
    icone = "📈"
    tendencia = "AUMENTO"
else:
    cor_delta = "normal" 
    cor_texto = "red"
    icone = "📉"
    tendencia = "QUEDA"


        # --- Seção: Correlação entre Nota Média e Taxa de Suporte Digital ---
st.markdown("---")
with st.container(border=True):
    st.markdown("# 🔗 Análise Bivariada")
        
    with st.container(border=True):
        st.markdown(f"### Correlação entre Nota Média do ENEM e {nome_metrica}")
        # Plots de dispersão lado a lado
        col_a, col_b = st.columns(2)
        with col_a:
                st.metric(label="2019", value=corr19)    
                fig_corr19 = px.scatter(
                        df19_corr,
                        x=metrica_selecionada,
                        y='Nota_Media_Geral',
                        title=f'2019: Nota Média vs {metrica_selecionada}',
                        labels={metrica_selecionada: 'Taxa de Suporte Digital', 'Nota_Media_Geral': 'Nota Média ENEM'},
                        color_discrete_sequence=['#8e44ad']
                )
                st.plotly_chart(fig_corr19, use_container_width=True)

        with col_b:
                st.metric(label="2023", value=corr24)  
                fig_corr24 = px.scatter(
                        df23_corr,
                        x=metrica_selecionada,
                        y='Nota_Media_Geral',
                        title='2023: Nota Média vs Taxa de Suporte Digital',
                        labels={metrica_selecionada: 'Taxa de Suporte Digital', 'Nota_Media_Geral': 'Nota Média ENEM'},
                        color_discrete_sequence=['#ff9f43']
                )
                st.plotly_chart(fig_corr24, use_container_width=True)

        # --- Storytelling ---
        st.subheader("💡 Análise do Cenário")

        insight = ""
        if metrica_selecionada == 'Taxa_Computador':
            insight = "A correlação desta métrica com a Nota do ENEM permanece alta e robusta (próxima a **0.70**) em ambos os anos. Isso ocorre porque a posse de um computador ainda é um diferencial competitivo significativo para o desempenho acadêmico, mesmo com o aumento do uso de celulares."

        elif metrica_selecionada == 'Taxa_Internet':
            insight = "O acesso à rede foi **universalizado**, virando uma *commodity*. A pandemia rompeu a barreira do sinal, mas isso gerou um fenômeno estatístico: a correlação entre 'Ter Internet' e 'Nota do ENEM' **caiu drasticamente**. Isso significa que ter internet deixou de ser um diferencial competitivo e virou o piso básico: quase todo mundo tem, inclusive quem tira nota baixa."
            

        elif metrica_selecionada == 'Taxa_Inclusao_Digital':
            insight = "A Taxa de Suporte Digital (PC + Internet) subiu. Ela segue praticamente a mesma tendência do computador porque, estatisticamente, ele é o computador. Como quase todos já têm internet, a única coisa que separa quem tem Suporte Digital de quem não tem é a posse da máquina. Com a escassez de equipamentos, ter um suporte digital completo tornou-se um privilégio ainda mais exclusivo. Quem tem essa ferramenta se destaca ainda mais da massa mobile, fortalecendo a relação entre ter o equipamento e ter a nota alta."

        texto_explicativo_corr = f"""
        Entre 2019 e 2023, o Ceará observou um(a) :{cor_texto}[**{tendencia}**] na correlação entre {metrica_selecionada} e a nota média.\n\n
        {insight}
        """
        st.write(texto_explicativo_corr)
        with st.expander("🔍 Ver Dados Detalhados por Município"):
            df_merge_corr = pd.merge(df19[['MUNICIPIO', metrica_selecionada, 'Nota_Media_Geral']], df23[['MUNICIPIO', metrica_selecionada, 'Nota_Media_Geral']], on='MUNICIPIO', suffixes=('_19', '_23'))
            df_merge_corr[f'{metrica_selecionada}_19'] = round((df_merge_corr[f'{metrica_selecionada}_19']) * 1, 4)
            df_merge_corr[f'{metrica_selecionada}_23'] = round((df_merge_corr[f'{metrica_selecionada}_23']) * 1, 4)
            st.dataframe(df_merge_corr)


    # st.markdown("---")
    with st.container(border=True):
        st.markdown("## 📊 Desigualdade Social ainda reflete na nota em 2023")
        st.markdown("---")
        st.markdown("### 📦 Boxplot 2019 vs 2023")
        st.write("Boxplots comparativos com uma variável qualitativa (ano de análise) e outra quantitativa (a métrica selecionada), para visualizar a distribuição e variações entre os anos.")
        box1, box2 = st.columns(2)
        with box1:
            # 1. Boxplot dinâmico da métrica selecionada
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            data_group1_sel = df19[metrica_selecionada].dropna()
            data_group2_sel = df23[metrica_selecionada].dropna()
            ax1.boxplot([data_group1_sel, data_group2_sel], positions=[1, 2], labels=['2019', '2023'])
            ax1.set_title(f'Comparação de {metrica_selecionada}: 2019 vs 2023')
            ax1.set_ylabel(metrica_selecionada)
            ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig1)

        with box2:
            # 2. Boxplot estático da nota média geral
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            data_group1_nota = df19['Nota_Media_Geral'].dropna()
            data_group2_nota = df24['Nota_Media_Geral'].dropna()
            ax2.boxplot([data_group1_nota, data_group2_nota], positions=[1, 2], labels=['2019', '2023'])
            ax2.set_title('Comparação de Nota Média Geral: 2019 vs 2023')
            ax2.set_ylabel('Nota Média Geral')
            ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig2)
    with st.container(border=True):
        st.markdown("### Gráfico Comparativo: Alta Estrutura X Baixa Estrutura")
        st.markdown("#### 📦 Estagnação na Educação em 2023 foi perceptível")
        img1, img2 = st.columns(2)
        with img1:
            st.image(img_ideb)
        with img2:
            st.image(img_ideb_ce)
        st.write("O panorama é preocupante pois a desigualdade entre as escolas estruturadas e as não estruturadas se manteve, mesmo que o acesso à informação tenha se democratizado.")
        st.markdown("### 📦 Associação de Variáveis: Escolas de Alta Estrutura vs Escolas de Baixa Estrutura ")
        st.write("Boxplots comparativos entre escolas com alta estrutura (Federal e Privada) e baixa estrutura (Municipal e Estadual), para visualizar se houve uma mudança no GAP entre esses grupos ao longo do tempo.")
        st.image(img_box)
    with st.container(border=True):
        st.markdown("### 📦 IDEB")
        st.write("O Índice de Desenvolvimento da Educação Básica (IDEB) é um indicador que mede a qualidade do ensino nas escolas brasileiras. Ele combina dados de desempenho acadêmico (notas em avaliações padronizadas) e taxas de aprovação escolar para fornecer uma visão geral do sistema educacional.")
        # correlacao_ideb = df19['IDEB19'].corr(df19_corr['Nota_Media_Geral'])

        # 2. Exibindo a Métrica Atualizada
        corr_ideb_19 = df19[['Nota_Media_Geral', 'IDEB19']].corr().iloc[0,1]
        corr_ideb_23 = df23[['Nota_Media_Geral', 'IDEB23']].corr().iloc[0,1]
        corr_ideb_taxa_19 = df19[['Taxa_Inclusao_Digital', 'IDEB19']].corr().iloc[0,1]
        corr_ideb_taxa_23 = df23[['Taxa_Inclusao_Digital', 'IDEB23']].corr().iloc[0,1]
        ideb19, ideb23 = st.columns(2)
        with ideb19:
            st.metric(label="Correlação (IDEB vs ENEM)", value=f"{corr_ideb_19:.2f}")
            # 3. Gerando o Gráfico
            fig_corr19 = px.scatter(
                    df19,
                    x='IDEB19', # <--- AQUI: Mudamos para a coluna do IDEB
                    y='Nota_Media_Geral',
                    title=f'2019: Impacto do IDEB na Nota do ENEM',
                    labels={'IDEB19': f'Nota do IDEB (2019)', 'Nota_Media_Geral': 'Nota Média ENEM'},
                    color_discrete_sequence=['#8e44ad'],
                    # trendline="ols" # DICA: Adiciona a linha de tendência para provar a correlação visualmente
            )

            st.plotly_chart(fig_corr19, use_container_width=True)
            st.markdown("---")
            st.markdown("\n\n")

    
            st.metric(label="Correlação (IDEB vs Taxa de Suporte Digital)", value=f"{corr_ideb_taxa_19:.2f}")
            # 3. Gerando o Gráfico
            fig_corr_taxa_19 = px.scatter(
                    df19,
                    x='IDEB19', # <--- AQUI: Mudamos para a coluna do IDEB
                    y='Taxa_Inclusao_Digital',
                    title=f'2019: Correlação entre IDEB e Taxa de Suporte Digital',
                    labels={'IDEB19': f'Nota do IDEB (2019)', 'Taxa_Inclusao_Digital': 'Taxa de Suporte Digital'},
                    color_discrete_sequence=['#8e44ad'],
                    # trendline="ols" # DICA: Adiciona a linha de tendência para provar a correlação visualmente
            )

            st.plotly_chart(fig_corr_taxa_19, use_container_width=True)
        with ideb23:
            st.metric(label="Correlação (IDEB vs ENEM)", value=f"{corr_ideb_23:.2f}")
            fig_corr23 = px.scatter(
                    df23,
                    x='IDEB23', # <--- AQUI: Mudamos para a coluna do IDEB
                    y='Nota_Media_Geral',
                    title='2023: Impacto do IDEB na Nota do ENEM',
                    labels={'IDEB23': f'Nota do IDEB (2023)', 'Nota_Media_Geral': 'Nota Média ENEM'},
                    color_discrete_sequence=['#ff9f43'],
                    # trendline="ols" # DICA: Adiciona a linha de tendência para provar a correlação visualmente
            )
            st.plotly_chart(fig_corr23, use_container_width=True)
            st.markdown("---")
            st.markdown("\n\n")

            st.metric(label="Correlação (IDEB vs Taxa de Suporte Digital)", value=f"{corr_ideb_taxa_23:.2f}")
            # 3. Gerando o Gráfico
            fig_corr_taxa_23 = px.scatter(
                    df23,
                    x='IDEB23', # <--- AQUI: Mudamos para a coluna do IDEB
                    y='Taxa_Inclusao_Digital',
                    title=f'2023: Correlação entre IDEB e Taxa de Suporte Digital',
                    labels={'IDEB23': f'Nota do IDEB (2023)', 'Taxa_Inclusao_Digital': 'Taxa de Suporte Digital'},
                    color_discrete_sequence=['#ff9f43'],
                    # trendline="ols" # DICA: Adiciona a linha de tendência para provar a correlação visualmente
            )

            st.plotly_chart(fig_corr_taxa_23, use_container_width=True)
        st.subheader("💡 Análise do Cenário")
        st.write("O IDEB perdeu parte de sua capacidade de representar o aprendizado real no cenário pós-pandemia.\nIsso ocorre, em partes, porque houve um mascaramento dos efeitos reais da pandemia nas avaliações internas.")
 


        

    


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

st.markdown("---")
with st.container(border=True):
    st.markdown("## 📋 Conclusão e Relatório Final")
    st.markdown("""
    ### Panorama Geral da Educação Digital no Ceará (2019 vs 2023)
    
    Este dashboard analisou a evolução da inclusão digital educacional no Ceará, comparando dados agregados por município do ENEM de 2019 (pré-pandemia) e 2024 (pós-pandemia). Os indicadores principais — Taxa de Inclusão Digital Plena (computador + internet), Taxa de Posse de Computador e Taxa de Acesso à Internet — revelam transformações significativas no acesso a tecnologias, com impactos diretos no desempenho acadêmico medido pela Nota Média Geral do ENEM.
    
    ### Principais Descobertas
    
    #### 1. **Evolução das Taxas de Acesso Tecnológico**
    - **Taxa de Suporte Digital**: Caiu de aproximadamente ~9 pontos percentuais, indicando uma geração "Mobile-Only" — alunos com acesso à internet via celular, mas sem computadores adequados para estudos avançados.
    - **Posse de Computador**: Diminuiu drasticamente (queda de ~10 pontos percentuais), evidenciando o "Paradoxo da Conectividade": mais alunos, mas menos equipamentos de produtividade.
    - **Acesso à Internet**: Universalizou-se, com aumento significativo (~20-30 pontos percentuais), tornando-se uma commodity essencial. A pandemia acelerou a infraestrutura de telecomunicações, rompendo barreiras de sinal em municípios remotos.
    
    #### 2. **Impacto no Desempenho Acadêmico (Nota Média do ENEM)**
    - A nota média estadual subiu (~3%), apesar da queda na inclusão digital plena. Isso sugere que fatores exógenos, além do aumento da conectividade compensaram a falta de hardware tradicional.
    - Correlação com Suporte Digital: Forte em 2019 (~0.70), com um bom aumento em 2023 (~0.81), indicando que ter computador deixou de ser um diferencial competitivo.
    - Correlação com Internet: Caiu drasticamente (de ~0.47 para ~0.16), pois o acesso se tornou ubíquo, não diferenciando mais alunos de alto desempenho.
    - Correlação com Computador: Manteve-se robusta (~0.65-0.70), bem similar a correlação com a taxa de suporte digital, confirmando que equipamentos de produtividade ainda são cruciais para habilidades técnicas avançadas.
    
    
    #### 3. **Hipótese da IA Generativa e Tecnologias Emergentes**
    - A subida das notas, apesar da queda em computadores, aponta para o papel compensatório de IA generativa, celulares inteligentes e ferramentas online. Alunos de baixa renda podem estar usando esses recursos para nivelar o campo de jogo.
    - Recomendação: Políticas públicas devem focar em hardware (computadores/notebooks) para alunos de baixa renda, enquanto incentivam o uso ético de IA em redação e estudos.
    
    ### Recomendações Estratégicas
    - **Para Governos e Escolas**: Investir em distribuição de equipamentos, não apenas conectividade. Programas para fornecimento de dispositivos adequados ao estudo devem ser priorizados.
    - **Para Educadores**: Adaptar currículos para incluir habilidades digitais móveis, mas sem negligenciar o treinamento em ferramentas avançadas (ex.: programação, análise de dados).
    - **Para Pesquisa Futura**: Investigar o impacto causal de IA generativa via inferência causal (ex.: propensity score matching), considerando confundidores socioeconômicos.
    
    ### Limitações da Análise
    - Dados agregados por município limitam correlações individuais; análises com MICRODADOS revelariam padrões mais granulares.
    - Fatores externos (ex.: mudanças curriculares, motivação pós-pandemia) não foram controlados.
    
    Este relatório destaca a necessidade urgente de equilibrar conectividade universal com acesso a ferramentas produtivas, garantindo que a transformação digital beneficie todos os alunos cearenses de forma equitativa.
    """)