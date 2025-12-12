# Estudo Educacional - Ceará

## 📊 Sobre o Projeto

Este projeto realiza uma análise detalhada dos microdados do ENEM no estado do Ceará, comparando os anos de 2019 e 2024. O foco principal é investigar a infraestrutura digital educacional disponível para os estudantes através da criação de uma métrica inovadora: a **Taxa de Suporte Digital Educacional (TSDE)**.

## 🎯 Objetivo

Avaliar a evolução do acesso à infraestrutura digital dos estudantes cearenses participantes do ENEM, medindo a interseção entre a disponibilidade de internet e computador nas residências dos alunos. Esta análise permite compreender as condições de suporte digital para o aprendizado e como elas evoluíram ao longo dos anos.

## 📈 Métrica Principal

### Taxa de Suporte Digital Educacional (TSDE)

**Definição:** Percentual de alunos que possuem **simultaneamente** acesso à internet E computador em suas residências.

```
TSDE = (Alunos com Internet ∩ Alunos com Computador) / Total de Alunos × 100
```

Esta métrica é crucial pois reflete a capacidade real dos estudantes de acessarem conteúdos educacionais digitais, participarem de aulas online e realizarem atividades que exigem conectividade e dispositivos adequados.

## 🗂️ Estrutura do Projeto

```
Estudo-Educacional-CE/
├── Atividade_Enem.ipynb    # Notebook principal com análises
├── app.py                   # Aplicação principal (Dashboard/Interface)
├── func.py                  # Funções auxiliares e processamento de dados
├── img.py                   # Funções para geração de visualizações
├── indicadores19.csv        # Indicadores processados de 2019
├── indicadores24.csv        # Indicadores processados de 2024
├── imgs/                    # Pasta com visualizações geradas
├── requirements.txt         # Dependências do projeto
└── .gitignore              # Arquivos ignorados pelo Git
```

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/mh-vasconcelos/Estudo-Educacional-CE.git
cd Estudo-Educacional-CE
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando o Projeto

**Análise Exploratória:**
```bash
jupyter notebook Atividade_Enem.ipynb
```

**Aplicação/Dashboard:**
```bash
python app.py
```

## 📊 Dados Utilizados

Os dados são provenientes dos **microdados do ENEM** disponibilizados pelo INEP (Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira), com foco nos seguintes anos:
- **2019**: Ano pré-pandemia (baseline)
- **2024**: Ano mais recente disponível

### Variáveis Principais
- Acesso à internet residencial
- Disponibilidade de computador
- Localização geográfica (municípios do Ceará)
- Características socioeconômicas
- Desempenho no ENEM

## 🔍 Análises Realizadas

1. **Evolução da Taxa de Suporte Digital Educacional (2019 vs 2024)**
2. **Distribuição geográfica da infraestrutura digital**
3. **Correlação entre suporte digital e desempenho no ENEM**
4. **Análise por perfil socioeconômico**
5. **Identificação de municípios com maior déficit de infraestrutura**

## 📸 Visualizações

As visualizações geradas pelo projeto estão disponíveis na pasta `imgs/` e incluem:
- Mapas de calor da distribuição de infraestrutura
- Gráficos comparativos entre os anos
- Análises de correlação
- Rankings municipais

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **Matplotlib/Seaborn**: Visualizações estáticas
- **Plotly**: Visualizações interativas
- **Jupyter Notebook**: Ambiente de análise exploratória

## 👥 Autores

- **Matheus Vasconcelos** - [@mh-vasconcelos](https://github.com/mh-vasconcelos)

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional e pesquisa.

## 📚 Referências

- [Microdados do ENEM - INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)
- Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Abrir issues relatando bugs ou sugerindo melhorias
- Enviar pull requests com novas análises ou correções
- Compartilhar o projeto

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório ou entre em contato através do GitHub.

---

**Desenvolvido com 📊 para análise educacional do Ceará**
