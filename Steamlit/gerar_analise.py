import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

sns.set()

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None

st.set_page_config(
    page_title='SINASC Rondônia',
    page_icon='https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_map_of_Rondonia.png',
    layout='wide'
)

st.title('Análise SINASC - Rondônia')
st.header('Explorando recursos streamlit')
st.subheader('Projeto EBAC - Cientista de dados')

# Obtém o caminho relativo da imagem em relação ao diretório do script
image_path = Path(__file__).with_name("mapa_rondonia.png").relative_to(Path.cwd())

# Exibe a imagem
st.image(str(image_path))

st.write('--------')

st.header('Visualizando o dataframe')

sinasc = pd.read_csv(r"C:\Users\Igor\Documents\GitHub\volta-zero\Steamlit\input_M15_SINASC_RO_2019.csv")

sinasc

st.subheader('Descrição das variaveis')

sinasc.describe

st.write('--------')

sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)

min_data = sinasc.DTNASC.min()
max_data = sinasc.DTNASC.max()

data_inicial = st.sidebar.date_input('Data inicial',
                                     value=min_data,
                                     min_value=min_data,
                                     max_value=max_data)
data_final = st.sidebar.date_input('Data final',
                                   value=max_data,
                                   min_value=min_data,
                                   max_value=max_data)


liberar_analises_finais = st.checkbox("Ver gráficos")

# Adiciona uma barra de progresso
progresso = st.progress(0)

# Adiciona um elemento de texto dinâmico
info_texto = st.empty()

# Adiciona um botão para redefinir os filtros de data
if st.sidebar.button('Resetar Filtros'):
    data_inicial = min_data
    data_final = max_data

# Filtra os dados com base nos filtros
sinasc_filtrado = sinasc[
    (sinasc['DTNASC'] <= pd.to_datetime(data_final)) &
    (sinasc['DTNASC'] >= pd.to_datetime(data_inicial)) 
]

# Atualiza a barra de progresso e o texto dinâmico
progresso.progress(25)
info_texto.text('Dados filtrados.')

# Executa análises apenas se a opção estiver marcada
if liberar_analises_finais:
    # Adiciona um gráfico de barras para visualizar os dados de escolaridade da mãe
    st.bar_chart(sinasc_filtrado['ESCMAE'].value_counts())

    # Atualiza a barra de progresso e o texto dinâmico
    progresso.progress(50)
    info_texto.text('Análises finais realizadas.')

    # Executa análises adicionais
    plota_pivot_table(sinasc_filtrado, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')
    plota_pivot_table(sinasc_filtrado, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento', 'unstack')
    plota_pivot_table(sinasc_filtrado, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')
    plota_pivot_table(sinasc_filtrado, 'PESO', 'ESCMAE', 'median', 'PESO mediano', 'escolaridade mae', 'sort')
    plota_pivot_table(sinasc_filtrado, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio', 'gestacao', 'sort')

    # Atualiza a barra de progresso e o texto dinâmico
    progresso.progress(100)
    info_texto.text('Análises concluídas.')

# Oculta a barra de progresso e o texto dinâmico ao finalizar
progresso.empty()
info_texto.empty()





